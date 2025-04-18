import argparse
import importlib
import json
import logging
import os
import subprocess
import uuid
import hcl2
from python_terraform import Terraform

RESOURCE_MAP = {
    "service_account": {
        "base": "google_service_account.this",
        "iam": {
            "member": "google_service_account_iam_member",
            "binding": "google_service_account_iam_binding"
        }
    },
    "storage_bucket": {
        "base": "google_storage_bucket.this"
    },
    "compute_instance": {
        "base": "google_compute_instance.this"
    },
    "pubsub": {
        "topic": "google_pubsub_topic.this",
        "subscription_push": "google_pubsub_subscription.push",
        "subscription_pull": "google_pubsub_subscription.pull",
        "iam_topic": "google_pubsub_topic_iam_member",
        "iam_subscription": "google_pubsub_subscription_iam_member",
        "project_iam": "google_project_iam_member.token_creator_binding",
        
    }
}

def parse_args():
    parser = argparse.ArgumentParser(description="Generate import blocks for Terraform modules")
    parser.add_argument("--file", default="resources.tf", help="Path to the .tf file")
    parser.add_argument("--type", choices=RESOURCE_MAP.keys(), required=True)
    parser.add_argument("--output", default="import.tf", help="Output import.tf file")
    parser.add_argument("--execute", action="store_true", help="Optionally run terraform import")
    parser.add_argument("--log", help="Log output to file")
    parser.add_argument("--project-number", default=None, help="Project number for IAM service account email")
    parser.add_argument("--fix-state", action="store_true", help="Fix missing 'project' in IAM state after apply")
    return parser.parse_args()

def setup_logger(log_file=None):
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        handlers=[logging.FileHandler(log_file), logging.StreamHandler()] if log_file else [logging.StreamHandler()]
    )

def parse_modules(file_path):
    with open(file_path, 'r') as f:
        return hcl2.load(f).get("module", [])

def build_imports(modules, resource_type, project_number=None):
    def get_sa_email():
        if project_number:
            return f"service-{project_number}@gcp-sa-pubsub.iam.gserviceaccount.com"
        return None
    imports = []
    token_creator_added = False

    for module in modules:
        for mod_name, attrs in module.items():
            project_id = attrs.get("project_id", "")
            name = attrs.get("name", "")

            if resource_type == "service_account":
                sa_email = f"{name}@{project_id}.iam.gserviceaccount.com"
                imports.append((f"module.{mod_name}.{RESOURCE_MAP[resource_type]['base']}",
                                 f"projects/{project_id}/serviceAccounts/{sa_email}"))

                for role in attrs.get("iam_roles", []):
                    target = f"module.{mod_name}.{RESOURCE_MAP[resource_type]['iam']['member']}[\"{role}\"]"
                    resource_id = f"projects/{project_id}/serviceAccounts/{sa_email} roles/{role}"
                    imports.append((target, resource_id))

            elif resource_type == "storage_bucket":
                bucket_name = attrs.get("bucket_name", "")
                if bucket_name:
                    tf_target = f"module.{mod_name}.{RESOURCE_MAP[resource_type]['base']}"
                    tf_id = bucket_name
                    imports.append((tf_target, tf_id))

            elif resource_type == "compute_instance":
                zone = attrs.get("zone", "")
                if name and zone:
                    tf_target = f"module.{mod_name}.{RESOURCE_MAP[resource_type]['base']}"
                    tf_id = f"projects/{project_id}/zones/{zone}/instances/{name}"
                    imports.append((tf_target, tf_id))

            elif resource_type == "pubsub":
                topic_name = attrs.get("topic")
                if topic_name:
                    tf_target = f"module.{mod_name}.{RESOURCE_MAP[resource_type]['topic']}[0]"
                    tf_id = f"projects/{project_id}/topics/{topic_name}"
                    imports.append((tf_target, tf_id))

                    sa_email = get_sa_email()
                    if not project_number:
                        logging.warning(f"⚠️  Skipping IAM import for topic '{topic_name}' due to missing --project-number.")
                    elif sa_email:
                        iam_id = f"projects/{project_id}/topics/{topic_name} roles/pubsub.publisher serviceAccount:{sa_email}"
                        imports.append((iam_target, iam_id))

                push_subs = attrs.get("push_subscriptions", [])
                for sub in push_subs:
                    if project_number and "oidc_service_account_email" in sub:
                        sa_email = sub["oidc_service_account_email"]
                        tf_target = f"module.{mod_name}.{RESOURCE_MAP[resource_type]['project_iam']}[\"{sub['name']}_token_creator\"]"
                        tf_id = f"projects/{project_id}/roles/iam.serviceAccountTokenCreator serviceAccount:{sa_email}"
                        imports.append((tf_target, tf_id))
                    elif not project_number:
                        logging.warning(f"⚠️  Skipping token_creator_binding for push subscription '{sub.get('name')}' in module '{mod_name}' due to missing --project-number.")

                pull_subs = attrs.get("pull_subscriptions", [])
                for sub in pull_subs:
                    if project_number and "service_account" in sub:
                        sa_email = sub["service_account"]
                        tf_target = f"module.{mod_name}.{RESOURCE_MAP[resource_type]['project_iam']}[\"{sub['name']}_token_creator\"]"
                        tf_id = f"projects/{project_id}/roles/iam.serviceAccountTokenCreator serviceAccount:{sa_email}"
                        imports.append((tf_target, tf_id))
                    elif not project_number:
                        logging.warning(f"⚠️  Skipping token_creator_binding for pull subscription '{sub.get('name')}' in module '{mod_name}' due to missing --project-number.")


                        if not project_number:
                            logging.warning(f"⚠️  Skipping IAM import for pull subscription '{sub_name}' due to missing --project-number.")
                        elif sa_email:
                            iam_target = f'module.{mod_name}.{RESOURCE_MAP[resource_type]["iam_subscription"]}["{sub_name}_pull"]'
                            iam_id = f"projects/{project_id}/subscriptions/{sub_name} roles/pubsub.subscriber serviceAccount:{sa_email}"
                            imports.append((iam_target, iam_id))

                
    return imports

