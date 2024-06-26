import os 
import pandas as pd 
from pathlib import Path

RAW_DIR = os.path.join('data', 'dfe')
OUT_DIR = os.path.join('src', '_data', 'viz', 'dashboard')

ENTRIES_DATA_2021 = os.path.join(
    RAW_DIR, 'Data_tables_for_provisional_entries_for_GCSE_AS_and_A_level_summer_2021_exam_series.xlsx')
ENTRIES_DATA_2023 = os.path.join(
    RAW_DIR, 'Data_tables_for_provisional_entries_for_GCSE_AS_and_A_level_summer_2023_exam_series.xlsx')

subject_entries_2021 = pd.read_excel(ENTRIES_DATA_2021, sheet_name='A level',
                            index_col=0, skiprows=3)

subject_entries_2023 = pd.read_excel(ENTRIES_DATA_2023, sheet_name='Table 4',
                            index_col=0, skiprows=1)

if __name__ == '__main__':

    # Process subject entries for years 2017-2018
    subject_entries_2017_2018 = (
        subject_entries_2021.iloc[:44]
        .drop(columns={
            'Year 11 & below_2021', 'Year 12_2021', 'Year 13_2021', 'Year 14+_2021',
            'Year 11 & below_2020', 'Year 12_2020', 'Year 13_2020', 'Year 14+_2020',
            'Year 11 & below_2019', 'Year 12_2019', 'Year 13_2019', 'Year 14+_2019',
            'Year 11 & below_2018', 'Year 12_2018', 'Year 13_2018', 'Year 14+_2018',
            'Year 11 & below_2017', 'Year 12_2017', 'Year 13_2017', 'Year 14+_2017',
        })
        .fillna(0)
        .replace('0~', 0)
        .replace('-', 0)
        .reset_index()
    )
    subject_entries_2017_2018['JCQ_Code'] = subject_entries_2017_2018['JCQ_Code'].astype(int)

    # Process subject entries for years 2021-2023
    subject_entries_2021_2023 = (
        subject_entries_2023.iloc[:31]
        .loc[:, ['JCQ Code', 'Total 2022', 'Total 2023']]
        .fillna(0)
        .reset_index()
    )

    # Merge and clean the data
    merged = (
        pd.merge(subject_entries_2017_2018, subject_entries_2021_2023, left_on='JCQ_Code', right_on='JCQ Code')
        .drop(columns={'JCQ Code', 'JCQ_Code', 'JCQ Title'})
        .rename(columns={'JCQ_Title': 'subject', 'Total 2023': '2023', 'Total 2022': '2022', 'Total_2021': '2021', 'Total_2020': '2020', 'Total_2019': '2019', 'Total_2018': '2018', 'Total_2017': '2017'})
    ).set_index('subject')

    merged = merged.reindex(sorted(merged.columns), axis=1)

    # # Prepare for visualisation
    merged = (
        merged.T
        .reset_index()
        .rename(columns={'index': 'year'})
        .astype(int)
    ).set_index('year')
    
    merged.to_csv(os.path.join(OUT_DIR, 'subject_entries_all_a_level.csv'))
    merged['Art & design subjects'].astype(int).to_csv(os.path.join(OUT_DIR, 'subject_entries_arts_a_level.csv'))


        
