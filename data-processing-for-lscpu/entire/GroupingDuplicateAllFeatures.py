# import library
import pandas as pd

import gspread as gs
from gspread_formatting import *

import copy

# Intel
CPUID_1_EDX = ['ss']
CPUID_1_ECX = ['monitor', 'vmx', 'est', 'pcid', 'x2apic', 'tsc_deadline_timer']
CPUID_7_0_EBX = ['tsc_adjust', 'hle', 'erms', 'invpcid', 'rtm', 'mpx', 'avx512f', 'avx512dq', 'rdseed', 'adx', 'smap', 'avx512ifma', 'clflushopt', 'clwb', 'avx512cd', 'sha_ni', 'avx512bw', 'avx512vl']
CPUID_7_0_ECX = ['avx512vbmi', 'umip', 'pku', 'ospke', 'avx512_vbmi2', 'gfni', 'vaes', 'vpclmulqdq', 'avx512_vnni', 'avx512_bitalg', 'tme', 'avx512_vpopcntdq', 'rdpid']
CPUID_7_0_EDX = ['md_clear', 'flush_l1d', 'arch_capabilities', ]

# AMD
CPUID_8000_0001_EDX = ['mmxext', 'fxsr_opt', 'pdpe1gb']
CPUID_8000_0001_ECX = ['cmp_legacy', 'svm', 'cr8_legacy', 'sse4a', 'misalignsse', '3dnowprefetch', 'topoext', 'perfctr_core']
CPUID_8000_0008_EBX = ['clzero', 'xsaveerptr', 'rdpru', 'wbnoinvd']
# CPUID_8000_000a_EDX : AMD SVM(Secure Virtual Machine) features, 하드웨어 기반 가상화를 지원하는 기술
CPUID_8000_000a_EDX = ['npt', 'nrip_save','tsc_scale', 'vmcb_clean', 'flushbyasid', 'decodeassists', 'pausefilter', 'pfthreshold', 'v_vmsave_vmload']

# Linux
CPUID_LNX_Other = ['constant_tsc', 'arch_perfmon', 'xtopology', 'tsc_reliable', 'nonstop_tsc', 'amd_dcm', 'aperfmperf', 'tsc_known_freq']
CPUID_LNX_Auxiliary = ['cpuid_fault', 'invpcid_single', 'pti', 'ssbd', 'ibrs', 'ibpb', 'stibp', 'ibrs_enhanced', ]
CPUID_LNX_Virtualization = ['tpr_shadow', 'vnmi', 'ept', 'vpid', 'vmmcall', 'ept_ad']

# Extended state features
CPUID_D_1_EAX = ['xsavec', 'xgetbv1', 'xsaves']

# All
CPU_FEATURES = CPUID_1_EDX + CPUID_1_ECX + CPUID_7_0_EBX + CPUID_7_0_ECX + CPUID_7_0_EDX + CPUID_8000_0001_EDX + CPUID_8000_0001_ECX + CPUID_8000_0008_EBX + CPUID_8000_000a_EDX + CPUID_LNX_Other + CPUID_LNX_Auxiliary + CPUID_LNX_Virtualization + CPUID_D_1_EAX

# read google spread sheet(core features)
gc = gs.service_account(filename='../secure-outpost-380004-8d45b1504f3e.json')

sheet = gc.open('CPU Feature Visualization').worksheet('all features')
df = pd.DataFrame(sheet.get_all_records())

# Extract instance types with the same CPU features
columns = copy.deepcopy(CPU_FEATURES)
columns.insert(0, 'Flags')
columns.insert(0, 'feature groups')

groupList = []
flagList = []
grouped = df.groupby('Flags')
i = 0

df_new = pd.DataFrame(columns=columns)

for flags, group in grouped:
    i += 1
    # print(f"group{i}: {group['InstanceType'].tolist()}")
    instanceTypes = ', '.join(group['InstanceType'].tolist())

    eachFlag = group[CPU_FEATURES]
    row = eachFlag.iloc[0]
    row = row.to_frame().T
    row.insert(0, 'feature groups', instanceTypes)
    row.insert(1, 'Flags', flags)

    df_new = pd.concat([df_new, row], ignore_index=True)

# "Flags" column position change to last column
tempColumn = df_new.pop('Flags')
df_new.insert(len(df_new.columns), 'Flags', tempColumn)

# write google spread sheet
gc = gs.service_account(filename='../secure-outpost-380004-8d45b1504f3e.json')

sheet = gc.open('CPU Feature Visualization').worksheet('feature groups(all)')
sheet.clear() # 이전 데이터 삭제
sheet.update([df_new.columns.values.tolist()] + df_new.values.tolist())

format_cell = cellFormat(
    verticalAlignment='MIDDLE', 
    wrapStrategy='OVERFLOW_CELL', 
    textFormat=textFormat(fontSize=10)
)

format_cell_range(sheet, '1:500', format_cell)