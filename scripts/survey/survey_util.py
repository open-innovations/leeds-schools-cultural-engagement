import pandas as pd

SURVEY_PATH = ('../../data/survey/raw/Results-for-creative-arts-2024_no-personal-data.xlsx')

SURVEY_QUESTION_MAPPER = {
    "Unique Response Number": "unique_response_number",
    "2. Name of school": "02_school_name",
    "3. Type of school": "03_school_type",
    "3.a. If you selected Other, please specify:" : "03a_other",
    "4. What is your role?": "04_role",
    "4.a. Please specify your role:" : "04a_other_role",
    "5. Overall, how would you rate your school's arts curriculum offer?" : "05_overall_rating_arts_offer",
    "5.a. Why do you rate your school's arts curriculum as excellent/good?": "05a_why_excellent_good",
    "5.b. Why do you rate your school's arts curriculum as mixed?": "05b_why_mixed",
    "5.c. Why do you rate your school's arts curriculum as poor/very poor?": "05c_why_poor",
    "6. Does your school have a particular commitment(s) to pupil entitlement in the arts?": "06_pupil_arts_entitlement",
    "6.a. If yes, please tell us more about the commitment(s)." : "06a_pupil_entitlement_details",
    "7. Does your school attract additional funding for arts curriculum or enrichment activity?" : "07_additional_arts_funding",
    "7.a. Where does your school attract funding from? Tick all that apply.": "07a_arts_funding_sources",
    "7.a.i. If you selected Other, please specify your school's other sources of arts funding:": "07ai_other_funding_details",
    "8. Does your school offer any of the following non-curricular arts activities that pupils can participate in?": "08_non_curricular_arts_activities",
    "8.a. Please describe the year groups or key stages that are involved in these activities, or whether they are open to the whole school.": "08a_year_groups_non_curricular_activities",
    "8.b. Do you invite parents or a wider audience to any of these activities?": "08b_parents_wide_audience",
    "8.c. If you selected Other non-curriculum activities, what does your school provide?" : "08c_other_non_curricular_activities",
    "9. Does your school enter pupils into any competitions, platforms or showcases at a local, community, regional or national level?": "09_competitions_showcases",
    "9.a. What competitions, platforms or showcases has your school entered pupils into?": "09a_competitions_details",
    "10. Does your school actively sign-post opportunities for pupils to develop creative skills and participate in arts opportunities beyond the curriculum?": "10_signposting_beyond_curriculum",
    "10.a. What activities are sign-posted?": "10a_signposted_activities_details",
    "11. Do any of your school's governors work in the arts or creative industries?": "11_governors_creative_industries",
    "12. Does your school have a governor with a dedicated remit for the arts and creative education?": "12_governor_dedicated_arts_remit",
    "13. Does your school have... Tick all that apply": "13_arts_facilities",
    "13.a. If you selected Other, please specify what arts or creative facilities your school has:": "13a_other_arts_facilities_details",
    "13.b. What production facilities does your hall or theatre have?": "13b_production_facilities",
    "13.c. Do pupils have access to any of these facilities outside of formal extra-curricular activities and lessons unsupervised?": "13c_unsupervised_access_facilities",
    "13.c.i. If there is a mixed level of access to different facilities, please comment on this here:": "13ci_mixed_access_details",
    "14. How would you rate your school's extra-curricular and arts enrichment offer?": "14_rating_extra_curricular_arts_enrichment_offering",
    "14.a. Why do you rate your school's extra-curricular or arts enrichment offer as excellent or good?": "14a_why_excellent_good",
    "14.b. Why do you rate your school's extra-curricular or arts enrichment offer as mixed?": "14b_why_mixed",
    "14.c. Why do you rate your school's extra-curricular or arts enrichment offer as poor or very poor?": "14c_why_poor",
    "15. Does your school offer any of the following extra-curricular activity or arts enrichment?" : "15_offer_extracurricular_activity_select",
    "15.a. If you selected Other extra-curricular or arts enrichment activities, please specify:": "15a_other_extracurricular_details",
    "15.b. Do you supply musical instruments?": "15b_supply_musical_instruments",
    "15.c. Are the music lessons (individual or group) run by the school/teachers OR external providers that come into the school?": "15c_music_lessons_teachers_or_external",
    "15.c.i. Please tell us the names of the providers (organisations or freelance creative practitioners).": "15ci_music_lesson_provider_names",
    "15.d. Are the orchestras, ensembles or bands run by the school/teachers OR external providers that come into the school?": "15d_orchestras_teachers_or_external",
    "15.d.i. Please tell us the names of the providers (organisations or freelance creative practitioners).": "15di_orchestra_provider_names",
    "15.e. Are the choirs or vocal ensembles run by the school/teachers OR external providers that come into the school?": "15e_choir_vocal_ensembles_internal_external",
    "15.e.i. Please tell us the names of the providers (organisations or freelance creative practitioners)." : "15ei_choir_external_org_names",
    "15.f. Are the dance groups run by the school/teachers OR external providers that come into the school?": "15f_dance_groups_internal_external",
    "15.f.i. Please tell us the names of the providers (organisations or freelance creative practitioners).": "15fi_dance_group_external_org_names",
    "15.g. Are the drama groups run by the school/teachers OR external providers that come into the school?": "15g_drama_groups_internal_external",
    "15.g.i. Please tell us the names of the providers (organisations or freelance creative practitioners).": "15gi_drama_group_external_org_names",
    "15.h. Are the D&T groups run by the school/teachers OR external providers that come into the school?": "15h_dt_groups_internal_external",
    "15.h.i. Please tell us the names of the providers (organisations or freelance creative practitioners).": "15hi_dt_groups_external_org_names",
    "15.i. Are the digital media groups run by the school/teachers OR external providers that come into the school?": "15i_digital_media_internal_external",
    "15.i.i. Please tell us the names of the providers (organisations or freelance creative practitioners).": "15ii_digital_media_external_org_names",
    "15.j. Are the art groups run by the school/teachers OR external providers that come into the school?": "15j_art_groups_internal_external",
    "15.j.i. Please tell us the names of the providers (organisations or freelance creative practitioners).": "15ji_art_group_external_org_names",
    "16. Does your school offer Arts Award?": "16_arts_award",
    "16.a. Are any of your teachers qualified as Arts Award Advisors OR do you partner with a local organisation?": "16a_teacher_arts_award_advisors_or_local_org",
    "16.a.i. Which organisation(s) do you partner with?": "16ai_arts_award_external_org_names",
    "17. Does your school have an arts council or school council focused on the arts?": "17_arts_council",
    "18. In academic year 2022/23, did your school invite organisations or creative practitioners into the school to deliver arts performances, workshops, or other creative activities?": "18_external_orgs_arts_performances",
    "18.a. What are the subject areas of the organisations or creative practitioners that are invited into school? Tick all that apply.": "18a_arts_performance_external_org_subject_areas",
    "18.b. Please tell us the names of the companies or creative practitioners that come and work in your school.": "18b_arts_performance_external_org_names",
    "19. Does your school take pupils on arts trips outside the school?": "19_arts_trips",
    "19.a. Typically, how are your school's arts trips funded?": "19a_arts_trips_funding",
    "19.a.i. Please use this space to provide any further information about how your school's art trips are funded, e.g. if certain trips are always core funded." : "19ai_arts_trips_funding_details",
    "20. Which of the following did you undertake in academic year 2022/23?": "20_trips_undertaken_22_23",
    "20.a. If you selected Other art trips, please specify:": "20a_arts_trips_other_details",
    "20.b. Were these theatre trips to see a play or musical to locations:": "20b_theatre_trip_locations", 
    "20.b.i. Which Key Stage(s) took part in these theatre trips?": "20bi_theatre_trip_key_stages", 
    "20.c. Were these concert trips to locations:": "20c_concert_trip_locations",
    "20.c.i. Which Key Stage(s) took part in these concert trips?": "20ci_concert_trip_key_stages",
    "20.d. Were these cinema trips to locations:": "20d_cinema_trip_locations",
    "20.d.i. Which Key Stage(s) took part in these cinema trips?": "20di_cinema_trip_key_stages",
    "20.e. Were these gallery trips to locations:": "20e_gallery_trip_locations",
    "20.e.i. Which Key Stage(s) took part in these gallery trips?": "20ei_gallery_trip_key_stages",
    "20.f. Were these dance trips to locations:": "20f_dance_trip_locations", 
    "20.f.i. Which Key Stage(s) took part in these dance trips?": "20fi_dance_trip_key_stages",
    "20.g. Were these museum trips to locations:": "20g_museum_trip_locations",
    "20.g.i. Which Key Stage(s) took part in these museum trips?": "20gi_museum_trip_key_stages",
    "20.h. Were these heritage site trips to locations:": "20h_heritage_trip_locations",
    "20.h.i. Which Key Stage(s) took part in these heritage site trips?": "20hi_heritage_trip_key_stages",
    "20.i. Were these gaming experience trips to locations:": "20i_gaming_trip_locations",
    "20.i.i. Which Key Stage(s) took part in these gaming experience trips?": "20ii_gaming_trip_key_stages",
    "20.j. Were these library trips to locations:": "20j_library_trip_locations",
    "20.j.i. Which Key Stage(s) took part in these library trips?": "20ji_library_trip_key_stages",
    "20.k. Were these community trips to locations:": "20k_community_trip_locations",
    "20.k.i. Which Key Stage(s) took part in these local community trips?": "20ki_community_trip_key_stages",
    "21. Regarding access, diversity, and inclusion, does your school experience any barriers or challenges in encouraging, recruiting, or gaining permissions for pupils to go on trips out of school?": "21_barriers_encouraging_recruiting_permissions_trips",
    "21.a. Please briefly describe the barriers or challenges you face.": "21a_barriers_encouraging_recruiting_permissions_trips_details",
    "22. Regarding access, diversity, and inclusion, does your school experience any barriers or challenges with the experience or facilities at host venues when taking pupils on trips out of the school?": "22_barriers_facilities_host_venues_trips",
    "22.a. Please briefly describe the barriers or challenges you face.": "22a_barriers_facilities_host_venues_trips_details",
    "23. Is your school part of any national programmes delivered by arts institutions or organisations?": "23_national_programmes",
    "23.a. What national programmes does your school take part in?": "23a_national_programmes_details",
    "24. Does your school have a partnership with any local arts organisations?": "24_partnerships_external_orgs",
    "24.a. Could you tell us a little about these partnerships and their benefits to your school?": "24a_partnerships_external_orgs_details",
    "25. Does your school have a partnership with any other local schools to support the arts curriculum?": "25_partnerships_local_schools",
    "25.a. Could you tell us a little about these partnerships and their benefits to your school?": "25a_partnerships_benefits",
    "26. Is your school part of any local/community-based arts programmes?": "26_community_based_arts_programmes",
    "26.a. Could you tell us a little about these programmes?": "26a_community_based_arts_programmes_details",
    "27. Are there any other arts programmes or projects your school has been a part of that you haven't mentioned yet?": "27_other_arts_programmes_partnerships",
    "27.a. Could you tell us a little about these programmes?": "27a_other_arts_programmes_partnerships_details",
    "28. Are you able to find arts delivery partners who reflect or understand the diversity of your pupils?": "28_partnerships_diversity_challenges",
    "28.a. Please briefly describe any challenges you have faced in finding arts partners who reflect or understand the diversity of your pupils.": "28_partnerships_diversity_challenges_details",
    "29. Does your school give pupils opportunities to engage with professionals or practitioners in the arts?": "29_pupil_practitioner_engagement_opportunities",
    "30. Does your school have someone able to give specialist advice on career pathways into the arts?": "30_specialist_creative_career_advice",
    "30.a. Please specify the role  hey have in your school.": "30a_specialist_creative_career_advice_details",
    "31. Do you hold data on the number of your pupils who progress on to study arts subjects in further or higher education?": "31_data_pupil_progression_creative_education",
    "31.a. If possible, please provide details of the % cohort who continued to study arts subjects at further or higher education in 2022.": "31a_percentage_pupil_progression_creative_education",
    "32. Does your school support teachers' CPD in arts subjects?": "32_supporting_teacher_cpd",
    "32.a. What support does your school offer?": "32a_supporting_teacher_cpd_details",
    "33. Do you consider your school to lack any particular areas of expertise in delivering the arts curriculum?": "33_school_lacking_expertise_arts_curriculum",
    "34. Do you consider your school to be an exemplar in any areas of the arts curriculum?": "34_school_exemplar_arts_curriculum",
    "35. Would you like to tell us anything else about your school's arts curriculum and enrichment or extra-curricular activities?": "35_other_school_arts_offering_details"
}

def load_raw_survey_data():
    data = pd.read_excel(SURVEY_PATH).rename(columns=SURVEY_QUESTION_MAPPER).drop(columns=['03a_other']).set_index('unique_response_number')
    return data

def count_by_school_type(data):
    school_counts = data.groupby('03_school_type').size().reset_index(name='Count')
    return school_counts

def calculate_percentage(row, counts_by_school_type):
    school_type = row['School Type']
    count = row['Count']
    total_count = counts_by_school_type.loc[counts_by_school_type['03_school_type'] == school_type, 'Count'].iloc[0]
    result = ((count/total_count)*100).round(0).astype(int)
    return result

def drop_duplicates(data):
    # Manually select duplicate schools for now 
    duplicates = [
        '1132118-1132100-122057142',
        '1132118-1132100-122043869',
        '1132118-1132100-122294596',
        '1132118-1132100-121181859'
    ] 
    deduped = data.drop(duplicates)

    return deduped
