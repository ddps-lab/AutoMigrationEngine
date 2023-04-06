# import library
import pandas as pd

import gspread as gs
from gspread_formatting import *

# Define core CPU features of CRIU(simplification)
# Exclude features that exist or do not exist in all instances type

# Intel
CPUID_1_ECX = ['pclmulqdq', 'monitor', 'movbe', 'aes', 'xsave', 'avx', 'f16c', 'rdrand']
CPUID_7_0_EBX = ['fsgsbase', 'bmi1', 'hle', 'avx2', 'bmi2', 'erms', 'rtm', 'mpx', 'avx512f', 'avx512dq', 'rdseed', 'adx', 'clflushopt', 'avx512cd', 'sha_ni', 'avx512bw', 'avx512vl']
CPUID_7_0_ECX = ['avx512vbmi', 'avx512_vbmi2', 'gfni', 'vaes', 'vpclmulqdq', 'avx512_vnni', 'avx512_bitalg', 'tme', 'avx512_vpopcntdq', 'rdpid']

# AMD
CPUID_8000_0001_EDX = [ 'mmxext', 'rdtscp']
CPUID_8000_0001_ECX = ['abm', 'sse4a', 'misalignsse', '3dnowprefetch']
CPUID_8000_0008_EBX = ['clzero']

# Extended state features
CPUID_D_1_EAX = ['xsaveopt', 'xsavec', 'xgetbv1']

# All
CPU_FEATURES = CPUID_1_ECX + CPUID_7_0_EBX + CPUID_7_0_ECX + CPUID_8000_0001_EDX + CPUID_8000_0001_ECX + CPUID_8000_0008_EBX + CPUID_D_1_EAX

# csv read & add header
df = pd.read_csv('../lscpu/CPU(s) visualization.csv', usecols=['CloudProvider', 'Architecture', 'InstanceType', 'Model name', 'Flags'], index_col='InstanceType')
df = df.reset_index()
df = df.loc[df['Architecture'] == 'x86_64']

df.drop('Architecture', axis=1, inplace=True)
df = df[['InstanceType', 'CloudProvider', 'Model name', 'Flags']]

df = pd.concat([df, pd.DataFrame(columns=CPU_FEATURES)], axis=1)

# 지원하지 않는 인스턴스 제거
unsupported = ['m2.xlarge', 'm2.2xlarge', 'm2.4xlarge', 'm1.large', 'm1.xlarge', 'c3.large', 'r3.large', 'm3.large', 'r3.xlarge', 'c3.xlarge', 'm3.xlarge', 'r3.2xlarge', 'm3.2xlarge', 'c3.2xlarge', 'r3.4xlarge', 'c3.4xlarge', 'r3.8xlarge', 'c3.8xlarge']

for instance in unsupported:
    df = df.drop(df[df['InstanceType'] == instance].index)

# Extract each flag
for i in range(len(df)):
    columnIndex = df.columns.get_loc('Flags')
    flags = df.iloc[i, columnIndex]
    flagList = flags.split(' ')

    for j in range(len(CPU_FEATURES)):
        isExist = CPU_FEATURES[j] in flagList
        columnIndex += 1
        if(isExist):
            df.iat[i, columnIndex] = 1
        else:
            df.iat[i, columnIndex] = 0

df.reset_index(drop=True, inplace=True)

# "Flags" column position change to last column
tempColumn = df.pop('Flags')
df.insert(len(df.columns), 'Flags', tempColumn)

# write google spread sheet1(core features)
gc = gs.service_account(filename='../secure-outpost-380004-8d45b1504f3e.json')

sheet = gc.open('CPU Feature Visualization').worksheet('core features')
sheet.clear() # 이전 데이터 삭제
sheet.update([df.columns.values.tolist()] + df.values.tolist())

format_cell = cellFormat(
    verticalAlignment='MIDDLE', 
    wrapStrategy='OVERFLOW_CELL', 
    textFormat=textFormat(fontSize=10)
)

format_cell_range(sheet, '1:500', format_cell)

# Extract features that exist or do not exist on all instances
zero_cols = df.columns[df.eq(0).all(axis=0)].tolist()
print(zero_cols)
print(f"The number of features not exists in all instances : {len(zero_cols)}\n")

one_cols = df.columns[df.eq(1).all(axis=0)].tolist()

print(one_cols)
print(f"The number of features exists in all instances : {len(one_cols)}\n")

# InstanceType, CloudProvider, Model Name, Flags 제외 총 칼럼 개수 = 적어도 1개 이상 사용되는 CPU features 개수
print(f"Number of CPU features used at least one : {len(df.columns) - 4}")