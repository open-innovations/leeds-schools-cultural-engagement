import pandas as pd 
import os 

RAW_DIR = os.path.join('data', 'raw')

OUT_DIR = os.path.join('src', '_data', 'viz', 'survey', 'phase_2')

RAW_DATA = os.path.join(
    RAW_DIR, 'Results-for-creative-arts-2024_no-personal-data.xlsx')

REF_SCHOOLS_DATA = os.path.join(
    'data', 'leeds_schools_public.csv'
)

raw_data = pd.read_excel(RAW_DATA)
ref_schools_data = pd.read_csv(REF_SCHOOLS_DATA)



if __name__ == '__main__':

    raw_data = raw_data.rename(columns= {'3. Type of school': '3_school_type'}).set_index('Unique Response Number')

    base_respondents = len(raw_data)

    # Responses broken down by school type
    by_school_type = pd.DataFrame({
        'total_respondents' : raw_data.groupby('3_school_type')['3_school_type'].count(),
        'percent_respondents': raw_data.groupby('3_school_type')['3_school_type'].count().div(base_respondents).mul(100).round(1),
        'unit': '%'
    }).to_csv(os.path.join(OUT_DIR, 'by_school_type.csv'))

    
