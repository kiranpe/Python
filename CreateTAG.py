#!/usr/bin/env python3

import boto3
import os
import json

os.environ['AWS_PROFILE'] = "DevOps"
os.environ['AWS_DEFAULT_REGION'] = "us-east-2"

def lambda_handler():
  ec2 = boto3.client('ec2')
    
  instance_ids = ['i-0b592587dafa38729']
  
  for instance in instance_ids:  
    reservations = ec2.describe_instances(InstanceIds=[instance])
    
    print(reservations)

    for reservation in reservations['Reservations']:
       for instance in reservation['Instances']:
        tags = {}
        for tag in instance['Tags']:
            tags[tag['Key']] = tag['Value']

        if not 'Owner' in tags:
            print(instance['InstanceId'] + " does not have Owner tag")

            ownertag = ec2.create_tags(Resources=[instance['InstanceId']], Tags=[{'Key': 'Owner', 'Value': 'kiran'}])
            
            print("\nCreating Owner tag for : {}".format(instance['InstanceId']))

        

        elif tags['Owner'] in ['Kiran', 'kiran']:
            print(instance['InstanceId'] + " has [K|k]iran Owner tag")
            
        return{
           "statusCode": 200,
           "message": ""
        }

lambda_handler()
