import os 
import pandas as pd 
from pathlib import Path

RAW_DIR = os.path.join('data', 'dfe')
OUT_DIR = os.path.join('src', '_data', 'viz', 'dashboard')

RAW_DATA = os.path.join('data', 'dfe', 'ks4-performance', '2223_subject_timeseries_data_revised.csv')
OUT_DIR = os.path.join('src', '_data', 'viz', 'dashboard')

def add_year_column(df):
    df['Year'] = df['time_period'].apply(lambda x: str(x)[:2] + str(x)[-2:])
    return df

def convert_columns_to_percentage(df, reference_column):
    for column in df.columns:
        if column != 'Year':
            df[column] = pd.to_numeric(df[column], errors='coerce')
    percentage_df = df.copy()
    for column in percentage_df.columns:
        if column != 'Year' and column != reference_column:
            percentage_df[column] = ((percentage_df[column] / percentage_df[reference_column]) * 100).round(1)
    return percentage_df

def summarise(df):
    art_subjects = [col for col in df.columns if col not in ['Year', 'All Subjects', 'Art and Design']]
    df['Art & Design Subjects'] = df[art_subjects].sum(axis=1)
    df['Art & Design Subjects (%)'] = (df['Art & Design Subjects'] / df['All Subjects']) * 100
    return df

arts_subjects = {
    'All Subjects',
    'Art and Design',
    'Dance',
    'Design & Technology',
    'Drama',
    'Media/Film/TV',
    'Music', 
    'Performing Arts'
}

if __name__ == '__main__':

    # Art & Design Subjects

    raw_data = pd.read_csv(RAW_DATA, usecols={
        'time_period',
        'gender',
        'subject', 
        'total_exam_entries', 
        'grade', 
        })
    
    add_year_column(raw_data)
    
    total_data = (
        raw_data.loc[(raw_data['grade'] == '91AstarG') & (raw_data['gender'] == 'Total')]
        .drop(columns={'grade', 'time_period'})
    )

    arts_subjects = total_data.loc[total_data.subject.isin(arts_subjects)]

    arts_subjects = arts_subjects.pivot(
        columns='subject',
        index='Year',
        values='total_exam_entries'
    )
    arts_subjects.to_csv(os.path.join(OUT_DIR, 'arts_subjects.csv'))

    # Calculate percentage of all subjects

    arts_percentage = convert_columns_to_percentage(arts_subjects, 'All Subjects')
    arts_percentage.to_csv(os.path.join(OUT_DIR, 'arts_percentage.csv'))

    # Add up and present as total percentage

    art_design_subjects = summarise(arts_subjects)
    # art_design_subjects.to_csv(os.path.join(OUT_DIR, 'art_design_subjects.csv'))
