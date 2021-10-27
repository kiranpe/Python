import boto3
import botocore
import paramiko
import os

def lambda_handler(event, context):
    #Get IP addresses of EC2 instances
    client = boto3.client('ec2')
    instDict=client.describe_instances(
            Filters=[{'Name':'tag:Environment','Values':['Dev']}]
        )
    hostList=[]
    for r in instDict['Reservations']:
        for inst in r['Instances']:
            hostList.append(inst['PublicIpAddress'])
            
    print(hostList)
               
    s3_client = boto3.client('s3')
    #Download private key file from secure S3 bucket
    s3_client.download_file('pranitha-lambda-101','keys/devops.pem', '/tmp/devops.pem')

    # reading pem file and creating key object
    key = paramiko.RSAKey.from_private_key_file("/tmp/devops.pem")
    # an instance of the Paramiko.SSHClient
    ssh_client = paramiko.SSHClient()
    # setting policy to connect to unknown host
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    host=hostList[0]
    print("Connecting to " + host)
    # connecting to server
    ssh_client.connect( hostname = host, username = "ubuntu", pkey = key)
    print("Connected to " + host)

    commands = [
        "aws s3 cp s3://kiran-aws-batch-101/scripts/HelloWorld.sh /home/ubuntu/HelloWorld.sh",
        "chmod 700 /home/ubuntu/HelloWorld.sh",
        "/home/ubuntu/HelloWorld.sh"
        ]
    for command in commands:
        print("Executing {}".format(command))
        stdin , stdout, stderr = ssh_client.exec_command(command)
        print(stdout.read())
        print(stderr.read())

    return
    {
        'message' : "Script execution completed. See Cloudwatch logs for complete output"
    }
