
import os
import pandas as pd
import ast

from thefuzz import process

SCHOOLS_DATA = os.path.join('working', 'upstream', 'schools_events.csv')
SCHOOLS_REF_DATA = os.path.join('data', 'schools.csv')
WARD_REFERENCE = os.path.join('data', 'leeds_wards.csv')
DATA_DIR = os.path.join('data', 'leeds-2023')
VIZ_DIR = os.path.join('src', '_data', 'viz', 'leeds_2023')
UNIQUE_SCHOOLS_OVERRIDE = 228
TOTAL_SCHOOL_ENGAGEMENTS_OVERRIDE=501
SCHOOL_COUNT_OVERRIDE = 294

def load_schools_data():
    return pd.read_csv(SCHOOLS_DATA, parse_dates=['date']).apply(literal_converter)

def literal_converter(series):
    def convert(value):
        try:
            return ast.literal_eval(value)
        except (SyntaxError, ValueError):
            return value
    return series.apply(convert)

def fuzzy_match_leeds_wards(data, ward_name_col="ward", ward_code_col="ward_code"):
    wards = pd.read_csv(WARD_REFERENCE)
    valid_wards = data[ward_name_col].notna()
    data.loc[valid_wards, 'WD21NM'] = data.loc[valid_wards, ward_name_col].apply(
        lambda x: process.extractOne(x, wards.WD21NM)[0])
    data = pd.merge(left=data, right=wards, how='left', on='WD21NM')
    data = data.drop(columns=[ward_name_col]).rename(columns={'WD21CD': ward_code_col, 'WD21NM': ward_name_col})
    return data

if __name__ == "__main__":
    # Load data
    data = load_schools_data()
    data.to_csv(os.path.join(DATA_DIR, 'schools_events.csv'), index=False)
    all_schools = pd.read_csv(SCHOOLS_REF_DATA, usecols=['school_name', 'ward_name', 'ward_code']).set_index('school_name')
    leeds_wards = pd.read_csv(WARD_REFERENCE)
    
    # Count summary statistics
    summary = {}
    summary['Schools in Leeds'] = SCHOOL_COUNT_OVERRIDE
    summary['Schools not assigned to ward'] = len(all_schools[all_schools.ward_name.isna()])
    summary['Total pupil engagements'] = data.pupil_count.sum().astype(int)
    summary['Total school engagements'] = TOTAL_SCHOOL_ENGAGEMENTS_OVERRIDE
    summary['Unique schools'] = UNIQUE_SCHOOLS_OVERRIDE
    summary['Percentage of Leeds schools engaged'] = str(round((summary['Unique schools'] / SCHOOL_COUNT_OVERRIDE * 100),2)) + '%'
    summary['Date build'] = pd.Timestamp.today().floor('D').strftime('%Y-%m-%d')
    summary['Earliest date'] = data.date.min().strftime('%Y-%m-%d')

    # Write engagements by week 
    pupil_engagements = data.groupby('date').pupil_count.sum().resample('W-FRI').sum().astype(int)
    school_engagements = data.groupby('date').school_count.sum().resample('W-FRI').sum()
    cumulative_pupil_engagements = pupil_engagements.cumsum()
    cumulative_school_engagements = school_engagements.cumsum()
    engagements_by_week = pd.DataFrame({
        'pupil_engagements': pupil_engagements,
        'cumulative_pupil_engagements': cumulative_pupil_engagements,
        'school_engagements': school_engagements,
        'cumulative_school_engagements': cumulative_school_engagements,
    })
    engagements_by_week.to_csv(os.path.join(VIZ_DIR, 'engagements_by_week.csv'))

    # Write school engagement counts
    schools_counts = data.schools.explode().value_counts().to_frame().reset_index()
    schools_counts.columns = ['school_name', 'count_of_engagements']
    schools_counts = schools_counts.merge(
        right=all_schools,
        left_on='school_name', 
        right_on='school_name',
        how='left' 
    )
    schools_counts.to_csv(os.path.join(VIZ_DIR, 'school_engagement_counts.csv'), index=False)

    # Write engagements by ward
    ward_stats = leeds_wards.merge(
        schools_counts.reset_index(),
        how='left',
        left_on='WD21CD',
        right_on='ward_code',
    )

    pupils_per_ward = data[['pupil_count', 'wards']].explode('wards').rename(columns={
            'wards': 'ward_name',
        })
    pupils_per_ward = fuzzy_match_leeds_wards(pupils_per_ward, ward_name_col='ward_name')

    ward_group = ward_stats.groupby(['WD21CD', 'WD21NM'])
    engagements_by_ward = pd.DataFrame({
        'schools_engaged': ward_group.count_of_engagements.count(),
        'total_engagements': ward_group.count_of_engagements.sum(),
        'count_of_schools': all_schools.reset_index().groupby(['ward_code', 'ward_name']).school_name.count(),
        'pupil_engagements': pupils_per_ward.groupby(['ward_code', 'ward_name']).pupil_count.sum(),
    }).fillna(0).astype(int)

    summary['Engagements with schools not assigned to ward'] = schools_counts[schools_counts.ward_code.isna()].count_of_engagements.sum().astype(int)
    summary['Engagements with pupils not assigned to ward'] = (data.pupil_count.sum() - engagements_by_ward.pupil_engagements.sum()).astype(int)

    engagements_by_ward.index.names = ['ward_code', 'ward']
    engagements_by_ward['percent_of_schools_in_ward_engaged'] = (engagements_by_ward.schools_engaged / engagements_by_ward.count_of_schools * 100).astype(int)

    engagements_by_ward.to_csv(os.path.join(VIZ_DIR, 'engagements_by_ward.csv'))

    # Write summary JSON
    summary = pd.DataFrame.from_dict(summary, orient="index", columns=['value']).sort_index()
    summary.value.to_json(os.path.join(VIZ_DIR, 'summary.json'), indent=2)

    # Write summary CSV
    summary = summary.reset_index().rename(columns={'index': 'title'})
    summary.to_csv(os.path.join(VIZ_DIR, 'headlines.csv'), index=False)