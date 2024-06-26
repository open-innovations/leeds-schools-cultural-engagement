import os 
import pandas as pd
import re

ORG_DATA = os.path.join('data', 'orgs.csv')
OUT_DIR = os.path.join('src', '_data', 'viz', 'dashboard')


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


if __name__ == "__main__":

    ward_data = pd.read_csv(os.path.join('data', 'postcodes.csv'))

    organisations = pd.read_csv(ORG_DATA).drop(columns={
        'Funding',
        'Type of organisation',
        'Website'
    })

    orgs_with_ward_codes = match_ward(organisations)
    orgs_by_ward = orgs_with_ward_codes.groupby('ward_code').size().reset_index(name='count_orgs')   
    orgs_by_ward.to_csv(os.path.join(OUT_DIR, 'organisations_by_ward.csv'), index=False) 

