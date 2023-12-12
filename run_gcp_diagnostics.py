"""
The service account that runs this test must have the following roles:
- roles/compute.instanceAdmin.v1
- roles/compute.securityAdmin
- roles/iam.serviceAccountAdmin
- roles/iam.serviceAccountKeyAdmin
- roles/iam.serviceAccountUser
The Project Editor legacy role is not sufficient because it does not grant
several necessary permissions.
"""
from __future__ import annotations

import base64
import contextlib
import json
import subprocess
import time
import uuid
import logging
import requests
import argparse
from typing import Optional

from google.api_core.exceptions import BadRequest, NotFound
import google.auth
from google.cloud import compute_v1
from google.cloud import oslogin_v1
from google.oauth2 import service_account
import googleapiclient.discovery
import googleapiclient.errors

def init_logger():
   time_format = '%d-%b-%Y %H:%M:%S %p %Z'
   logger = logging.getLogger(__name__)
   logging.basicConfig(format='%(asctime)s - [%(levelname)s]  %(message)s', datefmt=time_format, level=logging.INFO)
   return logger

def download_diagnostic_script(download_script_cmd: str, project: str, zone: str, instance: str) -> str:
    download_script = [
        "gcloud",
        "compute",
        "ssh",
        "--project",
        f"{project}",
        "--zone",
        f"{zone}",
        f"{instance}",
        "--command",
        download_script_cmd,
    ]
    init_logger().info(f"Running diagnostic sript download command: {' '.join(download_script)}")
    tries = 0
    while tries < 3:
        try:
            ssh = subprocess.run(
                download_script,
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                check=True,
                timeout=10,
            )
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as err:
            time.sleep(10)
            tries += 1
            if tries == 3:
                if isinstance(err, subprocess.CalledProcessError):
                    init_logger().error(
                        f"Failed to run SSH command (return code: {err.returncode}. Output received: {err.output}"
                    )
                else:
                    init_logger().error("Failed to run SSH - timed out.")
                raise err
        else:
            return ssh.stdout

def run_diagonstic_script(cmd: str, project: str, zone: str, instance: str) -> str:
    run_diagonstic_script = [
        "gcloud",
        "compute",
        "ssh",
        "--project",
        f"{project}",
        "--zone",
        f"{zone}",
        f"{instance}",
        "--command",
        cmd,
    ]
    init_logger().info(f"Running diagnostic script: {' '.join(run_diagonstic_script)}")
    tries = 0
    while tries < 3:
        try:
            ssh = subprocess.run(
                run_diagonstic_script,
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                check=True,
                timeout=10,
            )
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as err:
            time.sleep(10)
            tries += 1
            if tries == 3:
                if isinstance(err, subprocess.CalledProcessError):
                    init_logger().error(
                        f"Failed to run SSH command (return code: {err.returncode}. Output received: {err.output}"
                    )
                else:
                    init_logger().error("Failed to run SSH - timed out.")
                raise err
        else:
            return ssh.stdout

def main(cmd: str, project: str, instance: Optional[str] = None, zone: Optional[str] = None, download_script_cmd: Optional[str] = None, oslogin: Optional[oslogin_v1.OsLoginServiceClient] = None,) -> str:
    # Run a download diagnostic script command on the remote instance over SSH.
    download_diagnostic_script_result = download_diagnostic_script(download_script_cmd, project, zone, instance)
    # Run a diagnostic command on the remote instance over SSH.
    run_diagonstic_script_result = run_diagonstic_script(cmd, project, zone, instance)

    # Print the command line output from the remote instance.
    init_logger().info(download_diagnostic_script_result)
    return download_diagnostic_script_result
    init_logger().info(run_diagonstic_script_result)
    return run_diagonstic_script_result
        
def oslogin_instance():
    PROJECT = f"<your project>"
    ZONE = "us-east1-d"
    INSTNACE_NAME = f"<your cluster master name>"
    FIREWALL_TAG = "allow-ssh"
    HOME_DIR = "/home/kiran_peddineni"
    cmd = f"sudo bash {HOME_DIR}/diagnostic-script.sh"
    download_script_cmd = "gsutil cp gs://dataproc-diagnostic-scripts/diagnostic-script.sh ."
    instance = compute_v1.Instance()
    instance.name = INSTNACE_NAME

    sa = compute_v1.ServiceAccount()
    sa.email = f"<sevice_account"
    sa.scopes = ["https://www.googleapis.com/auth/cloud-platform"]
    instance.service_accounts = [sa]

    instance.metadata = compute_v1.Metadata()
    item = compute_v1.Items()
    item.key = "enable-oslogin"
    item.value = "TRUE"
    instance.metadata.items = [item]
    instance.zone = ZONE
    
    client = compute_v1.InstancesClient()
    for attempt in range(5):
        time.sleep(5)
        instance = client.get(project=PROJECT, zone=ZONE, instance=instance.name)
        if instance.status == "RUNNING":
            init_logger().info(f"{instance.name} instance is {instance.status} from 15hrs.. Running diagnostics!!")
            main(cmd=cmd, project=PROJECT, instance=instance.name, zone=ZONE, download_script_cmd=download_script_cmd,)
            break
       
        if instance.status != "RUNNING":
            init_logger().info(f"Instance is not in {instance.status} state.. No need of diagnostics!!")
            break

oslogin_instance()
