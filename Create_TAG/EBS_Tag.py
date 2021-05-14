#!/usr/bin/env python3

import boto3
import os

os.environ['AWS_PROFILE'] = "DevOps"
os.environ['AWS_DEFAULT_REGION'] = "us-east-2"

def lambda_handler():

     ec2 = boto3.resource('ec2')

     ids = ('vol-00568be6c5', 'vol-0b1b887e2')

     for vol_id in ids:

       volume = ec2.Volume(vol_id)
       
       tag = volume.create_tags(
                Tags = [{"Key": "Env", "Value": "Test"},]
       )
 
       print(tag)

lambda_handler()
