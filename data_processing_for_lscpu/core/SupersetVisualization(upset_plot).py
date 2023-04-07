import sys
from pathlib import Path

# module 경로 추가
sys.path.append(str(Path(__file__).resolve().parent.joinpath('..', 'modules')))

import GspreadUtils
import Transferable

df = GspreadUtils.read_gspread('simplized aws group(core)')
featureGroups = df['feature groups'].tolist()
df = df.drop('feature groups', axis=1)

GROUP_NUMBER = 10
Transferable.UpsetPlot(GROUP_NUMBER, df)