# import library
import pandas as pd

import gspread as gs
from gspread_formatting import *

import copy

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

# read google spread sheet(core features)
gc = gs.service_account(filename='../secure-outpost-380004-8d45b1504f3e.json')

sheet = gc.open('CPU Feature Visualization').worksheet('core features')
df = pd.DataFrame(sheet.get_all_records())

# Extract instance types with the same CPU features
columns = copy.deepcopy(CPU_FEATURES)
columns.insert(0, 'feature groups')

groupList = []
flagList = []
grouped = df.groupby(CPU_FEATURES)
i = 0

df_new = pd.DataFrame(columns=columns)

for features, group in grouped:
    i += 1
    # print(f"group{i}: {group['InstanceType'].tolist()}")
    instanceTypes = ', '.join(group['InstanceType'].tolist())

    eachFlag = group[CPU_FEATURES]
    row = eachFlag.iloc[0]
    row = row.to_frame().T
    row.insert(0, 'feature groups', instanceTypes)

    df_new = pd.concat([df_new, row], ignore_index=True)

# write google spread sheet
gc = gs.service_account(filename='../secure-outpost-380004-8d45b1504f3e.json')

sheet = gc.open('CPU Feature Visualization').worksheet('feature groups(core)')
sheet.clear() # 이전 데이터 삭제
sheet.update([df_new.columns.values.tolist()] + df_new.values.tolist())

format_cell = cellFormat(
    verticalAlignment='MIDDLE', 
    wrapStrategy='OVERFLOW_CELL', 
    textFormat=textFormat(fontSize=10)
)

format_cell_range(sheet, '1:500', format_cell)