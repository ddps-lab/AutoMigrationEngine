import pandas as pd
from pathlib import Path

data_processing_for_lscpu_path = str(Path(__file__).resolve().parent.parent)

def read_csv(CPU_FEATURES):
    """
    The function reads data from a CSV file that contains information collected from different cloud vendors. It extracts the columns InstanceType, CloudProvider, Model name, and flags to create a dataframe. Additionally, it splits the flags column into separate columns based on the CPU_FEATURES list passed as a parameter to the function.
    """
    # csv read & add header
    df = pd.read_csv(f'{data_processing_for_lscpu_path}/lscpu/lscpu_all_vendors.csv', usecols=['CloudProvider', 'Architecture', 'InstanceType', 'Model name', 'Flags'], index_col='InstanceType')
    df = df.reset_index()
    df = df.loc[df['Architecture'] == 'x86_64']

    df.drop('Architecture', axis=1, inplace=True)
    df = df[['InstanceType', 'CloudProvider', 'Model name', 'Flags']]

    df = pd.concat([df, pd.DataFrame(columns=CPU_FEATURES)], axis=1)

    # remove the unsupported instance type by AWS
    unsupported = ['m2.2xlarge', 'm2.4xlarge', 'm2.xlarge', 't1.micro', 'c1.xlarge', 'm1.large', 'm1.medium', 'm1.small', 'm1.xlarge', 'c3.2xlarge', 'c3.4xlarge', 'c3.8xlarge', 'c3.large', 'c3.xlarge', 'g2.2xlarge', 'i2.2xlarge', 'i2.4xlarge', 'i2.8xlarge', 'i2.xlarge', 'm3.2xlarge', 'm3.large', 'm3.medium', 'm3.xlarge', 'r3.2xlarge', 'r3.4xlarge', 'r3.8xlarge', 'r3.large', 'r3.xlarge', 'u-18tb1.112xlarge']
    
    for instance in unsupported:
        df = df.drop(df[df['InstanceType'] == instance].index)

    return df