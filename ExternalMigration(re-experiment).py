import subprocess
import time
import datetime
import boto3
from tqdm import tqdm

import csv
from pathlib import Path
csv_path = str(Path(__file__).resolve().parent) + '/infrastructure/CPU Feature Visualization - minimized aws group(all).csv'

import ssh_scripts.playbook as playbook

ec2_client = boto3.client('ec2', region_name='us-west-2')
ec2_resource = boto3.resource('ec2', region_name='us-west-2')
s3_client = boto3.client('s3')

bucket_name = 'migration-compatibility'
prefix = 'Migration-between-groups/rubin/'

def createInfrastructure(CREATE_GROUP):
    # create infrastructure by group
    with open(f'terraform.log', 'w') as f:
        subprocess.run(['terraform', 'apply', '-auto-approve', '-target', 'module.read-instances', '-var',
                        f'group={CREATE_GROUP}'], cwd='infrastructure/external_migration', stdout=f, stderr=f, encoding='utf-8')
        subprocess.run(['terraform', 'apply', '-auto-approve', '-var', f'group={CREATE_GROUP}'],
                       cwd='infrastructure/external_migration', stdout=f, stderr=f, encoding='utf-8')

    print('\nComplete infrastructure creation')
    print('wating 2 minute..')

    time.sleep(120)

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


def performTask(CREATE_GROUP):
    # Execute an Ansible command to start the checkpoint.
    playbook.externalMigrationDump(CREATE_GROUP, re_exp=True)

    # Execute an Ansible command to start the restore.
    playbook.externalMigrationRestore(CREATE_GROUP, 0, re_exp=True)


def destroyInfrastructure(CREATE_GROUP):
    # destroy infrastructure by groups
    with open(f'terraform.log', 'a') as f:
        p = subprocess.Popen(['terraform', 'destroy', '-auto-approve', '-var',
                              f'group={CREATE_GROUP}'], cwd='infrastructure/external_migration', stdout=f, stderr=f)
        p.wait()


def getReExp():
    instances = ["m5a.large", "m5a.2xlarge", "m5a.8xlarge", "c5a.large", "c6a.large", "m4.large", "h1.2xlarge", "x1e.xlarge", "r4.large", "i3.large", "c5a.24xlarge", "c6a.24xlarge", "c4.8xlarge", "h1.8xlarge", "h1.16xlarge", "x1e.8xlarge", "m4.16xlarge", "r4.8xlarge", "r4.16xlarge", "c6i.large", "c5.large", "m5n.large", "m5.large", "c6i.16xlarge", "c5d.9xlarge", "m5zn.6xlarge", "c5.9xlarge"]
    isExists = []
    re = []

    for src in instances:
        for dst in instances:
            if(src == dst):
                continue
            
            isExists.append(src + '_to_' + dst + '.csv')

    # 버킷 내의 모든 객체 조회
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    objects = response.get('Contents', [])

    # 객체 이름만 리스트로 저장
    file_names = [obj['Key'].split('/')[-1] for obj in objects]
    file_names = set(file_names)
    file_names.discard('')

    notExists = []
    for case in isExists:
        if case not in file_names:
            notExists.append(case)

    src = notExists[0].split('_')[0]
    dsts = []
    reExpCases = []
    for missingCase in notExists:
        if src != missingCase.split('_')[0]:
            reExpCases.append({src: dsts})

            dsts = []
            src = missingCase.split('_')[0]
            dsts.append(missingCase.split('_')[-1].split('.csv')[0])
            continue

        dsts.append(missingCase.split('_')[-1].split('.csv')[0])

    reExpCases.append({src: dsts})
    
    print(reExpCases)

    return reExpCases

def setCsv(cases):
    data = []
    column = ['feature groups']

    data.append(column)
    data.append(cases.keys())
    for values in cases.values():
        for value in values:
            data.append([value])

    # CSV 파일로 저장
    with open(csv_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

if __name__ == '__main__':
    playbook.setWorkload()
    start_time = datetime.datetime.now()
    
    reExpCases = getReExp()
    with tqdm(total=len(reExpCases), unit='Processing') as pbar:
        for reExpCase in reExpCases:
            setCsv(reExpCase)
            
            # values(dst instances) count + src instance count
            length = len(list(reExpCase.values())[0]) + 1
            CREATE_GROUP = [i for i in range(length)]

            createInfrastructure(CREATE_GROUP)
            performTask(CREATE_GROUP)
            destroyInfrastructure(CREATE_GROUP)
            pbar.update(1)

            time.sleep(5)

    end_time = datetime.datetime.now()

    elapsed_time = end_time - start_time
    total_seconds = elapsed_time.total_seconds()
    print(f'total time : {total_seconds}')