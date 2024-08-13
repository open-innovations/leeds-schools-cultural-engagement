import os 
import pandas as pd 
from pathlib import Path

DATA_DIR = os.path.join('src', '_data', 'viz', 'schools')

datasets = {
    'schools.csv',
    'school-data-by-type.csv',
    'school-data-artsmark.csv',
    'school-data-artsaward.csv',
    'school-data-creative-entries.csv'
}

replace_types = ['Voluntary', 'Foundation', 'Community']

def calculate_percentages(df, columns, total_column):
    percentage_columns = []
    for column in columns:
        percentage_col = f'{column}_percent'
        df[percentage_col] = round(df[column] / df[total_column] * 100, 0)
        percentage_columns.append(percentage_col)
    return df

def group_and_sum(df, group_types, new_type_name, columns_to_sum, percentage_columns):
    summed_rows = df[df['type'].isin(group_types)].sum(numeric_only=True)
    summed_rows['type'] = new_type_name
    total_schools = summed_rows[columns_to_sum[-1]]

    for col in percentage_columns:
        base_col = col.replace('_percent', '')
        summed_rows[col] = round(summed_rows[base_col] / total_schools * 100, 0)

    df = df[~df['type'].isin(group_types)]
    df = pd.concat([df, pd.DataFrame([summed_rows])], ignore_index=True)
    return df


if __name__ == '__main__':

    dataframes = {}
    for dataset in datasets:
        file_path = os.path.join(DATA_DIR, dataset)
        dataframes[dataset] = pd.read_csv(file_path)

    schools_data = dataframes['schools.csv']

    # Artsmark status by school type

    artsmark_data = dataframes['school-data-artsmark.csv'][['type', 'Awarded', 'Registered', 'Working Towards', 'Total schools of this type']]
    artsmark_data[['awarded_percent', 'registered_percent', 'working_towards_percent']] = artsmark_data.apply(
        lambda row: pd.Series({
            'awarded_percent': round(row['Awarded'] / row['Total schools of this type'] * 100, 0),
            'registered_percent': round(row['Registered'] / row['Total schools of this type'] * 100, 0),
            'working_towards_percent': round(row['Working Towards'] / row['Total schools of this type'] * 100, 0)
        }), axis=1
    )
    replace_types = ['Voluntary', 'Foundation', 'Community']
    summed_rows = artsmark_data[artsmark_data['type'].isin(replace_types)].sum(numeric_only=True)
    summed_rows['type'] = 'Maintained'
    total_schools = summed_rows['Total schools of this type']
    summed_rows[['awarded_percent', 'registered_percent', 'working_towards_percent']] = [
        round(summed_rows['Awarded'] / total_schools * 100, 0),
        round(summed_rows['Registered'] / total_schools * 100, 0),
        round(summed_rows['Working Towards'] / total_schools * 100, 0)
    ]
    artsmark_data = artsmark_data[~artsmark_data['type'].isin(replace_types)]
    artsmark_data = pd.concat([artsmark_data, pd.DataFrame([summed_rows])], ignore_index=True)
    artsmark_data = artsmark_data.set_index('type').astype(int)
    artsmark_data.to_csv(os.path.join(DATA_DIR, 'school_data_artsmark_maintained.csv'))

    # Arts award status by school type 

    arts_award_data = dataframes['school-data-artsaward.csv'][['type', 'Number of schools signed up for Arts Award', 'Total Schools of this type', 'Percentage of schools of this type signed up for Arts Award']]

    summed_rows = arts_award_data[arts_award_data['type'].isin(replace_types)].sum(numeric_only=True)
    summed_rows['type'] = 'Maintained'
    total_schools = summed_rows['Total Schools of this type']

    summed_rows['Percentage of schools of this type signed up for Arts Award'] = round(
        summed_rows['Number of schools signed up for Arts Award'] / total_schools * 100, 2
    )

    arts_award_data = arts_award_data[~arts_award_data['type'].isin(replace_types)]

    arts_award_data = pd.concat([arts_award_data, pd.DataFrame([summed_rows])], ignore_index=True)
    arts_award_data = arts_award_data.set_index('type').astype(int)
    arts_award_data.to_csv(os.path.join(DATA_DIR, 'arts_award_data_maintained.csv'))

    # Replace the school types after
    schools_data['type'] = schools_data['type'].replace(replace_types, 'Maintained')
    schools_data.to_csv(os.path.join(DATA_DIR, 'schools.csv'), index=False)

