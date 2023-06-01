import sys
from pathlib import Path

# module 경로 추가
sys.path.append(str(Path(__file__).resolve().parent.joinpath('modules')))

import GspreadUtils

df = GspreadUtils.read_AWS_migration_compatibility('Group all features with the same instances')

bidirectionalMigrationSuccessList = [3,4]
unidirectionalMigrationSuccessList = [[0, 1, 2, 3, 4, 5, 6], [3, 4]] # src = [][0], dst = [][1:]

# 양방향 마이그레이션에 성공한 케이스에서 일치하지 않는 flag 추출
def bidirectionalMigration(bidirectionalMigrationSuccessList):
    groups = df.loc[bidirectionalMigrationSuccessList]

    # 특정 행(0,1,2)에서 값이 같지 않은 열을 탐색.
    not_equal_columns = groups.loc[bidirectionalMigrationSuccessList].nunique() != 1
    # 값이 같지 않은 열을 선택.
    different_columns = groups.loc[:, not_equal_columns]

    print(different_columns)

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

    print(unique_list)

bidirectionalMigration(bidirectionalMigrationSuccessList)
unidirectionalMigration(unidirectionalMigrationSuccessList)