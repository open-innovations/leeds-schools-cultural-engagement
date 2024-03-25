import pandas as pd 
import os 
from survey_questions import SURVEY_QUESTION_MAPPER

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

    raw_data = raw_data.rename(columns = SURVEY_QUESTION_MAPPER).set_index('unique_response_number')

    base_respondents = len(raw_data)

    # Responses broken down by school type
    by_school_type = pd.DataFrame({
        'total_respondents' : raw_data.groupby('3_school_type')['3_school_type'].count(),
        'percent_respondents': raw_data.groupby('3_school_type')['3_school_type'].count().div(base_respondents).mul(100).round(0).astype(int),
        'unit': '%',
        'notes': [
            'of survey respondents were from a Primary school',
            'of survey respondents were from a Secondary school',
            'of survey respondents were from a Special school',
            'of survey respondents were from a Through school'
        ]
    }).to_csv(os.path.join(OUT_DIR, 'by_school_type.csv'))

    # Art provision in schools
    totals = raw_data.groupby(
            '3_school_type')['6_pupil_arts_entitlement'].count()

    responded_yes = raw_data.loc[raw_data['6_pupil_arts_entitlement'] == 'Yes'].groupby(
            '3_school_type')['6_pupil_arts_entitlement'].count()

    percent_responded_yes = (responded_yes/totals).mul(100).round(0).astype(int).values.tolist()

    arts_commitment_headlines = pd.DataFrame({
        'totals': totals,
        'responded_yes' : responded_yes,
        'percent_responded_yes' : percent_responded_yes,
        'unit': '%',
        'notes': [
            'of Primary schools who responded to the survey said they have a commitment to the arts',
            'of Secondary schools who responded to the survey said they have a commitment to the arts',
            'of Special schools who responded to the survey said they have a commitment to the arts',
            'of Through schools who responded to the survey said they have a commitment to the arts'
        ]
    }).to_csv(os.path.join(OUT_DIR, 'arts_commitment_headlines.csv'))

    # How would you rate your school's extra-curricular and arts enrichment offer?


    
