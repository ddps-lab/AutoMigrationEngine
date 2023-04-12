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

GspreadUtils.write_gspread('feature groups(all)', df_new)