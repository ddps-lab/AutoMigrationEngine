import sys
from pathlib import Path

# module 경로 추가
sys.path.append(str(Path(__file__).resolve().parent.joinpath('..', 'modules')))

import ReadCsv
import CPUFeatures_h
import GspreadUtils

CPU_FEATURES = CPUFeatures_h.all_CPU_features_simplification_by_lscpu()

df = ReadCsv.read_csv(CPU_FEATURES)

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

GspreadUtils.write_gspread('all features', df)

# Extract features that exist or do not exist on all instances
zero_cols = df.columns[df.eq(0).all(axis=0)].tolist()
print(zero_cols)
print(f"The number of features not exists in all instances : {len(zero_cols)}\n")

one_cols = df.columns[df.eq(1).all(axis=0)].tolist()

print(one_cols)
print(f"The number of features exists in all instances : {len(one_cols)}\n")

# InstanceType, CloudProvider, Model Name, Flags 제외 총 칼럼 개수 = 적어도 1개 이상 사용되는 CPU features 개수
print(f"Number of CPU features used at least one : {len(df.columns) - 4}")