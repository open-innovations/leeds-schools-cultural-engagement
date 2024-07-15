import os 
import pandas as pd
from pathlib import Path
import re

RAW_DATA = os.path.join('data', 'dfe', 'ks4-performance', 'arts_mark_settings_24.csv')
OUT_DIR = os.path.join('src', '_data', 'viz', 'dashboard')
WARD_DATA = os.path.join('data', 'postcodes.csv')

def match_ward(data, postcode_field='Postcode', ward_column='ward_code'):
    data[postcode_field] = data[postcode_field].apply(postcode_formatter)
    data = data.merge(
        how='left',
        right=ward_data[['pcds', 'osward']],
        left_on=postcode_field,
        right_on='pcds',
        validate='many_to_one',
    )
    data.osward.fillna('UNKNOWN', inplace=True)
    data.drop(columns=['pcds'], inplace=True)
    data.rename(columns={'osward': ward_column}, inplace=True)
    return data

def postcode_formatter(postcode):
    if postcode is not None:
        postcode = re.sub(
            r'^([A-Z]+)(\d+)\s*(\d)([A-Z]{2})', r'\1\2 \3\4', str(postcode).upper().strip().replace(' ', ''))
        return postcode

if __name__ == '__main__':

    ward_data = pd.read_csv(WARD_DATA)

    artsmark_all = pd.read_csv(RAW_DATA, skiprows=7).iloc[:,1:].set_index('Setting Name')

    artsmark_leeds = artsmark_all.loc[artsmark_all['Local Authority']=='Leeds']

    artsmark_awarded = artsmark_leeds.loc[artsmark_leeds['Current Artsmark progress']=='Awarded']

    artsmark_ward_codes = match_ward(artsmark_awarded)

    artsmark_by_ward = artsmark_ward_codes.groupby('ward_code').size().reset_index(name='count_schools')   
    artsmark_by_ward.to_csv(os.path.join(OUT_DIR, 'artsmark_by_ward.csv'), index=False) 

