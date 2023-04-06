# import library
import pandas as pd

import gspread as gs
from gspread_formatting import *

import re

# read google spread sheet(core features)
gc = gs.service_account(filename='../secure-outpost-380004-8d45b1504f3e.json')

sheet = gc.open('CPU Feature Visualization').worksheet('groupby aws(core)')
df = pd.DataFrame(sheet.get_all_records())

df = df['feature groups']

# df to list
groups = []

for i in range(len(df)):
    groups.append(df.iloc[i].split(', '))

sizelist = ['micro', 'small', 'medium', 'large', 'xlarge', '2xlarge', '4xlarge', '8xlarge', '16xlarge']
newgroup = []
newgroups = []
typelist = []
unduplicate = []

# select the smallest instance size
for group in groups:
    # extract to instance type ex) m5.large -> m5
    for instance in group:
        typelist.append(instance[:instance.index('.')])

    # delete duplicate
    unduplicate = list(set(typelist))

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
        # print(result)
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

        if instance in tempgroup:
            continue
    
        if len(instance_group_name) > 3 and instance_group_name[2] in {'a', 'i', 'g'}:
            if instance[:3] + instance[instance.index('.'):] not in tempgroup:
                tempgroup.append(instance)
        else:
            pattern = '^' + instance[:2] + '.'
            result = [instance for instance in tempgroup if re.match(pattern, instance)]
            if(len(result) == 0):
                tempgroup.append(instance)
    simplized_group.append(tempgroup)

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
        

print()
for group in final_experiment_set:
    print(group)

print(f'deleted_index : {deleted_index}')

# read google spread sheet(core features)
gc = gs.service_account(filename='../secure-outpost-380004-8d45b1504f3e.json')

sheet = gc.open('CPU Feature Visualization').worksheet('groupby aws(core)')
df = pd.DataFrame(sheet.get_all_records())

# Update with a simplified dataset.
for index in sorted(deleted_index, reverse = True):
    df = df.drop(index)

df = df.reset_index()
df.drop('index', axis=1, inplace=True)
for i in range(len(final_experiment_set)):
    df.at[i, 'feature groups'] = ', '.join(final_experiment_set[i])

# write google spread sheet1(core features)
gc = gs.service_account(filename='../secure-outpost-380004-8d45b1504f3e.json')

sheet = gc.open('CPU Feature Visualization').worksheet('simplized aws group(core)')
sheet.clear() # 이전 데이터 삭제
sheet.update([df.columns.values.tolist()] + df.values.tolist())

format_cell = cellFormat(
    verticalAlignment='MIDDLE', 
    wrapStrategy='OVERFLOW_CELL', 
    textFormat=textFormat(fontSize=10)
)

format_cell_range(sheet, '1:500', format_cell)