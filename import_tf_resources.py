import hcl2
from python_terraform import Terraform
import argparse
import logging

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
    }
}

def parse_args():
    parser = argparse.ArgumentParser(description="Terraform import automation for multiple resource types")
    parser.add_argument("--file", default="resources.tf", help="Path to .tf file")
    parser.add_argument("--type", choices=["service_account", "storage_bucket", "compute_instance"], required=True)
    parser.add_argument("--mode", choices=["member", "binding"], default="member", help="IAM mode (only for service_account)")
    parser.add_argument("--execute", action="store_true", help="Run terraform import (default is dry-run)")
    parser.add_argument("--log", help="Log output to file")
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

def build_imports(modules, resource_type, mode):
    imports = []
    for module in modules:
        for mod_name, attrs in module.items():
            project_id = attrs.get("project_id")
            name = attrs.get("name")
            if not project_id or not name:
                logging.warning(f"Skipping {mod_name} — missing project_id or name")
                continue

            if resource_type == "service_account":
                sa_email = f"{name}@{project_id}.iam.gserviceaccount.com"
                imports.append((
                    f"module.{mod_name}.{RESOURCE_MAP[resource_type]['base']}",
                    f"projects/{project_id}/serviceAccounts/{sa_email}"
                ))

                for role in attrs.get("iam_roles", []):
                    tf_res = RESOURCE_MAP[resource_type]["iam"][mode]
                    tf_target = f'module.{mod_name}.{tf_res}["{role}"]'
                    if mode == "member":
                        tf_id = f"projects/{project_id}/serviceAccounts/{sa_email} roles/{role}"
                    else:
                        tf_id = f"projects/{project_id}/serviceAccounts/{sa_email}/roles/{role}"
                    imports.append((tf_target, tf_id))

            elif resource_type == "storage_bucket":
                tf_target = f"module.{mod_name}.{RESOURCE_MAP[resource_type]['base']}"
                tf_id = f"{project_id}/{name}"
                imports.append((tf_target, tf_id))

            elif resource_type == "compute_instance":
                zone = attrs.get("zone")
                if not zone:
                    logging.warning(f"Skipping {mod_name} — missing zone for compute instance")
                    continue
                tf_target = f"module.{mod_name}.{RESOURCE_MAP[resource_type]['base']}"
                tf_id = f"projects/{project_id}/zones/{zone}/instances/{name}"
                imports.append((tf_target, tf_id))

    return imports

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

def main():
    args = parse_args()
    setup_logger(args.log)
    modules = parse_modules(args.file)
    imports = build_imports(modules, args.type, args.mode)
    run_imports(imports, args.execute)

if __name__ == "__main__":
    main()
