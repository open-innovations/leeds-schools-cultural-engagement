import os 
import pandas as pd 
from pathlib import Path

RAW_DIR = os.path.join('data', 'dfe')
OUT_DIR = os.path.join('src', '_data', 'viz', 'dashboard')

ENTRIES_DATA_2021 = os.path.join(
    RAW_DIR, 'Data_tables_for_provisional_entries_for_GCSE_AS_and_A_level_summer_2021_exam_series.xlsx')
ENTRIES_DATA_2023 = os.path.join(
    RAW_DIR, 'Data_tables_for_provisional_entries_for_GCSE_AS_and_A_level_summer_2023_exam_series.xlsx')

subject_entries_2021 = pd.read_excel(ENTRIES_DATA_2021, sheet_name='GCSE',
                            index_col=0, skiprows=3)

subject_entries_2023 = pd.read_excel(ENTRIES_DATA_2023, sheet_name='Table 1',
                            index_col=0, skiprows=1)

if __name__ == '__main__':

    # Process subject entries for years 2017-2018
    subject_entries_2017_2018 = (
        subject_entries_2021.iloc[:44]
        .drop(columns={
            'Year 9 & below_2021', 'Year 10_2021', 'Year 11_2021', 'Year 12_2021', 'Year 13+_2021',
            'Year 9 & below_2020', 'Year 10_2020', 'Year 11_2020', 'Year 12_2020', 'Year 13+_2020',
            'Year 9 & below_2019', 'Year 10_2019', 'Year 11_2019', 'Year 12_2019', 'Year 13+_2019',
            'Year 9 & below_2018', 'Year 10_2018', 'Year 11_2018', 'Year 12_2018', 'Year 13+_2018',
            'Year 9 & below_2017', 'Year 10_2017', 'Year 11_2017', 'Year 12_2017', 'Year 13+_2017'
        })
        .fillna(0)
        .replace('0~', 0)
        .reset_index()
    )
    subject_entries_2017_2018['JCQ_Code'] = subject_entries_2017_2018['JCQ_Code'].astype(int)

    # Process subject entries for years 2021-2023
    subject_entries_2021_2023 = (
        subject_entries_2023.iloc[:31]
        .drop(columns={
            'Year 9 and below June 2023', 'Year 10 June 2023', 'Year 11 June 2023', 'Year 12 June 2023', 'Year 13 and above June 2023',
            'Year 9 and below June 2022', 'Year 10 June 2022', 'Year 11 June 2022', 'Year 12 June 2022', 'Year 13 and above June 2022',
            'Year 9 and below June 2021', 'Year 10 June 2021', 'Year 11 June 2021', 'Year 12 June 2021', 'Year 13 and above June 2021', 'Total 2021',
            'Year 9 and below June 2020', 'Year 10 June 2020', 'Year 11 June 2020', 'Year 12 June 2020', 'Year 13 and above June 2020', 'Total 2020',
            'Year 9 and below June 2019', 'Year 10 June 2019', 'Year 11 June 2019', 'Year 12 June 2019', 'Year 13 and above June 2019', 'Total 2019'
        })
        .fillna(0)
        .reset_index()
    )

    # Merge and clean the data
    merged = (
        pd.merge(subject_entries_2021_2023, subject_entries_2017_2018, left_on='JCQ Code', right_on='JCQ_Code')
        .drop(columns={'JCQ Code', 'JCQ_Code', 'JCQ Title'})
        .rename(columns={'JCQ_Title': 'subject', 'Total 2023': '2023', 'Total 2022': '2022', 'Total_2021': '2021', 'Total_2020': '2020', 'Total_2019': '2019', 'Total_2018': '2018', 'Total_2017': '2017'})
    ).set_index('subject')

    # Prepare for visualisation
    merged = (
        merged.T
        .reset_index()
        .rename(columns={'index': 'year'})
        .astype(int)
    ).set_index('year')
    
    merged.to_csv(os.path.join(OUT_DIR, 'subject_entries_all.csv'))
    merged['Art & design subjects'].astype(int).to_csv(os.path.join(OUT_DIR, 'subject_entries_arts.csv'))


        
