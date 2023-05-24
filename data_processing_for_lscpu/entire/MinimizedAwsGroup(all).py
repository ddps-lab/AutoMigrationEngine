import re

import sys
from pathlib import Path

# module 경로 추가
sys.path.append(str(Path(__file__).resolve().parent.joinpath('..', 'modules')))

import GspreadUtils

df = GspreadUtils.read_gspread('simplized aws group(all)')
df = df['feature groups']

# df to list
groups = []

for i in range(len(df)):
    groups.append(df.iloc[i].split(', '))

prices = GspreadUtils.read_gspread('ec2 price(us-west-2, 23.05.24)')
prices = prices[['Instance', 'Linux On Demand cost']]

newGroups = []
totalPrice = 0

for group in groups:
    tempPrice = 0
    tempInstance = ''
    for instance in group:
        # 인스턴스 가격 조회
        price = prices.loc[prices['Instance'] == instance, 'Linux On Demand cost'].values.item()
        price = float(re.findall(r'\d+\.\d+', price)[0])

        if tempPrice == 0 or price < tempPrice:
            tempPrice = price
            tempInstance = instance
    newGroups.append(tempInstance)
    totalPrice += tempPrice

print(f"totalPrice : {totalPrice} USD/hour")

# update gspread
df = GspreadUtils.read_gspread('minimized aws group(all)')
df['feature groups'] = newGroups
GspreadUtils.write_gspread('minimized aws group(all)', df)