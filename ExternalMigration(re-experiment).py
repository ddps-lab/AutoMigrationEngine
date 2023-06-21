import ssh_scripts.playbook as playbook
import subprocess
import time
import datetime
import boto3

from tqdm import tqdm
from pprint import pprint

import sys
from pathlib import Path

# module 경로 추가
sys.path.append(str(Path(__file__).resolve().parent.joinpath(
    'data_processing_for_lscpu/modules')))

import CollectGroupNumbers

ec2_client = boto3.client('ec2', region_name='us-west-2')
ec2_resource = boto3.resource('ec2', region_name='us-west-2')


def createInfrastructure(i):
    with open(f'terraform.log', 'w') as f:
        subprocess.run(['terraform', 'apply', '-auto-approve', '-target', 'module.read-instances', '-var', f'group={ExprimentGroups[i]}'],
                       cwd='infrastructure/external_migration', stdout=f, stderr=f, encoding='utf-8')
        subprocess.run(['terraform', 'apply', '-auto-approve', '-var', f'group={ExprimentGroups[i]}'],
                       cwd='infrastructure/external_migration', stdout=f, stderr=f, encoding='utf-8')

    time.sleep(100)
    # checking instance status
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


def performTask(ExprimentGroups, workload):
    with tqdm(total=len(ExprimentGroups), unit='Processing') as pbar:
        for i in range(len(ExprimentGroups)):
            createInfrastructure(i)

            # Execute an Ansible command to start the checkpoint.
            playbook.externalMigrationDump([ExprimentGroups[i][0]], workload)

            # Execute an Ansible command to start the restore.
            playbook.externalMigrationRestore(
                ExprimentGroups[i], ExprimentGroups[i][0], True, workload)

            destroyInfrastructure(i)

            pbar.update(1)


def destroyInfrastructure(i):
    with open(f'terraform.log', 'a') as f:
        p = subprocess.Popen(['terraform', 'destroy', '-auto-approve', '-var',
                             f'group={ExprimentGroups[i]}'], cwd='infrastructure/external_migration', stdout=f, stderr=f)
        p.wait()


if __name__ == '__main__':
    workload = playbook.setWorkload()

    ExprimentGroups = CollectGroupNumbers.CollectGroupNumbersForInstances(
        "ExperimentFailureCases.csv", False)
    total_count = sum(len(sub_lst) for sub_lst in ExprimentGroups)
    source_count = len(ExprimentGroups)
    print(
        f"There are {source_count} source instances and {total_count - source_count} migrations to be performed..")
    pprint(ExprimentGroups)

    start_time = datetime.datetime.now()
    performTask(ExprimentGroups, workload)
    end_time = datetime.datetime.now()

    elapsed_time = end_time - start_time
    total_seconds = elapsed_time.total_seconds()
    print(f'total time : {total_seconds}')
