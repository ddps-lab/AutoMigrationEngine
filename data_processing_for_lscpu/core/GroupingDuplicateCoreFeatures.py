import pandas as pd

import copy

import sys
from pathlib import Path

# module 경로 추가
sys.path.append(str(Path(__file__).resolve().parent.joinpath('..', 'modules')))

import CPUFeatures_h
import GspreadUtils

CPU_FEATURES = CPUFeatures_h.core_CPU_features_simplification_by_lscpu()

df = GspreadUtils.read_CPU_Feature_Visualization('core features')

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

GspreadUtils.write_CPU_Feature_Visualization('feature groups(core)', df_new)