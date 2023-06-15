import sys
from pathlib import Path
import pandas as pd
import copy

# module 경로 추가
sys.path.append(str(Path(__file__).resolve().parent.joinpath('modules')))

import GspreadUtils
import CollectGroupNumbers
import CPUFeatures_h

df = GspreadUtils.read_AWS_migration_compatibility('Group all features with the same instances')
groups = df['feature groups'].to_list()

# 마이그레이션에 성공한 케이스에서 src에만 존재하는 flag 추출
# dst list에서 한 번이라도 존재하지 않으면 해당 flag는 호환에 영향이 없는 것으로 간주함.
def allSuccessMigration(MigrationSuccessList):
    selected_columns_list = []
    for i in range(len(MigrationSuccessList)):
        groups = df.loc[MigrationSuccessList[i]]

        selected_columns = groups.loc[:, (groups.iloc[0] == 1) & (groups.iloc[1:].isin([0]).any())]
        selected_columns_list.append(selected_columns.columns.tolist())
    
    flattened_list = [item for sublist in selected_columns_list for item in sublist]
    # 중복 제거.
    unique_items = set(flattened_list)
    unique_list = list(unique_items)

    # flag 차이가 있음에도 마이그레이션에 성공, 실패하는 경우가 있음. 실패하는 케이스가 있기 때문에 영향이 있음으로 간주하고 해당 flag를 그룹화에 포함.
    unique_list.remove("rtm")
    unique_list.remove("hle")

    return(unique_list)

migrationSuccessList = CollectGroupNumbers.CollectGroupNumbersForInstances("MigrationSuccessCases.csv", True) 

no_effect_flags = []
no_effect_flags_by_all = allSuccessMigration(migrationSuccessList)
print(f"Number of no effect flags by all cases are {len(no_effect_flags_by_all)}")
print(f"No effect flags by all cases are \n{no_effect_flags_by_all}")
no_effect_flags = no_effect_flags_by_all

df = df.drop(no_effect_flags, axis=1)
CPU_FEATURES = CPUFeatures_h.all_CPU_features_simplification_by_lscpu()
CPU_FEATURES = [x for x in CPU_FEATURES if x not in no_effect_flags]

# Extract instance types with the same CPU features
columns = copy.deepcopy(CPU_FEATURES)
columns.insert(0, 'feature groups')

groupList = []
flagList = []
grouped = df.groupby(CPU_FEATURES)

df_new = pd.DataFrame(columns=columns)

for features, group in grouped:
    instanceTypes = ', '.join(group['feature groups'].tolist())

    eachFlag = group[CPU_FEATURES]
    row = eachFlag.iloc[0]
    row = row.to_frame().T
    row.insert(0, 'feature groups', instanceTypes)

    df_new = pd.concat([df_new, row], ignore_index=True)

# 모든 row의 값이 동일한 컬럼 식별
columns_to_remove = df_new.columns[df.nunique() == 1]
print(f'\nremoving columns are.. \n{columns_to_remove.to_list()}')
# 컬럼 제거
df_new = df_new.drop(columns_to_remove, axis=1)

GspreadUtils.write_AWS_migration_compatibility("Remove no effect flags 1", df_new)