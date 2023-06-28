import pandas as pd
from pathlib import Path

data_processing_for_lscpu_path = str(Path(__file__).resolve().parent.parent)

instances_for_rhel = ["t3a.large", "m5a.large", "m5a.2xlarge", "m5a.8xlarge", "c5a.large", "c6a.large", "t2.large", "m4.large", "h1.2xlarge", "x1e.xlarge", "r4.large", "i3.large", "c5a.24xlarge", "c6a.24xlarge", "c4.8xlarge", "h1.8xlarge", "h1.16xlarge", "x1e.8xlarge", "m4.16xlarge", "r4.8xlarge", "r4.16xlarge", "c6i.large", "t3.large", "c5.large", "m5n.large", "t3.2xlarge", "m5.large", "c6i.16xlarge", "c5d.9xlarge", "m5zn.6xlarge", "c5.9xlarge"]

df = pd.read_csv(f'{data_processing_for_lscpu_path}/utils/ec2 price(us-west-2, 23.05.24).csv', usecols=['Instance', 'RHEL On Demand cost', 'Linux On Demand cost'])

# 'RHEL On Demand cost' 컬럼에서 숫자 부분만 추출하여 float로 변환
df['RHEL On Demand cost'] = df['RHEL On Demand cost'].str.extract('(\d+\.\d+)').astype(float)

# 'Instance' 컬럼에서 instances_for_rhel에 있는 값들이 있는지를 찾아 그 행의 'RHEL On Demand cost' 값을 더함
total_sum = df[df['Instance'].isin(instances_for_rhel)]['RHEL On Demand cost'].sum()

print(f'RHEL hourly rate : {total_sum}')

# 'RHEL On Demand cost' 컬럼에서 숫자 부분만 추출하여 float로 변환
df['Linux On Demand cost'] = df['Linux On Demand cost'].str.extract('(\d+\.\d+)').astype(float)

# 'Instance' 컬럼에서 instances_for_rhel에 있는 값들이 있는지를 찾아 그 행의 'RHEL On Demand cost' 값을 더함
total_sum = df[df['Instance'].isin(instances_for_rhel)]['Linux On Demand cost'].sum()

print(f'linux hourly rate : {total_sum}')