import re

import sys
from pathlib import Path

# module 경로 추가
sys.path.append(str(Path(__file__).resolve().parent.joinpath('..', 'modules')))

import GspreadUtils

df = GspreadUtils.read_gspread('groupby aws(all)')
df = df['feature groups']

# df to list
groups = []

for i in range(len(df)):
    groups.append(df.iloc[i].split(', '))

sizelist = ['nano', 'micro', 'small', 'medium', 'large', 'xlarge', '2xlarge', '3xlarge', '4xlarge', '6xlarge', '8xlarge', '9xlarge', 
            '10xlarge', '12xlarge', '16xlarge', '18xlarge', '24xlarge', '32xlarge', '48xlarge']
acceleratedType = ['p4', 'p3', 'p3dn', 'p2', 'dl1', 'trn1', 'inf2', 'inf1', 'g5', 'g5g', 'g4dn', 'g4ad', 'g3', 'g3s', 'f1', 'vt1']
newgroup = []
newgroups = []
typelist = []
unduplicate = []

# select the smallest instance size
for group in groups:
    # extract to instance type ex) m5.large -> m5
    for instance in group:
        # 최대 48xlarge까지만 간소화 대상으로 포함.
        if instance[instance.index('.') + 1:] in sizelist:
            typelist.append(instance[:instance.index('.')])

    # delete duplicate
    unduplicate = list(set(typelist))

    # delete accelerated instances
    for i in reversed(range(len(unduplicate))):
        if(unduplicate[i] in acceleratedType):
            unduplicate.pop(i)

    # extract to smallest instance for unduplicate typelist
    for i in range(len(unduplicate)):
        pattern = '^' + unduplicate[i] + '\.'
        result = [instance for instance in group if re.match(pattern, instance)]

        smallest_size = len(sizelist) - 1
        smallest = 0
        for j in range(len(result)):
            size = result[j][result[j].index('.') + 1:]

            if sizelist.index(size) < smallest_size:
                smallest_size = sizelist.index(size)
                smallest = j
        newgroup.append(result[smallest])
    newgroups.append(newgroup)
    newgroup = []
    typelist = []
    unduplicate = []

simplized_group = []

# Simplify instance types by processor type
for group in newgroups:
    tempgroup = []
    for instance in group:
        instance_group_name = instance[:instance.index('.')]

        if len(instance_group_name) == 2:
            tempgroup.append(instance)
            continue

        if len(instance_group_name) == 3 and instance_group_name[2] in {'a', 'i', 'g'}:
            tempgroup.append(instance)
            continue
    
    for instance in group:
        instance_group_name = instance[:instance.index('.')]
        count = 0

        if instance in tempgroup:
            continue
        
        if len(instance_group_name) > 3 and instance_group_name[2] in {'a', 'i', 'g'}:
            if instance[:3] + instance[instance.index('.'):] not in tempgroup:
                # tempgroup(간소화 전 임시로 저장하는 인스턴스 그룹)의 모든 원소의 타입 분류군(t3a? t3i?)을 조회 및 타입, 길이, 사이즈 비교
                for temp in tempgroup:
                    if instance[:3] in temp[:3]:
                        type1 = instance[:instance.index('.')]
                        type2 = temp[:temp.index('.')]
                        size1 = instance[instance.index('.') + 1:]
                        size2 = temp[temp.index('.') + 1:]

                        # tempgroup에 있는 인스턴스 보다 사이즈가 작은 경우 해당 인스턴스 선택
                        # x2iedn.large, x2idn.2xlarge가 있다면 x2iedn.large 선택
                        if sizelist.index(size1) < sizelist.index(size2):
                            tempgroup[tempgroup.index(temp)] = instance
                            break
                        # tempgroup에 있는 인스턴스와 사이즈가 같은 경우 타입의 길이가 짧은 타입 선택
                        # x2iedn.large, x2idn.large가 있다면 x2idn.large 선택
                        elif sizelist.index(size1) == sizelist.index(size2):
                            if len(type1) < len(type2):
                                tempgroup[tempgroup.index(temp)] = instance
                                break
                    else:
                        count += 1
                if count == len(tempgroup):
                    tempgroup.append(instance)
        else:
            pattern = '^' + instance[:2] + '.'
            result = ''.join([instance for instance in tempgroup if re.match(pattern, instance)])
            if(len(result) == 0):
                tempgroup.append(instance)
            else:
                type1 = instance[:instance.index('.')]
                type2 = result[:result.index('.')]
                size1 = instance[instance.index('.') + 1:]
                size2 = result[result.index('.') + 1:]

                # tempgroup에 있는 인스턴스 보다 사이즈가 작은 경우 해당 인스턴스 선택
                # r5dn.large, r5n.2xlarge가 있다면 r5dn.large 선택
                if sizelist.index(size1) < sizelist.index(size2):
                    tempgroup[tempgroup.index(result)] = instance
                # tempgroup에 있는 인스턴스와 사이즈가 같은 경우 타입의 길이가 짧은 타입 선택
                # r5dn.large, r5n.large가 있다면 r5n.large 선택
                elif sizelist.index(size1) == sizelist.index(size2):
                    if len(type1) < len(type2):
                        tempgroup[tempgroup.index(result)] = instance
    simplized_group.append(tempgroup)
    
df = GspreadUtils.read_gspread('groupby aws(all)')

# 단일 인스턴스만 남은 그룹 제거
if(False):
    final_experiment_set = []
    deleted_index = []
    # Remove a group with 1 instance
    i = 0
    for sublist in simplized_group:
        if len(sublist) > 1:
            final_experiment_set.append(sublist)
        else:
            deleted_index.append(i)
        i += 1
            
    # Update with a simplified dataset.
    for index in sorted(deleted_index, reverse = True):
        df = df.drop(index)

    df = df.reset_index()
    df.drop('index', axis=1, inplace=True)
    for i in range(len(final_experiment_set)):
        df.at[i, 'feature groups'] = ', '.join(final_experiment_set[i])
    
    GspreadUtils.write_gspread('simplized aws group(all, exclude single-element groups)', df)
else:
    for i in reversed(range(len(simplized_group))):
        if len(simplized_group[i]) < 1:
            df = df.drop(i)
            continue
        df.at[i, 'feature groups'] = ', '.join(simplized_group[i])

    GspreadUtils.write_gspread('simplized aws group(all)', df)