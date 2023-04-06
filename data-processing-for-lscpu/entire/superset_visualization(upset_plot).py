# import library
import pandas as pd

import gspread as gs
from gspread_formatting import *

# clustering & visualization
import matplotlib.pyplot as plt
from upsetplot import plot

# read google spread sheet(core features)
gc = gs.service_account(filename='../secure-outpost-380004-8d45b1504f3e.json')

sheet = gc.open('CPU Feature Visualization').worksheet('feature groups(all)')
df = pd.DataFrame(sheet.get_all_records())
featureGroups = df['feature groups'].tolist()

df = df.drop('feature groups', axis=1)
df = df.drop('Flags', axis=1)

values = []
for i in range(len(df)):
    values.append(df.iloc[i].tolist())

# 활성화된 flag 개수 추출 및 활성화된 flag의 개수가 같으나 종류가 다른 그룹의 조합을 추출
flagsCount = []

for i in range(len(values)):
    count = values[i].count(1)
    flagsCount.append(count)

duplicates = []

for value in set(flagsCount):
    if flagsCount.count(value) > 1:
        duplicates.append(value)

for value in duplicates:
    indexes_of_ones = [index + 2 for index, count in enumerate(flagsCount) if count == value]

flagToBinary = []

groupNumber = [str(i) for i in range(2,39)]

for value in values:
    binary_string = ''.join(str(i) for i in value)
    binary_number = int(binary_string, 2)
    flagToBinary.append(binary_number)

matrix = []
for binary in flagToBinary:
    row = []
    for i in range(len(flagToBinary)):
        if(binary & flagToBinary[i] == binary):
            row.append(True)
        else:
            row.append(False)
    matrix.append(row)

transferable = pd.DataFrame(matrix, columns=groupNumber)
transferable.index = range(2, len(transferable)+2)
transferable = transferable.groupby(groupNumber).size()

plot(transferable, orientation='horizontal')
plt.show()

for i in range(len(matrix)):
    print(f'Transferable group{i+2} to ',end='')
    for j in range(len(matrix[i])):
        if(matrix[i][j]):
            print(j+2, end=', ')
    print()