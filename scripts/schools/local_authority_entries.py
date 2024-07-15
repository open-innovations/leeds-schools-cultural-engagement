import os 
import pandas as pd 
from pathlib import Path

RAW_DATA = os.path.join('data', 'dfe', 'key-stage-4-performance_2022-23', '2223_subject_pupil_level_la_data_revised.csv')
OUT_DIR = os.path.join('src', '_data', 'viz', 'dashboard')

subjects = {
    'Any modern language',
    'Any Science',
    'Art and Design',
    'Business',
    'Computer Science',
    # 'Design & Technology',
    # 'Drama',
    'English & mathematics',
    'Media/Film/TV',
    # 'Film Studies',
    # 'Geography',
    # 'Religious Studies',
    # 'Social Studies',
    # 'Statistics'
    }

if __name__ == '__main__':

    raw_data = pd.read_csv(RAW_DATA).drop(columns={
        'time_identifier',
        'country_code',
        'country_name',
        'region_code',
        'region_name',
        'establishment_type'
    })

    leeds_gcse_data = raw_data.loc[(raw_data['la_name'] == 'Leeds') & 
                              (raw_data['qualification_type'] == 'GCSE') &
                              (raw_data['gender'] == 'Total') &
                              (raw_data['grade'] == 'Total pupil entries')] 
    
    # Select the subject areas we are interested in 
    leeds_gcse_subject_entries = leeds_gcse_data.loc[leeds_gcse_data['subject'].isin(subjects)]

    leeds_gcse_subject_entries.to_csv(os.path.join(OUT_DIR, 'leeds_GCSE_entries.csv'), index=False)