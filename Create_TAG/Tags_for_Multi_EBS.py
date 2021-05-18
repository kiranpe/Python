#!/usr/bin/env python3

import boto3
import os

os.environ['AWS_PROFILE'] = "DevOps"
os.environ['AWS_DEFAULT_REGION'] = "us-east-2"

def lambda_handler():
  client = boto3.client('ec2')
    
  volumes = ['vol-00568fdxxx58be6c5', 'vol-0b1b88xxxdc51c2']
  
  for ids in volumes:  
    instance = client.describe_volumes(VolumeIds=[ids])
    
    hostList = []
    
    for vol in instance['Volumes']:
        for attch in vol['Attachments']:
            hostList.append(attch['InstanceId'])
    
    for host in hostList:        
       reservations = client.describe_instances(InstanceIds=[host])
        
    for reservation in reservations['Reservations']:
       for instance in reservation['Instances']:
         tags = {}
         for tag in instance['Tags']:
           tags[tag['Key']] = tag['Value']
           
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
          
    tags = {}
    for tag in vol['Tags']:
      tags[tag['Key']] = tag['Value']
  
        
    if not 'Name' in tags:
        print(attch['VolumeId'] + " " + "volume does not have Name tag")
        nametag = client.create_tags(Resources=[attch['VolumeId']], Tags=[{'Key': 'Name', 'Value': Name}])
        print("\nCreating Name tag for volume : {}".format(attch['VolumeId']), "Name tag Value is : {}".format(Name))
          
    elif tags['Name'] in Name:
        print(attch['VolumeId'] + " " + "volume has Name tag")
        
    if not 'business_group' in tags:
        print(attch['VolumeId'] + " " + "volume does not have business_group tag")
        nametag = client.create_tags(Resources=[attch['VolumeId']], Tags=[{'Key': 'business_group', 'Value': business_group}])
        print("\nCreating business_group tag for volume : {}".format(attch['VolumeId']))
          
    elif tags['business_group'] in business_group:
        print(attch['VolumeId'] + " " + "volume has business_group tag")
        
    if not 'env_name' in tags:
        print(attch['VolumeId'] + " " + "volume does not have env_name tag")
        nametag = client.create_tags(Resources=[attch['VolumeId']], Tags=[{'Key': 'env_name', 'Value': env_name}])
        print("\nCreating env_name tag for volume : {}".format(attch['VolumeId']))
          
    elif tags['env_name'] in env_name:
        print(attch['VolumeId'] + " " + "volume has env_name tag")
        
    if not 'env_type' in tags:
        print(attch['VolumeId'] + " " + "volume does not have env_type tag")
        nametag = client.create_tags(Resources=[attch['VolumeId']], Tags=[{'Key': 'env_type', 'Value': env_type}])
        print("\nCreating env_type tag for volume : {}".format(attch['VolumeId']))
          
    elif tags['env_type'] in env_type:
        print(attch['VolumeId'] + " " + "volume has env_type tag")
        
    if not 'layer' in tags:
        print(attch['VolumeId'] + " " + "volume does not have layer tag")
        nametag = client.create_tags(Resources=[attch['VolumeId']], Tags=[{'Key': 'layer', 'Value': layer}])
        print("\nCreating layer tag for volume : {}".format(attch['VolumeId']))
          
    elif tags['layer'] in layer:
        print(attch['VolumeId'] + " " + "volume has layer tag")

    if not 'system' in tags:
        print(attch['VolumeId'] + " " + "volume does not have system tag")
        nametag = client.create_tags(Resources=[attch['VolumeId']], Tags=[{'Key': 'system', 'Value': system}])
        print("\nCreating system tag for volume : {}".format(attch['VolumeId']))
          
    elif tags['system'] in system:
        print(attch['VolumeId'] + " " + "volume has system tag")

lambda_handler()
