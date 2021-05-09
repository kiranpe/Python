#!/usr/bin/env python3

import boto3
import os

os.environ['AWS_PROFILE'] = "DevOps"
os.environ['AWS_DEFAULT_REGION'] = "us-east-2"

def lambda_handler():
      client = boto3.client('elbv2')
      
      system = 'test'
      CreatedBy = "Kiran P"
      layer_TAG = 'web'
      Type = 'alb'
      Name_TAG = system + "-" + layer_TAG + "-" + Type
      
      ARNs = ['arn:aws:elasticloadbalancing:us-east-2:901593578477:loadbalancer/app/testing/ab807acac88ae960', 'arn:aws:elasticloadbalancing:us-east-2:901593578477:loadbalancer/app/test/3c6b2b1b80eda0e6']
      
      
      for arn in ARNs:
        response = client.add_tags(ResourceArns=[arn],
          Tags=[
            {
              'Key': 'Name',
              'Value': Name_TAG,
            },
            {
              'Key': 'Created By',
              'Value': CreatedBy,
            },
          ],
        )
        
        print(response)

lambda_handler()
