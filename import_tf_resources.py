import hcl2
from python_terraform import Terraform
import argparse
import logging
import os

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
        "project_iam": "google_project_iam_member.token_creator_binding"
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
    parser.add_argument("--export", action="store_true", help="Output exportable project ID for sourcing")
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

                    if project_number:
                        sa_email = f"service-{project_number}@gcp-sa-pubsub.iam.gserviceaccount.com"
                        iam_target = f"module.{mod_name}.{RESOURCE_MAP[resource_type]['iam_topic']}[\"roles/pubsub.publisher\"]"
                        iam_id = f"projects/{project_id}/topics/{topic_name} roles/pubsub.publisher serviceAccount:{sa_email}"
                        imports.append((iam_target, iam_id))

                push_subs = attrs.get("push_subscriptions", [])
                for sub in push_subs:
                    sub_name = sub.get("name")
                    if sub_name:
                        tf_target = f'module.{mod_name}.{RESOURCE_MAP[resource_type]["subscription_push"]}["{sub_name}"]'
                        tf_id = f"projects/{project_id}/subscriptions/{sub_name}"
                        imports.append((tf_target, tf_id))

                        if project_number:
                            sa_email = f"service-{project_number}@gcp-sa-pubsub.iam.gserviceaccount.com"
                            iam_target = f'module.{mod_name}.{RESOURCE_MAP[resource_type]["iam_subscription"]}["{sub_name}_push"]'
                            iam_id = f"projects/{project_id}/subscriptions/{sub_name} roles/pubsub.subscriber serviceAccount:{sa_email}"
                            imports.append((iam_target, iam_id))

                pull_subs = attrs.get("pull_subscriptions", [])
                for sub in pull_subs:
                    sub_name = sub.get("name")
                    if sub_name:
                        tf_target = f'module.{mod_name}.{RESOURCE_MAP[resource_type]["subscription_pull"]}["{sub_name}"]'
                        tf_id = f"projects/{project_id}/subscriptions/{sub_name}"
                        imports.append((tf_target, tf_id))

                        if project_number:
                            sa_email = f"service-{project_number}@gcp-sa-pubsub.iam.gserviceaccount.com"
                            iam_target = f'module.{mod_name}.{RESOURCE_MAP[resource_type]["iam_subscription"]}["{sub_name}_pull"]'
                            iam_id = f"projects/{project_id}/subscriptions/{sub_name} roles/pubsub.subscriber serviceAccount:{sa_email}"
                            imports.append((iam_target, iam_id))

                if project_number and not token_creator_added:
                    sa_email = f"service-{project_number}@gcp-sa-pubsub.iam.gserviceaccount.com"
                    tf_target = f"module.{mod_name}.{RESOURCE_MAP[resource_type]['project_iam']}[0]"
                    tf_id = f"projects/{project_id}/roles/iam.serviceAccountTokenCreator serviceAccount:{sa_email}"
                    imports.append((tf_target, tf_id))
                    token_creator_added = True

    return imports

def write_import_file(imports, output_file):
    with open(output_file, "w") as f:
        for target, tf_id in imports:
            f.write(f'''import {{\n  to = {target}\n  id = {tf_id}\n}}\n\n''')
    logging.info(f"✅ Wrote {len(imports)} import blocks to {output_file}")

def run_imports(imports, execute=False):
    tf = Terraform()
    for target, resource_id in imports:
        logging.info(f">>> Importing: {target}")
        logging.info(f"    ID: {resource_id}")
        if execute:
            code, out, err = tf.cmd("import", target, resource_id)
            if code != 0:
                logging.error(f"❌ Failed: {err}")
            else:
                logging.info("✅ Success")

def export_project_id(modules, export_format=False):
    seen = False
    for module in modules:
        for _, attrs in module.items():
            if not seen and "project_id" in attrs:
                if export_format:
                    print(f"export GOOGLE_PROJECT={attrs['project_id']}")
                else:
                    print(f"Set GOOGLE_PROJECT={attrs['project_id']}")
                seen = True
                return

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


    args = parse_args()
    setup_logger(args.log)
    modules = parse_modules(args.file)
    imports = build_imports(modules, args.type, args.project_number)
    write_import_file(imports, args.output)
    run_imports(imports, args.execute)
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
        export_project_id(modules, args.export)

if __name__ == "__main__":
    main()
