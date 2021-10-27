import os
import boto3

AMI = os.environ['AMI']
INSTANCE_TYPE = os.environ['INSTANCE_TYPE']
KEY_NAME = os.environ['KEY_NAME']
SUBNET_ID = os.environ['SUBNET_ID']
REGION = os.environ['REGION']
SECURITY_GROUPS = os.environ['SECURITY_GROUPS']

ec2 = boto3.client('ec2', region_name=REGION)

def lambda_handler(event, context):
    init_script = """#!/bin/bash
                apt-get update -y
                apt-get install -y nginx
                service httpd start
                chkconfig httpd on
                shutdown -h +5"""
            
    LaunchSpecification={ 'SecurityGroupIds': [ SECURITY_GROUPS ] }
    
    instance = ec2.run_instances(
        ImageId=AMI,
        InstanceType=INSTANCE_TYPE,
        KeyName=KEY_NAME,
        SubnetId=SUBNET_ID,
        MaxCount=1,
        MinCount=1,
        InstanceInitiatedShutdownBehavior='terminate', 
        UserData=init_script
    )
    

    instance_id = instance['Instances'][0]['InstanceId']

    return instance_id
