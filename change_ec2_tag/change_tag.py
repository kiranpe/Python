import boto3
import os
import json

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')

    instances = ec2.describe_instances(Filters=[{'Name': 'tag:componenet_type', 'Values': ['application_server']}])

    ids = []

    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            ids.append(instance['InstanceId'])

    print("Changing tags for %d instances" % len(ids))

    print(ids)
    
    ec2.create_tags(Resources=ids, Tags=[{'Key': 'componenet_type', 'Value': 'application server'}])
 
    for reservation in instances['Reservations']:
      for instance in reservation['Instances']:
        for tag in instance['Tags']:
            if 'componenet_type'in tag['Key']:
                print(tag['Value'])
    
    return {
        'statusCode': 200,
        'message': 'Script execution completed successfully.'
    }
