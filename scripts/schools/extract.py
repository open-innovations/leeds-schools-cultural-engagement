

import os 
import pandas as pd 
from time import sleep
from io import BytesIO
import http.client
import urllib.request
import zipfile

DATA_DIR = os.path.join('data', 'dfe', 'ks4-performance')

def get_data_from_zipfile(url, file, filename):
    zip_url = f'{url}'
    retries = 3
    while retries > 0:
        try:
            with urllib.request.urlopen(zip_url) as response:
                if response.status == 200:
                    retries = 0
                    zip_data = response.read()
                else:
                    raise Exception(f"Failed to download file: Status code {response.status}")
        except urllib.error.URLError as e:
            retries -= 1
            if retries <= 0:
                raise e
            sleep(5)
    
    with zipfile.ZipFile(BytesIO(zip_data)) as z:
        with z.open(f'{file}/{filename}') as csvfile:
            data = pd.read_csv(csvfile)
    
    return data

def get_excel_data(url):
    retries = 3
    while retries > 0:
        try:
            with urllib.request.urlopen(url) as response:
                if response.status == 200:
                    retries = 0
                    excel_data = response.read()
                else:
                    raise Exception(f"Failed to download file: Status code {response.status}")
        except urllib.error.URLError as e:
            retries -= 1
            if retries <= 0:
                raise e
            sleep(5)
    
    # Read the Excel file from the downloaded bytes
    data = pd.read_excel(BytesIO(excel_data), sheet_name=None)
    
    return data

def save_excel_as_csv(excel_data):
    for sheet_name, df in excel_data.items():
        df.to_csv(os.path.join(DATA_DIR, 'arts_mark_settings_24.csv'), index=False)

if __name__ == '__main__':

    national_data = get_data_from_zipfile('https://content.explore-education-statistics.service.gov.uk/api/releases/90c95fb2-f2a1-4723-aba8-09c4b6e231a5/files','data', '2223_national_data_revised.csv')
    national_data.to_csv(os.path.join(DATA_DIR,'2223_national_data_revised.csv'), index=False)

    la_data = get_data_from_zipfile('https://content.explore-education-statistics.service.gov.uk/api/releases/90c95fb2-f2a1-4723-aba8-09c4b6e231a5/files','data', '2223_la_data_revised.csv')
    national_data.to_csv(os.path.join(DATA_DIR,'2223_la_data_revised.csv'), index=False)

    subject_la_data = get_data_from_zipfile('https://content.explore-education-statistics.service.gov.uk/api/releases/90c95fb2-f2a1-4723-aba8-09c4b6e231a5/files','data', '2223_subject_pupil_level_la_data_revised.csv')
    national_data.to_csv(os.path.join(DATA_DIR,'2223_subject_pupil_level_la_data_revised.csv'), index=False)

    arts_mark_settings = get_excel_data('https://www.artsmark.org.uk/media/2325/download?attachment')
    save_excel_as_csv(arts_mark_settings)
