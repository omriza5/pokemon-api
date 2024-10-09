import boto3
import paramiko
import time

aws_management_console = boto3.session.Session(profile_name="py-user")
# Create a new EC2 client
ec2 = aws_management_console.client('ec2')

vpcs = ec2.describe_vpcs()

vpc_id = vpcs['Vpcs'][0]['VpcId']

security_group_name = 'pokemon-sg'
description = 'Security group for SSH and HTTP access'

try:
    response = ec2.create_security_group(
        GroupName=security_group_name,
        Description=description,
        VpcId=vpc_id
    )
    security_group_id = response['GroupId']
    print(f'Security Group {security_group_name} created with ID: {security_group_id}')

    # 2. Authorize inbound rules
    ec2.authorize_security_group_ingress(
        GroupId=security_group_id,
        IpPermissions=[
            {
                'IpProtocol': 'tcp',
                'FromPort': 22,
                'ToPort': 22,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}],  # Allow SSH from anywhere (replace for production)
            },
            {
                'IpProtocol': 'tcp',
                'FromPort': 80,
                'ToPort': 80,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}],  # Allow HTTP from anywhere
            }
        ]
    )
    print(f'Inbound rules set for security group {security_group_name}')
except Exception as e:
    print(f"Security group creation failed: {e}")

response = ec2.run_instances(
    ImageId='ami-0ebfd941bbafe70c6',
    InstanceType='t2.micro',
    MinCount=1,
    MaxCount=1,
    KeyName='my-project-keypair',
    SecurityGroupIds=[security_group_id]
)

instance_id = response['Instances'][0]['InstanceId']
print(f"Successfully launched EC2 instance with Instance ID: {instance_id}")

ec2_resource = aws_management_console.resource('ec2')
instance = ec2_resource.Instance(instance_id)

instance.wait_until_running()
instance.load()

public_ip = instance.public_ip_address
print(f'Instance is running with Public IP: {public_ip}')

private_key_file = "/Users/admin/code/python-learn/pokemon-api/my-project-keypair.pem" 

time.sleep(30)

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh_client.connect(public_ip, username="ec2-user", key_filename=private_key_file)

commands = [
    "sudo dnf -y update",
    "sudo dnf -y install python3.11 git",
    "cd /home/ec2-user",  
    "git clone https://github.com/omriza5/pokemon-api.git",  # Clone your GitHub repo
    "cd pokemon-api",  
    "python3.11 -m venv /home/ec2-user/pokemon-api/pokemon-env",
    "/home/ec2-user/pokemon-api/pokemon-env/bin/pip install --upgrade pip",  # Upgrade pip
    "source /home/ec2-user/pokemon-api/pokemon-env/bin/activate",  # Reactivate the environment after cloning
    "/home/ec2-user/pokemon-api/pokemon-env/bin/pip install -r /home/ec2-user/pokemon-api/requirements.txt"# Install necessary packages
]

for command in commands:
    stdin, stdout, stderr = ssh_client.exec_command(command)
    print(stdout.read().decode())
    print(stderr.read().decode())

ssh_client.close()