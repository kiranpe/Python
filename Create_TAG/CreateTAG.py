#!/usr/bin/env python3

import boto3
import os
import json

os.environ['AWS_PROFILE'] = "DevOps"
os.environ['AWS_DEFAULT_REGION'] = "us-east-2"

def lambda_handler():
    ec2 = boto3.client('ec2')
    
    reservations = ec2.describe_instances().get('Reservations', [])

    for reservation in reservations:
       for instance in reservation['Instances']:
        tags = {}
        for tag in instance['Tags']:
            tags[tag['Key']] = tag['Value']

        if not 'Owner' in tags:
            print(instance['InstanceId'] + " does not have Owner tag")
            
            ids = []
    
            #Getting instanceids and storing values in ids
            for reservation in reservations:
                for instance in reservation['Instances']:
                    ids.append(instance['InstanceId'])
            
            try:
             #Create/Change tag value
             ec2.create_tags(Resources=ids, Tags=[{'Key': 'Owner', 'Value': 'kiran'}])
      
            except:
             #Print on Zero instance case
             print("No instance to change TAG.")
            
        elif tags['Owner'] in ['Kiran', 'kiran']:
            print(instance['InstanceId'] + " has [K|k]iran Owner tag")

lambda_handler()
