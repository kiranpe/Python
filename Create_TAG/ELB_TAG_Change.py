#!/usr/bin/env python3

import boto3
import os

os.environ['AWS_PROFILE'] = "DevOps"
os.environ['AWS_DEFAULT_REGION'] = "us-east-2"

def lambda_handler():
    client = boto3.client('elbv2')
      
    ARNs = ['arn:aws:elasticloadbalancing:us-east-2:9015xxxx77:loadbalancer/app/test/b7a4102517408d86',]
      
    for arn in ARNs:  
      response = client.add_tags(ResourceArns=[arn],
         Tags=[{'Key': 'System', 'Value': 'test',}, 
               {'Key': 'CreatedBy', 'Value': 'Kiran',}, 
               {'Key': 'Type', 'Value': 'alb',}, 
               {'Key': 'Layer', 'Value': 'app'},
               {'Key': 'Env', 'Value': 'testenv'},
         ]
      )
      

      elb = client.describe_tags(ResourceArns=[arn],)
      
      for tagvalues in elb['TagDescriptions']:
        for tag in tagvalues['Tags']:
         if tag['Key'] == 'CreatedBy':
            createdby = tag['Value']
                
         if tag['Key'] == 'Type':
            type_tag = tag['Value']
                
         if tag['Key'] == 'System':
            system = tag['Value']
         
         if tag['Key'] == 'Layer':
            layer = tag['Value']
         
         if tag['Key'] == 'Env':
            env = tag['Value']
                
      Name_Tag = env + '-' + system + '-' + layer + '-' + type_tag
      
      print()
      print(Name_Tag)
      print()
      
      response = client.add_tags(ResourceArns=[arn], Tags=[{'Key': 'Name', 'Value': Name_Tag,},])
      
      print(response)

lambda_handler()
