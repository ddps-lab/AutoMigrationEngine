# import library
import pandas as pd

import gspread as gs
from gspread_formatting import *

# import math library
from math import *
from decimal import Decimal

import numpy as np

# clustering & visualization
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage

# read google spread sheet(core features)
gc = gs.service_account(filename='../secure-outpost-380004-8d45b1504f3e.json')

sheet = gc.open('CPU Feature Visualization').worksheet('feature groups(core)')
df = pd.DataFrame(sheet.get_all_records())

df = df.drop('feature groups', axis=1)

# 모든 값이 1로 이루어진 임의의 축 z 정의
df['z'] = 1

values = []
for i in range(len(df)):
    values.append(df.iloc[i].tolist())

matrix = []
for value in values:
    row = []
    for i in range(len(values)):
        cosine_sim = np.dot(value, values[i]) / (np.linalg.norm(value) * np.linalg.norm(values[i]))
        row.append(cosine_sim)
    matrix.append(row)

linkage_data = linkage(values, method='single', metric='cosine')
dendrogram(linkage_data)

plt.show()