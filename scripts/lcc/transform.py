import os 
import pandas as pd
from fuzzywuzzy import process, fuzz
import re

LCIP_DATA = os.path.join('data', 'lcc', 'lcip_funded_revenue_organisations.csv')
ORG_DATA = os.path.join('data', 'orgs.csv')
OUT_DIR = os.path.join('src', '_data', 'viz', 'dashboard')

def fuzzy_match(row, choices, scorer, threshold=70):
    """Fuzzy matches a row against choices and returns the best match above the threshold."""
    match, score = process.extractOne(row, choices, scorer=scorer)
    if score >= threshold:
        return match
    else:
        return None
    
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

    lcip_data = pd.read_csv(LCIP_DATA)

    orgs_data = pd.read_csv(ORG_DATA).drop(columns={'Latitude','Longitude','Funding','Type of organisation','Website'})

    ward_data = pd.read_csv(os.path.join('data', 'postcodes.csv'))

    right_names = orgs_data['Name'].unique()

    lcip_data['matched_name'] = lcip_data['Organisation'].apply(lambda x: fuzzy_match(x, right_names, scorer=fuzz.token_sort_ratio))

    # Manual matches dictionary
    manual_matches = {
        'Compass Live Art Limited ': 'Compass Live Art & Compass Festival',
        'Skippko Arts Team': 'Skippko',
        'Leeds Print Workshop Ltd': 'East Street Arts',
        'The Courthouse Project (Otley) - trading as Otley Courthouse': 'Otley Courthouse',
        'The Yorkshire Dance Centre Trust': 'Yorkshire Dance'
    }

    # Update matched_name column with manual matches
    lcip_data['matched_name'] = lcip_data.apply(lambda row: manual_matches.get(row['Organisation'], row['matched_name']), axis=1)

    merged_df = pd.merge(lcip_data, orgs_data, how='left', left_on='matched_name', right_on='Name')

    orgs_with_ward_codes = match_ward(merged_df)

    orgs_by_ward = orgs_with_ward_codes.groupby('ward_code').size().reset_index(name='organisations')

    # Save the result
    orgs_with_ward_codes.to_csv(os.path.join(OUT_DIR, 'lcc_funded_organisations.csv'), index=False)
    orgs_by_ward.to_csv(os.path.join(OUT_DIR, 'lcip_funded_orgs_by_ward.csv'), index=False)