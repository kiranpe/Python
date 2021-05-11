#!/usr/bin/env python3

import boto3
import os

os.environ['AWS_PROFILE'] = "DevOps"
os.environ['AWS_DEFAULT_REGION'] = "us-east-2"

def lambda_handler():
    ec2 = boto3.resource('ec2')
    security_group = ec2.SecurityGroup('sg-xxxxxxxx8d')
    tag = security_group.create_tags(

       Tags=[
          {
            'Key' : 'Team',
            'Value': "DevOps"
          },
          {
            'Key': 'Created By',
            'Value': 'Kiran'
          },
        ]
    )
    
    print(tag)

lambda_handler()
