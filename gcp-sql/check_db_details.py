#!/usr/bin/env python3

import os
import json
import psycopg2
from googleapiclient import discovery
from google.oauth2 import service_account

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/home/kiran/devops/Terraform/Gcp/credentials.json"

credentials = service_account.Credentials.from_service_account_file(
        filename=os.environ['GOOGLE_APPLICATION_CREDENTIALS'],
        scopes=['https://www.googleapis.com/auth/cloud-platform'])

service = discovery.build('sqladmin', 'v1beta4', credentials=credentials)
req = service.instances().list(project="pythonproject-335216")
resp = req.execute()
print(json.dumps(resp, indent=2))
