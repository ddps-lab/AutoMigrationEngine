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

# 양방향 마이그레이션에 성공한 케이스에서 일치하지 않는 flag 추출
def bidirectionalMigration(bidirectionalMigrationSuccessList):
    selected_columns_list = []
    for i in range(len(bidirectionalMigrationSuccessList)):
        groups = df.loc[bidirectionalMigrationSuccessList[i]]

        # 특정 행(0,1,2)에서 값이 같지 않은 열을 탐색.
        not_equal_columns = groups.loc[bidirectionalMigrationSuccessList[i]].nunique() != 1
        # 값이 같지 않은 열을 선택.
        different_columns = groups.loc[:, not_equal_columns]

        columns = different_columns.columns.to_list()
        columns.remove('feature groups')
        selected_columns_list.append(columns)

    flattened_list = [item for sublist in selected_columns_list for item in sublist]
    # 중복 제거.
    unique_items = set(flattened_list)
    unique_list = list(unique_items)
    return unique_list


# 단방향 마이그레이션에 성공한 케이스에서 src에만 존재하는 flag 추출
# dst list에서 한 번이라도 존재하지 않으면 해당 flag는 호환에 영향이 없는 것으로 간주함.
def unidirectionalMigration(unidirectionalMigrationSuccessList):
    selected_columns_list = []
    for i in range(len(unidirectionalMigrationSuccessList)):
        groups = df.loc[unidirectionalMigrationSuccessList[i]]

        selected_columns = groups.loc[:, (groups.iloc[0] == 1) & (groups.iloc[1:].isin([0]).any())]
        selected_columns_list.append(selected_columns.columns.tolist())
    
    flattened_list = [item for sublist in selected_columns_list for item in sublist]
    # 중복 제거.
    unique_items = set(flattened_list)
    unique_list = list(unique_items)

    return(unique_list)

bidirectionalMigrationSuccessList = CollectGroupNumbers.CollectGroupNumbersForInstances("BidirectionalMigrationSuccessCases.csv", True)
unidirectionalMigrationSuccessList = CollectGroupNumbers.CollectGroupNumbersForInstances("UnidirectionalMigrationSuccessCases.csv", True)

no_effect_flags = []
no_effect_flags_by_bidirectional = bidirectionalMigration(bidirectionalMigrationSuccessList)
no_effect_flags_by_unidirectional = unidirectionalMigration(unidirectionalMigrationSuccessList)
print(f"Number of no effect flags by bidirectional are {len(no_effect_flags_by_bidirectional)}")
print(f"No effect flags by bidirectional are \n{no_effect_flags_by_bidirectional}")
print(f"\nNumber of no effect flags by unidirectional are {len(no_effect_flags_by_unidirectional)}")
print(f"No effect flags by unidirectional are \n{no_effect_flags_by_unidirectional}")
no_effect_flags = no_effect_flags_by_bidirectional + no_effect_flags_by_unidirectional

no_effect_flags = list(set(no_effect_flags))
print(f"\nNumber of no effect flags are {len(no_effect_flags)}")
print(f"No effect flags by are \n{no_effect_flags}")

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
# 컬럼 제거
df_new = df_new.drop(columns_to_remove, axis=1)

print(df_new)
GspreadUtils.write_AWS_migration_compatibility("Remove no effect flags 1", df_new)