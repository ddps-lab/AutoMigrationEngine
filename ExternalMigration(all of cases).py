import subprocess
import time
import datetime
import boto3
from tqdm import tqdm

import ssh_scripts.playbook as playbook

ec2_client = boto3.client('ec2', region_name='us-west-2')
ec2_resource = boto3.resource('ec2', region_name='us-west-2')

CREATE_GRPUP = [i for i in range(27)]

def createInfrastructure(cwd):
    # create infrastructure by group
    with open(f'terraform.log', 'w') as f:
        subprocess.run(['terraform', 'apply', '-auto-approve', '-target', 'module.read-instances', '-var',
                        f'group={CREATE_GRPUP}'], cwd=cwd, stdout=f, stderr=f, encoding='utf-8')
        subprocess.run(['terraform', 'apply', '-auto-approve', '-parallelism=30', '-var', f'group={CREATE_GRPUP}'],
                    cwd=cwd, stdout=f, stderr=f, encoding='utf-8')
        
    print('\nComplete infrastructure creation')
    print('wating 2.5 minute..')

    time.sleep(150)

    # checking instance status
    print('checking instance status...')
    while True:
        instances = ec2_client.describe_instances(Filters=[
            {
                'Name': 'tag:Name',
                'Values': ['migration-test_*']
            }
        ])

        all_running = True

        for reservation in instances['Reservations']:
            for instance in reservation['Instances']:
                instance_id = instance['InstanceId']
                instance_obj = ec2_resource.Instance(instance_id)

                instance_state = instance_obj.state['Name']

                if instance_state == 'terminated':
                    break

                status = ec2_client.describe_instance_status(
                    InstanceIds=[instance_id])
                if 'InstanceStatuses' not in status or status['InstanceStatuses'][0]['InstanceStatus']['Status'] != 'ok':
                    all_running = False
                    break

            if not all_running:
                break

        if all_running:
            break
        time.sleep(10)

    print('Pass all instance health checks')


def performTask():
    # Extract ISA set from workload
    playbook.funcTracking(CREATE_GRPUP)
    playbook.bytecodeTracking(CREATE_GRPUP)
    playbook.entire_scanning(CREATE_GRPUP)

    # Execute an Ansible command to start the checkpoint.
    playbook.externalMigrationDump(CREATE_GRPUP)

    # Execute an Ansible command to start the restore.
    with tqdm(total=len(CREATE_GRPUP), unit='Processing') as pbar:
        for i in CREATE_GRPUP:
            playbook.externalMigrationRestore(
                CREATE_GRPUP, CREATE_GRPUP[i])

            pbar.update(1)


def destroyInfrastructure(cwd):
    # destroy infrastructure by groups
    with open(f'terraform.log', 'a') as f:
        p = subprocess.Popen(['terraform', 'destroy', '-auto-approve', '-parallelism=30', '-var',
                              f'group={CREATE_GRPUP}'], cwd=cwd, stdout=f, stderr=f)
        p.wait()


if __name__ == '__main__':
    playbook.setWorkload()

    print('Select experiment option')
    print('1. On-Demand\n2. Spot-Instance')
    option = int(input()) - 1

    if option == 0:
        cwd = 'infrastructure/external_migration'
    elif option == 1:
        cwd = 'infrastructure/external_migration_on_spot'
    else:
        print('invalid option')
        exit()
    
    start_time = datetime.datetime.now()

    createInfrastructure(cwd)
    performTask()
    destroyInfrastructure(cwd)

    end_time = datetime.datetime.now()

    elapsed_time = end_time - start_time
    total_seconds = elapsed_time.total_seconds()
    print(f'total time : {total_seconds}')