import os 
import pandas as pd 

RAW_DIR = os.path.join('data', 'dfe')
OUT_DIR = os.path.join('src', '_data', 'viz', 'dashboard')

RAW_DATA = os.path.join('data', 'dfe', 'a-level-and-other-16-to-18-results_2022-23', 'data', 'alevel_timeseries_subject_entries_results.csv')
OUT_DIR = os.path.join('src', '_data', 'viz', 'dashboard')

arts_subjects = {
    'Total subjects',
    'Art & design',
    'Design & technology',
    'Drama',
    'Media film tv',
    'Total Music'
}

def add_year_column(df):
    df['Year'] = df['time_period'].apply(lambda x: str(x)[:2] + str(x)[-2:])
    return df

def convert_columns_to_percentage(df, reference_column):
    for column in df.columns:
        if column != 'Year':
            df[column] = pd.to_numeric(df[column], errors='coerce')
    copy_df = df.copy()
    for column in copy_df.columns:
        if column != 'Year' and column != reference_column:
            copy_df[column] = ((copy_df[column] / copy_df[reference_column]) * 100).round(1)
    return copy_df

if __name__ == '__main__':

    raw_data = pd.read_csv(RAW_DATA, usecols={
        'time_period',
        'subject_name',
        'characteristic_value', 
        'entry_count'
    })
    raw_data = add_year_column(raw_data).drop(columns='time_period')
    raw_data = raw_data.loc[(raw_data['characteristic_value'] == 'All students') & (raw_data['subject_name'].isin(arts_subjects))]
    raw_data = raw_data.pivot(
        columns='subject_name',
        index='Year',
        values='entry_count'
    )

    raw_data.to_csv(os.path.join(OUT_DIR, 'a_level_arts_subject_timeseries.csv'))
    
    # Calculate percentage of all subjects

    arts_percentage = convert_columns_to_percentage(raw_data, 'Total subjects')
    arts_percentage.to_csv(os.path.join(OUT_DIR, 'a_level_arts_subject_timeseries_percent.csv'))