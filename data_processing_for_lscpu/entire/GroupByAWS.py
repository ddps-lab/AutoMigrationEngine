import pandas as pd

import copy

import sys
from pathlib import Path

# module 경로 추가
sys.path.append(str(Path(__file__).resolve().parent.joinpath('..', 'modules')))

import CPUFeatures_h
import GspreadUtils

CPU_FEATURES = CPUFeatures_h.all_CPU_features_simplification_by_lscpu()

df = GspreadUtils.read_gspread('all features')
df = df.loc[df['CloudProvider'] == 'AWS']

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
    instanceTypes = ', '.join(group['InstanceType'].tolist())

    eachFlag = group[CPU_FEATURES]
    row = eachFlag.iloc[0]
    row = row.to_frame().T
    row.insert(0, 'feature groups', instanceTypes)

    df_new = pd.concat([df_new, row], ignore_index=True)

GspreadUtils.write_gspread('groupby aws(all)', df_new)