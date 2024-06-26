import os 
import pandas as pd

#TODO: Documentation - IMD is normally published at LSOA level, which does not map perfectly to ward. We used the ONS best fit lookup (available here: https://geoportal.statistics.gov.uk/datasets/686527814d73403e8f0a59c7a28b0c34_0/explore) and calculated an average (mean IMD score) for each ward. An alternative approach to this might be to calculate the percentage of LSOAs within each ward that have a score of 1 or 2, indicating a higher proportion of deprived areas within each ward.

IMD_PATH = os.path.join('data', 'imd', 'imd_2019.xlsx')
LSOA_LOOKUP_PATH = os.path.join('data', 'LSOA_ward_LAD_lookup.csv')
OUT_DIR = os.path.join('src', '_data', 'viz', 'dashboard')


if __name__ == "__main__":

    imd_data = pd.read_excel(IMD_PATH, sheet_name='IMD2019')
    leeds_imd = imd_data.loc[imd_data['Local Authority District name (2019)'] == "Leeds"]

    lsoa_ward_lookup = pd.read_csv(LSOA_LOOKUP_PATH, usecols={'LSOA21CD', 'LSOA21NM', 'WD24CD', 'WD24NM', 'LAD24CD', 'LAD24NM' })
    leeds_lookup = lsoa_ward_lookup.loc[lsoa_ward_lookup.LAD24NM == "Leeds"]

    data = leeds_imd.merge(
        how='left',
        right=leeds_lookup[['LSOA21CD', 'WD24CD', 'WD24NM' ]],
        left_on='LSOA code (2011)',
        right_on='LSOA21CD',
        validate='many_to_one'
    ).dropna().drop(columns={'Local Authority District code (2019)', 'Local Authority District name (2019)'})

    data = data.rename(columns={
        'Index of Multiple Deprivation (IMD) Rank': 'imd_rank',
        'Index of Multiple Deprivation (IMD) Decile': 'imd_decile'
    })

    #TODO: Confirm that this is the best way to represent IMD.
    data = data.groupby('WD24CD')['imd_decile'].mean().round(2).reset_index(name='imd_decile')
    
    data.to_csv(os.path.join(OUT_DIR, 'imd_by_ward.csv'), index=False)





    