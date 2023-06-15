import sys
from pathlib import Path

import itertools

from pprint import pprint

# module 경로 추가
sys.path.append(str(Path(__file__).resolve().parent.joinpath('modules')))

import GspreadUtils
import Transferable
import ReadCsv

original = GspreadUtils.read_AWS_migration_compatibility('Group all features with the same instances')
revision = GspreadUtils.read_AWS_migration_compatibility('Remove no effect flags 1')
flags = revision.columns[1:].to_list()
groups = []

# DataFrame의 각 row별로 값 추출
for index, row in revision.iterrows():
    feature_group = row['feature groups']
    groups.append(feature_group.split(', '))

# 최종 그룹의 flag가 기존 데이터셋과 일치하는가?
def FlagIntegrityCheck():
    for i in range(len(revision)):
        revision_flags = revision.loc[revision['feature groups'] == ', '.join(groups[i]), flags]
        revision_flags.reset_index(drop=True, inplace=True)
        
        for j in range(len(groups[i])):
            original_flags = original.loc[original['feature groups'] == groups[i][j], flags]
            original_flags.reset_index(drop=True, inplace=True)

            is_matching = original_flags.equals(revision_flags)

            if not is_matching:
                print(groups[i][j])

# 최종 그룹 내에서 모두 마이그레이션에 성공하였는가?
def GroupInternalMigrationCheck():
    success = ReadCsv.read_exp_success_cases("MigrationSuccessCases.csv")
    success = success.values.tolist()
    success.sort()

    combinations = []
    for i in range(len(groups)):
        combinations += list(itertools.permutations(groups[i], 2))
    # to list
    combinations = [[item[0], item[1]] for item in combinations]
    combinations.sort()

    for i in range(len(combinations)):
        if combinations[i] not in success:
            print(combinations[i])

def GroupExternalMigrationCheck():
    success = ReadCsv.read_exp_success_cases("MigrationSuccessCases.csv")
    success = success.values.tolist()
    success.sort()

    flags = revision.drop('feature groups', axis=1)
    transferable_matrix = Transferable.tranferable_check(4, flags, matrix_only=True)
    Transferable.Digraph(4, flags)

    combinations = []
    for i in range(len(transferable_matrix)):
        for j in range(len(transferable_matrix[0])):
            # 마이그레이션 가능하다고 판단되는 그룹으로의 조합을 만들어 실험 결과와 비교
            if (i == j or not transferable_matrix[i][j]):
                continue
            combinations += list(itertools.product(groups[i], groups[j]))

    combinations = [[item[0], item[1]] for item in combinations]
    combinations.sort()

    for combination in combinations:
        if combination not in success:
            print(combination)

GroupInternalMigrationCheck()
GroupExternalMigrationCheck()