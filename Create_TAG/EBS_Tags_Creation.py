#!/usr/bin/env python3

import boto3
import os

os.environ['AWS_PROFILE'] = "DevOps"
os.environ['AWS_DEFAULT_REGION'] = "us-east-2"

def lambda_handler():
  client = boto3.client('ec2')
    
  volumes = 'vol-0b1b1c2', 'vol-005be6c5'
  
  for ids in volumes:  
    instance = client.describe_volumes(VolumeIds=[ids])
    
    hostList = []
    
    for vol in instance['Volumes']:
        for attch in vol['Attachments']:
            hostList.append(attch['InstanceId'])
            
    print(hostList)
            
    reservations = client.describe_instances(InstanceIds=hostList)
        
    for reservation in reservations['Reservations']:
     for instance in reservation['Instances']:
       for tag in instance['Tags']:
         if tag['Key'] == 'Name':
            Name = tag['Value']
         
         if tag['Key'] == 'business_group':
            business_group = tag['Value']
            
         if tag['Key'] == 'env_type':
            env_type = tag['Value']
        
         if tag['Key'] == 'env_name':
            env_name = tag['Value']
            
         if tag['Key'] == 'layer':
            layer = tag['Value']
         
         if tag['Key'] == 'system':
            system = tag['Value']
         
    ec2 = boto3.resource('ec2')
    
    volume = ec2.Volume(ids)
    tag = volume.create_tags(
        Tags=[{'Key': 'Name', 'Value': Name},
              {'Key': 'business_group', 'Value': business_group},
              {'Key': 'env_type', 'Value': env_type},
              {'Key': 'env_name', 'Value': env_name},
              {'Key': 'layer', 'Value': layer},
              {'Key': 'system', 'Value': system},
        ]
    ) 
    
    print(tag)

lambda_handler()
