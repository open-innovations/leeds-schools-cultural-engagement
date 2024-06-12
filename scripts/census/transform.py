import os 
import pandas as pd

POPULATION_DATA = os.path.join('data', 'census', 'population.csv')
PROJECTED_POP_DATA = os.path.join('data', 'census', 'projected_population.csv')
OUT_DIR = os.path.join('src', '_data', 'viz', 'dashboard')

POP_COLUMNS = {
    'GEOGRAPHY_NAME',
    'AGE_NAME',
    'SEX_NAME',
    'MEASURES_NAME',
    'OBS_VALUE'
}

PROJ_COLUMNS = {
    'PROJECTED_YEAR',
    'C_AGE_NAME',
    'MEASURES_NAME',
    'OBS_VALUE'
}


if __name__ == '__main__':

    # POPULATION DATA 

    population_data = pd.read_csv(POPULATION_DATA, usecols= POP_COLUMNS)

    population_data = population_data[population_data['SEX_NAME']=='Total']

    population_data = population_data.set_index(['GEOGRAPHY_NAME', 'SEX_NAME' ]).pivot_table(
                values='OBS_VALUE',
                index=['GEOGRAPHY_NAME'],
                columns=[ 'AGE_NAME', 'MEASURES_NAME']
    )

    sum = (population_data['Aged 0 - 15', 'Value']) + (population_data['Aged 15 - 19 years', 'Value'])
    total = (population_data['All ages', 'Value'])
    

    population_data['Aged 0 - 19 years', 'Value'] =  sum
    population_data['Aged 0 - 19 years', 'Percent'] = (sum/ total *100).round(1)

    population_data = population_data.T.rename(columns={'Leeds': 'VALUE'})
    
    population_data.to_csv(os.path.join(OUT_DIR, 'population_data.csv'), index=True)



    # PROJECTED POPULATION

    projected_data = (
        pd.read_csv(PROJECTED_POP_DATA, usecols=PROJ_COLUMNS)
    )


    projected_data = projected_data.pivot_table(
        values='OBS_VALUE',
        columns=[ 'C_AGE_NAME'],
        index='PROJECTED_YEAR'
    )

    sum = (projected_data['Aged 0 to 15']) + (projected_data['Aged 15-19'])
    projected_data['Aged 0-19'] =  sum
    projected_data = projected_data.round(2)

    projected_data.to_csv(os.path.join(OUT_DIR, 'projected_population.csv'), index=True)