def write_import_file(imports, output_file):
    with open(output_file, "w") as f:
        for target, tf_id in imports:
            f.write(f'''import {{\n  to = {target}\n  id = {tf_id}\n}}\n\n''')
    logging.info(f"✅ Wrote {len(imports)} import blocks to {output_file}")

def run_imports(imports, execute=False, project_id=None, project_number=None, output_script="import_pubsub_iam.sh"):
    tf = Terraform()
    pubsub_iam_commands = []

    for target, resource_id in imports:
        logging.info(f">>> Importing: {target}")
        logging.info(f"    ID: {resource_id}")

        if execute:
            # Special case: for pubsub IAM resources, collect shell script
            if "pubsub" in target and "iam_member" in target and "token_creator_binding" not in target:
                member_cmd = f'GOOGLE_PROJECT="{project_id}" terraform import {target} "{resource_id}"
'
                pubsub_iam_commands.append(member_cmd)
            else:
                code, out, err = tf.cmd("import", target, resource_id)
                if code != 0:
                    logging.error(f"❌ Failed: {err}")
                else:
                    logging.info("✅ Success")

    # Write shell script if needed
    if pubsub_iam_commands:
        with open(output_script, "w") as f:
            f.writelines(pubsub_iam_commands)
        os.chmod(output_script, 0o755)
        print(f"⚙️  Pub/Sub IAM import commands written to: {output_script}")
        
        
        print("▶️  Executing pubsub IAM import script manually...")
        os.system(f"./{output_script}")
        if project_id:
            os.system("terraform state pull > tfstate.json")
            fix_state_project("pubsub", project_id)



def fix_state_project(resource_type, project_id, state_path="tfstate.json"):
    import json
    import uuid

    with open(state_path) as f:
        state = json.load(f)

    fixed = False
    for module in state.get("resources", []):
        if module["type"].startswith("google_pubsub_") and module["type"].endswith("iam_member"):
            for instance in module.get("instances", []):
                attrs = instance.get("attributes", {})
                if "project" not in attrs:
                    attrs["project"] = project_id
                    fixed = True

    if fixed:
        fixed_state = f"fixed-{uuid.uuid4().hex}.json"
        with open(fixed_state, "w") as f:
            json.dump(state, f, indent=2)
        print(f"Updated state written to: {fixed_state}")
        os.system(f"terraform state push {fixed_state}")
    else:
        print("No changes made to state.")


def verify_tools():
    import venv
    if not venv.__file__:
        print("⚠️  Not running inside a virtual environment. It's recommended to use one for Python dependencies.")
    required_tools = ["terraform"]
    for tool in required_tools:
        if os.system(f"which {tool} > /dev/null 2>&1") != 0:
            print(f"❌ Required tool '{tool}' not found in PATH. Please install it.")
            exit(1)

    # Auto-install missing Python packages if possible
    required_packages = ["hcl2", "python_terraform"]
    for package in required_packages:
        try:
            importlib.import_module(package)
        except ImportError:
            print(f"⚠️  Python package '{package}' not found. Attempting to install...")
            subprocess.check_call(["pip", "install", package])


    # Check Terraform version
    try:
        version_output = subprocess.check_output(["terraform", "version"], stderr=subprocess.STDOUT).decode()
        version_line = version_output.splitlines()[0]
        version = version_line.split()[1].lstrip("v")
        major, minor, *_ = map(int, version.split("."))
        if (major, minor) < (1, 6):
            print(f"❌ Terraform version >= 1.6 required. Detected: {version}")
            exit(1)
    except Exception as e:
        print(f"❌ Failed to check Terraform version: {e}")
        exit(1)


def main():
    verify_tools()
    args = parse_args()
    setup_logger(args.log)
    modules = parse_modules(args.file)
    imports = build_imports(modules, args.type, args.project_number)
    write_import_file(imports, args.output)
    run_imports(imports, args.execute, project_id=args.project_number, project_number=args.project_number)

    if args.fix_state:
        if not args.execute:
            print("⚠️  '--fix-state' requires '--execute' to be set.")
        elif args.type != "pubsub":
            print("⚠️  '--fix-state' currently only supported for --type=pubsub.")
        elif not args.project_number:
            print("⚠️  '--fix-state' requires '--project-number' to be provided.")
        else:
            project_id = None
            for module in modules:
                for _, attrs in module.items():
                    if "project_id" in attrs:
                        project_id = attrs["project_id"]
                        break
            if project_id:
                os.system("terraform state pull > tfstate.json")
                fix_state_project(args.type, project_id)

if __name__ == "__main__":
    main()
