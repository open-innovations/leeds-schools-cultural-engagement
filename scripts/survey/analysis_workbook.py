import os
from pathlib import Path

import pandas as pd
import numpy as np
import xlsxwriter
from xlsxwriter.utility import xl_rowcol_to_cell
import matplotlib.pyplot as plt
from matplotlib import style

from survey_util import SURVEY_QUESTION_MAPPER
from survey_util import load_raw_survey_data
from survey_util import drop_duplicates

# Define paths and base directories
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
CHART_DIR = PROJECT_ROOT / 'data/survey/charts'
REPORT_DIR = PROJECT_ROOT / 'data/survey/report'
VIZ_DIR = PROJECT_ROOT / 'src/_data/viz/survey/phase_2'

# Create directories if they don't exist
CHART_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)
VIZ_DIR.mkdir(parents=True, exist_ok=True)

# Load and process data
raw_data = load_raw_survey_data()
raw_data_deduped = drop_duplicates(raw_data)

columns = {
    '04_role',
    '05_overall_rating_arts_offer',
    '06_pupil_arts_entitlement',
    '07_additional_arts_funding',
    '09_competitions_showcases',
    '10_does_your_school_actively_sign-post_opportunities_for_pupils_to_develop_creative_skills_and_participate_in_arts_opportunities_beyond_the_curriculum',
    '11_governors_creative_industries',
    '12_governor_dedicated_arts_remit',
    '13c_do_pupils_have_access_to_any_of_these_facilities_outside_of_formal_extra-curricular_activities_and_lessons_unsupervised',
    '14_how_would_you_rate_your_schools_extra-curricular_and_arts_enrichment_offer_answers_will_be_anonymised_and_data_will_not_be_linked_to_individual_schools',
    '15b_supply_musical_instruments',
    '16_arts_award',
    '17_arts_council',
    '18_external_orgs_arts_performances',
    '19_arts_trips',
    '21_regarding_access_diversity_and_inclusion_â_does_your_school_experience_any_barriers_or_challenges_in_encouraging_recruiting_or_gaining_permissions_for_pupils_to_go_on_trips_out_of_school',
    '22_regarding_access_diversity_and_inclusion_â_does_your_school_experience_any_barriers_or_challenges_with_the_experience_or_facilities_at_host_venues_when_taking_pupils_on_trips_out_of_the_school',
    '23_national_programmes',
    '24_partnerships_external_orgs',
    '25_partnerships_local_schools',
    '26_is_your_school_part_of_any_localcommunity-based_arts_programmes',
    '28_partnerships_diversity_challenges',
    '29_does_your_school_give_pupils_opportunities_to_engage_with_professionals_or_practitioners_in_the_arts_eg_musicians_or_artists-in-residence',
    '30_specialist_creative_career_advice',
    '31_data_pupil_progression_creative_education',
    '32_supporting_teacher_cpd'
}


def break_down_by_school_type(data, question, output_file_path=VIZ_DIR):
    try:
        if data[question].isna().all():
            print(f"No responses found for question: {question}")
            return None

        unique_responses = data[question].dropna().unique()
        if len(unique_responses) == 0:
            print(f"No valid responses found for question: {question}")
            return None

        result = (
            data.groupby(['03_school_type', question])
            .size()
            .unstack(fill_value=0)
            .apply(lambda x: (x / x.sum()) * 100 if x.sum() > 0 else x, axis=1)
            .round(0)
            .astype(int)
            .reset_index()
            .rename(columns={'03_school_type': 'School Type'})
        ).set_index('School Type')

        result['suffix'] = '%'
        return result
    except Exception as e:
        print(f"Error in break_down_by_school_type for {question}: {str(e)}")
        return None

def get_question_title(survey_questions, question):
    for original_title, mapped_title in survey_questions.items():
        if mapped_title == question:
            return original_title
    return question 

def create_chart(data, question, chart_dir=CHART_DIR, figsize=(6, 3)):
    try:
        responses = break_down_by_school_type(data, question)
        if responses is None:
            return

        school_type = responses.index
        x = np.arange(len(school_type))
        x_labels = school_type
        width = 1/(len(responses.columns))
        multiplier = 0

        fig, ax = plt.subplots(figsize=figsize)
        plt.style.use('bmh')
        plt.rcParams.update({'font.size': 8})

        for attribute, measurement in responses.items():
            offset = width * multiplier
            rects = ax.bar(x + offset, measurement, width, label=attribute)
            multiplier += 1

        ax.set_ylabel('Responses (%)')
        ax.set_title('{}'.format(get_question_title(SURVEY_QUESTION_MAPPER, question)), 
                     weight='bold', y=1.15, fontsize=9)
                    
        ax.set_xticks(x + width * (len(responses) - 1) / 2)
        ax.set_xticklabels(x_labels)
        ax.legend(ncol=len(responses.columns), bbox_to_anchor=(1.1, 1.15), columnspacing=0.5)

        plt.tight_layout()
        plt.savefig(chart_dir / '{}.png'.format(question), dpi=300, bbox_inches="tight")
        plt.close()
    except Exception as e:
        print(f"Error creating chart for {question}: {str(e)}")

def title_format(workbook):
    return workbook.add_format({
        'bold': True,
        "font_size": 16,
    })

def content_format(workbook):
    return workbook.add_format({
        'align': 'left',
        "font_size": 12,
    })

def main():
    output_file = 'Phase 2 Survey Analysis.xlsx'

    with pd.ExcelWriter(REPORT_DIR / output_file, engine='xlsxwriter') as writer:
        workbook = writer.book
        worksheet = workbook.add_worksheet('Sheet1')

        row_position = 9

        worksheet.write('B2', 'Phase 2 Survey Data Analysis', title_format(workbook))
        worksheet.write('B3', 
                       'This workbook contains the tables, charts and data analysis for the Creative Arts Education in Leeds Survey, 2024. It will be developed as the project progresses, and as more data sources become available for analysis.', 
                       content_format(workbook))

        for column in sorted(columns):
            try:
                responses = break_down_by_school_type(raw_data_deduped, column)
                if responses is None:
                    continue
                    
                worksheet.set_column(1, 5, 25)
                
                responses.to_excel(writer, sheet_name='Sheet1', startcol=1, startrow=row_position, index=True)
                create_chart(raw_data_deduped, column)
                
                worksheet.insert_image(f'H{row_position}', 
                                     str(CHART_DIR / '{}.png'.format(column)))
                
                row_position += 20
            except Exception as e:
                print(f"Error processing column {column}: {str(e)}")
                continue

if __name__ == "__main__":
    main() 