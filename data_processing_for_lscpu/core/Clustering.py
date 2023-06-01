import numpy as np

# clustering & visualization
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage

import sys
from pathlib import Path

# module 경로 추가
sys.path.append(str(Path(__file__).resolve().parent.joinpath('..', 'modules')))

import GspreadUtils

df = GspreadUtils.read_CPU_Feature_Visualization('feature groups(core)')

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