import pandas as pd
from pathlib import Path

import gspread as gs
from gspread_formatting import *

data_processing_for_lscpu_path = str(Path(__file__).resolve().parent.parent)

gc = gs.service_account(filename=f'{data_processing_for_lscpu_path}/secure-outpost-380004-8d45b1504f3e.json')

def read_CPU_Feature_Visualization(worksheet):
    sheet = gc.open('CPU Feature Visualization').worksheet(worksheet)
    df = pd.DataFrame(sheet.get_all_records())
    
    return df

def write_CPU_Feature_Visualization(worksheet, df):
    '''
    The function writes the contents of the dataframe to a Google Spreadsheet.
    '''
    # write google spread sheet1(core features)
    sheet = gc.open('CPU Feature Visualization').worksheet(worksheet)
    sheet.clear() # 이전 데이터 삭제
    sheet.update([df.columns.values.tolist()] + df.values.tolist())

    format_cell = cellFormat(
        verticalAlignment='MIDDLE', 
        wrapStrategy='OVERFLOW_CELL', 
        textFormat=textFormat(fontSize=10)
    )

    format_cell_range(sheet, '1:500', format_cell)

def read_AWS_migration_compatibility(worksheet):
    sheet = gc.open('AWS migration compatibility').worksheet(worksheet)
    df = pd.DataFrame(sheet.get_all_records())
    
    return df

def write_AWS_migration_compatibility(worksheet, df):
    '''
    The function writes the contents of the dataframe to a Google Spreadsheet.
    '''
    # write google spread sheet1(core features)
    sheet = gc.open('AWS migration compatibility').worksheet(worksheet)
    sheet.clear() # 이전 데이터 삭제
    sheet.update([df.columns.values.tolist()] + df.values.tolist())

    format_cell = cellFormat(
        verticalAlignment='MIDDLE', 
        wrapStrategy='OVERFLOW_CELL', 
        textFormat=textFormat(fontSize=10)
    )

    format_cell_range(sheet, '1:500', format_cell)