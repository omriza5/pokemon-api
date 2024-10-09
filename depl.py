import boto3
import paramiko
import os

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

private_key_file = "/Users/admin/Desktop/my-project-keypair.pem" 

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh_client.connect(public_ip, username="ec2-user", key_filename=private_key_file)


sftp = ssh_client.open_sftp()

local_project_path = "/Users/admin/code/python-learn/pokemon-project"
remote_project_path = "/home/ec2-user/pokemon/"

try:
    sftp.mkdir(remote_project_path)
except IOError:
    print("Remote directory already exists")

# Upload files (recursively if you want to upload an entire directory)
for filename in os.listdir(local_project_path):
    if filename.endswith('.py'):    
        local_file = os.path.join(local_project_path, filename)
        remote_file = os.path.join(remote_project_path, filename)
        sftp.put(local_file, remote_file)
        print(f"Uploaded {local_file} to {remote_file}")

# Close the SFTP session
sftp.close()

# Optionally, you can run a script or command on the EC2 instance
stdin, stdout, stderr = ssh_client.exec_command("ls -l /home/ec2-user/pokemon/")
print(stdout.read().decode())

commands = [
    "sudo dnf -y update",
    "sudo dnf -y install python3.11",
    "python3.11 -m venv /home/ec2-user/pokemon/pokemon-env",
    "source /home/ec2-user/pokemon/pokemon-env/bin/activate",  # Activate the environment
    "/home/ec2-user/pokemon/pokemon-env/bin/pip install --upgrade pip",  # Upgrade pip
    "/home/ec2-user/pokemon/pokemon-env/bin/pip install requests termcolor"  # Install necessary packages
]

for command in commands:
    stdin, stdout, stderr = ssh_client.exec_command(command)
    print(stdout.read().decode())
    print(stderr.read().decode())

ssh_client.close()