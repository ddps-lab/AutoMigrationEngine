import threading
import subprocess
import time
import datetime
import boto3

import ssh_scripts.playbook as playbook

ec2_client = boto3.client('ec2', region_name='us-west-2')
ec2_resource = boto3.resource('ec2', region_name='us-west-2')

GROUP_NUMBER = 1

start_time = datetime.datetime.now()

# create infrastructure by group 
with open(f'terraform.log', 'w') as f: # Created separately for reuse of some resources, such as VPCs
    p = subprocess.Popen(['terraform', 'apply', '-auto-approve', '-target', 'module.shuffle_instances'], cwd='infrastructure/Scenario1', stdout=f, stderr=f, encoding='utf-8')
    p.wait()
    p = subprocess.Popen(['terraform', 'apply', '-auto-approve'], cwd='infrastructure/Scenario1', stdout=f, stderr=f, encoding='utf-8')
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

subprocess.run(['rm', '-f', 'group*.log'])

# Execute an Ansible command to start the container migration test.
def worker(group_num):
    playbook.scenario1(str(group_num))

threads = []
for i in range(GROUP_NUMBER):
    thread = threading.Thread(target=worker, args=(i,))
    thread.start()
    threads.append(thread)
    time.sleep(3)

# wait for end of test
for thread in threads:
    thread.join()

# destroy infrastructure by group 
with open(f'terraform.log', 'a') as f:
    p = subprocess.Popen(['terraform', 'destroy', '-auto-approve'], cwd='infrastructure/Scenario1', stdout=f, stderr=f)
    p.wait()

end_time = datetime.datetime.now()

elapsed_time = end_time - start_time
total_seconds = elapsed_time.total_seconds()
print(f'total time : {total_seconds}')