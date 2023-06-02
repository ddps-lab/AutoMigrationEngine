import sys
from pathlib import Path

# module 경로 추가
sys.path.append(str(Path(__file__).resolve().parent.joinpath('modules')))

import ReadCsv
import GspreadUtils

def CollectGroupNumbersForInstances():
    '''
    https://docs.google.com/spreadsheets/d/1NCqFbgMiD9h6qxwrruAia0_yYv3nWi0suU2h5kut8NA/edit#gid=886260129\n
    Returns the group number that maps to the instance based on the latest dataset.\n
    Collected for re-experiment of failed instances in the CRIU restore phase.
    '''
    df = GspreadUtils.read_AWS_migration_compatibility("Group all features with the same instances")
    groups = df['feature groups'].to_list()

    df = ReadCsv.read_exp_failure_cases()
    df = df.sort_values(by='source')

    cases = []
    grouped = df.groupby('source')['destination'].apply(list)
    for source, destinations in grouped.items():
        instances = ([source] + destinations)
        case = [groups.index(element) for element in instances]
        
        cases.append(case)

    # Sorting by source
    cases = sorted(cases, key=lambda x: x[0])
    # Sorting destinations
    cases = [sub_lst[:1] + sorted(sub_lst[1:]) for sub_lst in cases]

    return cases