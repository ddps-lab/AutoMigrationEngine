import boto3

import sys
from pathlib import Path

# module 경로 추가
sys.path.append(str(Path(__file__).resolve().parent.joinpath('modules')))

import GspreadUtils

# EC2 클라이언트 생성
ec2_client = boto3.client('ec2', region_name = 'us-west-2')

createable_x86_64_instances = []
createable_arm64_instances = []
unsupported_instances = []
next_token = None

while True:
    # 인스턴스 타입 정보 가져오기
    if next_token:
        response = ec2_client.describe_instance_types(NextToken=next_token)
    else:
        response = ec2_client.describe_instance_types()

    # 현재 페이지의 인스턴스 유형 이름 추가
    for instance_type in response['InstanceTypes']:
        if instance_type['CurrentGeneration']:
            architectures = instance_type['ProcessorInfo']['SupportedArchitectures']
            if 'x86_64' in architectures:
                createable_x86_64_instances.append(instance_type['InstanceType'])
            elif 'arm64' in architectures:
                createable_arm64_instances.append(instance_type['InstanceType'])
        else:
            unsupported_instances.append(instance_type['InstanceType'])

    # 다음 페이지 토큰 설정
    next_token = response.get('NextToken', None)

    # 다음 페이지 토큰이 없으면 종료
    if not next_token:
        break

print(f"Number of all instances : {len(createable_x86_64_instances) + len(createable_arm64_instances) + len(unsupported_instances)}")
print(f"Number of createable x86_64 instances : {len(createable_x86_64_instances)}")
print(f"Number of createable arm64 instances : {len(createable_arm64_instances)}")
print(f"Number of unsupported instances : {len(unsupported_instances)}")

df = GspreadUtils.read_CPU_Feature_Visualization('groupby aws(all)')
featureGroups = df['feature groups'].tolist()
groups = []

for i in range(len(featureGroups)):
    groups.append(featureGroups[i].split(", "))

unsupported = []
not_exist_x86_64 = []
not_exist_arm64 = []

for group in groups:
    for instance in group:
        if instance in unsupported_instances:
            unsupported.append(instance)

for instance_type, instance_list in [("x86_64", createable_x86_64_instances), ("arm64", createable_arm64_instances)]:
    for instance in instance_list:
        if not any(instance in group for group in groups):
            if instance_type == "x86_64":
                not_exist_x86_64.append(instance)
            else:
                not_exist_arm64.append(instance)

print(unsupported)
print(f'Number of unsupported instances extracted from the dataset: {len(unsupported)}\n')
print(not_exist_x86_64)
print(f'Number of non-existent x86_64 instances extracted from the dataset: {len(not_exist_x86_64)}\n')
print(not_exist_arm64)
print(f'Number of non-existent arm64 instances extracted from the dataset: {len(not_exist_arm64)}\n')
