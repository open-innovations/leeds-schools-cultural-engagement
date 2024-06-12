import os 
import pandas as pd 
from pathlib import Path

RAW_DIR = os.path.join('data')
OUT_DIR = os.path.join('src', '_data', 'viz', 'dashboard')

SCHOOLS_REF_DATA = pd.read_csv(os.path.join(RAW_DIR, 'schools.csv'))
LEEDS_SCHOOLS = len(SCHOOLS_REF_DATA)

PROJECTED_POP_DATA = pd.read_csv(os.path.join(OUT_DIR, 'projected_population.csv'))
POP_DATA = pd.read_csv(os.path.join(OUT_DIR, 'population_data.csv'))


if __name__ == "__main__":

    headlines = {}

    leeds_population = POP_DATA.loc[(POP_DATA['AGE_NAME'] == 'All ages') & (POP_DATA['MEASURES_NAME'] == 'Value'), 'VALUE'].values[0].astype(int)

    school_age_population = POP_DATA.loc[(POP_DATA['AGE_NAME'] == 'Aged 0 - 19 years') & (POP_DATA['MEASURES_NAME'] == 'Value'), 'VALUE'].values[0].astype(int)

    projected_population_2025_all_ages = PROJECTED_POP_DATA.loc[
        (PROJECTED_POP_DATA['PROJECTED_YEAR'] == 2025), 
        'All Ages'
    ].values[0]

    projected_population_2025_0_19 = PROJECTED_POP_DATA.loc[
        (PROJECTED_POP_DATA['PROJECTED_YEAR'] == 2025), 
        'Aged 0-19'
    ].values[0]

    headlines['Leeds population'] = leeds_population
    headlines['Schools in Leeds'] = LEEDS_SCHOOLS
    headlines['School age population'] = school_age_population
    headlines['Projected population 2025 - all ages'] = projected_population_2025_all_ages
    headlines['Projected population 2025 - school age'] = projected_population_2025_0_19
    
    headlines = pd.DataFrame.from_dict(headlines, orient='index', columns=['value']).reset_index()
    headlines = headlines.rename(columns={'index':'headline'}).to_csv(os.path.join(OUT_DIR, 'headlines.csv'), index=False)

