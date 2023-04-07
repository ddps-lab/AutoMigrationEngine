import sys
from pathlib import Path

# module 경로 추가
sys.path.append(str(Path(__file__).resolve().parent.joinpath('..', 'modules')))

import GspreadUtils
import Transferable

df = GspreadUtils.read_gspread('feature groups(all)')
featureGroups = df['feature groups'].tolist()

df = df.drop('feature groups', axis=1)
df = df.drop('Flags', axis=1)

GROUP_NUMBER = 37
Transferable.UpsetPlot(GROUP_NUMBER, df)