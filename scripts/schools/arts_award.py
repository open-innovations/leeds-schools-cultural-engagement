import os 
import pandas as pd
from pathlib import Path
import re

# NOTE: This data is manually extracted from https://www.artsaward.org.uk/centre/lookup.php - need to find an alternative source or write a script to scrape the data. 
RAW_DATA = os.path.join('data', 'schools', 'arts_award.json')
OUT_DIR = os.path.join('src', '_data', 'viz', 'dashboard')
WARD_DATA = os.path.join('data', 'postcodes.csv')
SCHOOLS_DATA = os.path.join('data', 'leeds_schools_public.csv')

def match_ward(data, postcode_field='postcode', ward_column='ward_code'):
    data[postcode_field] = data[postcode_field].apply(postcode_formatter)
    data = data.merge(
        how='left',
        right=ward_data[['pcds', 'osward']],
        left_on=postcode_field,
        right_on='pcds',
        validate='many_to_one',
    )
    data['osward'] = data['osward'].fillna('UNKNOWN')
    data = data.drop(columns=['pcds'])
    data = data.rename(columns={'osward': ward_column})
    return data

def postcode_formatter(postcode):
    if postcode is not None:
        postcode = re.sub(
            r'^([A-Z]+)(\d+)\s*(\d)([A-Z]{2})', r'\1\2 \3\4', str(postcode).upper().strip().replace(' ', ''))
        return postcode

if __name__ == '__main__':

    ward_data = pd.read_csv(WARD_DATA)
    arts_award_centres = pd.read_json(RAW_DATA)
    arts_award_centres = pd.json_normalize(arts_award_centres.features)

    # Filter for orgs in Leeds, who engage with young people
    leeds = arts_award_centres[arts_award_centres['address2'].apply(lambda x: ', LS' in x)].copy()

    # leeds.contactfrom = leeds.contactfrom.str.split(',')
    # leeds = leeds[leeds['contactfrom'].apply(lambda x: 'Young people' in x)].copy()

    # Create a table of Leeds Arts Award centres
    leeds_table = leeds.drop(columns={'placeId', 'coords.lat', 'coords.lng', 'address1', 'address2'}).rename(columns={
        'title': 'Arts Award Centre', 
        'telephone': 'Telephone',
        'email': 'Email', 
        'website': 'Website',
        'artform': 'Artform', 
        'contactfrom': 'Welcomes contact from'
    })
    leeds_table.to_csv(os.path.join(OUT_DIR, 'arts_award_centres.csv'), index=False)

    # Group data by ward
    leeds['address2'] = leeds['address2'].str.split(',')
    leeds.loc[:, 'postcode'] = leeds['address2'].apply(lambda x: x[-1])
    arts_award_by_ward = match_ward(leeds)
    arts_award_by_ward = arts_award_by_ward.groupby('ward_code').size().reset_index(name='count_orgs')   
    arts_award_by_ward.to_csv(os.path.join(OUT_DIR, 'arts_award_leeds.csv'), index=False)

    # SCHOOLS BY ARTS AWARD STATUS

    schools_public = pd.read_csv(SCHOOLS_DATA, usecols={'school_name', 'ward_code', 'ward_name', 'school_postcode', 'artsaward'}).fillna('').rename(columns={'school_postcode':'postcode'})
    schools_public = schools_public.groupby('ward_code').size().reset_index(name="count_schools")

    schools_public.to_csv(os.path.join(OUT_DIR, 'arts_award_schools_by_ward.csv'), index=False)


