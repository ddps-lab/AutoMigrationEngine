import subprocess
import time
import datetime
import boto3

ec2_client = boto3.client('ec2', region_name='us-west-2')
ec2_resource = boto3.resource('ec2', region_name='us-west-2')

GROUP_NUMBER = 10

start_time = datetime.datetime.now()

# initialize workspace
for i in range(GROUP_NUMBER):
    subprocess.run(['terraform', 'workspace', 'delete', 'group' + str(i)], cwd='terraform')
    time.sleep(1)
    subprocess.run(['terraform', 'workspace', 'new', 'group' + str(i)], cwd='terraform')

# create infrastructure by group 
subprocess.run(['terraform', 'workspace', 'select', 'group0'], cwd='terraform')
time.sleep(1)
with open(f'group0.log', 'w') as f: # Created separately for reuse of some resources, such as VPCs
    p = subprocess.Popen(['terraform', 'apply', '-auto-approve', '-lock=false', '-var=group_number=0'], cwd='terraform', stdout=f, stderr=f)

p.wait()

processes = []
for i in range(1, GROUP_NUMBER):
    subprocess.run(['terraform', 'workspace', 'select', 'group' + str(i)], cwd='terraform')
    time.sleep(5)
    with open(f'group{i}.log', 'w') as f:
        processes.append(subprocess.Popen(['terraform', 'apply', '-auto-approve', '-lock=false', '-var=group_number=' + str(i)], cwd='terraform', stdout=f, stderr=f))
    time.sleep(5)

# wait for the infrastructure to be created
for p in processes:
    p.wait()

print('\nComplete infrastructure creation')

# checking instance status
while True:
    print('checking instance status...')
    instances = ec2_client.describe_instances(Filters=[
        {
            'Name': 'tag:Name',
            'Values': ['container-migration-test_*']
        }
    ])

    all_running = True

    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            instance_obj = ec2_resource.Instance(instance_id)

            instance_state = instance_obj.state['Name']
            
            if instance_state == 'terminated':
                print(f"Instance {instance_id} is terminated")
                break

            status = ec2_client.describe_instance_status(InstanceIds=[instance_id])
            if 'InstanceStatuses' not in status or status['InstanceStatuses'][0]['InstanceStatus']['Status'] != 'ok':
                print(f"Instance {instance_id} is not yet ready. Waiting 5 seconds...")
                all_running = False
                break

        if not all_running:
            break
    
    if all_running:
        print('All instances are running')
        break    
    time.sleep(10)
    
print('Pass all instance health checks')

# Execute an Ansible command to start the container migration test.
processes = []
for i in range(GROUP_NUMBER):
    with open(f'group{i}.log', 'a') as f:
        processes.append(subprocess.Popen(['python3', 'playbook.py', str(i)], cwd='ansible', stdout=f, stderr=f))
    time.sleep(10)

# wait for end of test
for p in processes:
    p.wait()

# destroy infrastructure by group 
processes = []
for i in range(GROUP_NUMBER):
    subprocess.run(['terraform', 'workspace', 'select', 'group' + str(i)], cwd='terraform')
    time.sleep(5)
    with open(f'group{i}.log', 'a') as f:
        processes.append(subprocess.Popen(['terraform', 'destroy', '-auto-approve', '-lock=false', '-var=group_number=' + str(i)], cwd='terraform', stdout=f, stderr=f))
    time.sleep(5)

# wait for the infrastructure to be deleted
for p in processes:
    p.wait()

end_time = datetime.datetime.now()

elapsed_time = end_time - start_time
total_seconds = elapsed_time.total_seconds()
print(f'total time : {total_seconds}')