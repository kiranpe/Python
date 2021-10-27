#!/usr/bin/env python3

import boto3
import os
import json

os.environ['AWS_PROFILE'] = "DevOps"
os.environ['AWS_DEFAULT_REGION'] = "us-east-2"

def lambda_handler():
    ec2 = boto3.client('ec2')
   
    filters = [{'Name': 'tag:componenet_type', 'Values': ['application server']}]
    instances = ec2.describe_instances(Filters=filters)

    for reservation in instances['Reservations']:
      for instance in reservation['Instances']:
        for tag in instance['Tags']:
            if 'componenet_type'in tag['Key']:
                print("Current TAG Value : %s" % tag['Value'])

    ids = []

    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            ids.append(instance['InstanceId'])

    print("Changing tags for %d instances" % len(ids))

    print("Changing TAG for: {}".format(ids))
    
    try:
      ec2.create_tags(Resources=ids, Tags=[{'Key': 'componenet_type', 'Value': 'application_server'}])
 
    except:
      print("All TAG values are correct.. No change needed..")

    return {
        'statusCode': 200,
        'message': 'Script execution completed successfully.'
    }

lambda_handler()
