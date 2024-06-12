

import os 
import sys
import pandas as pd 
import http.client
from time import sleep

# print('cwd is %s' %(os.getcwd()))
# scriptdir = os.path.dirname(os.path.realpath(__file__))
# print('dir containing script is %s' % (scriptdir))
# print('============\ncwd is %s' %(os.getcwd()))
# os.chdir(scriptdir)
# print('============\ncwd after change to script dir is %s' %(os.getcwd()))

# TOP_DIR=os.path.abspath("..")
# sys.path.append("../..")

DATA_DIR = os.path.join('data', 'census')

def get_data(url):
    url = f'{url}'
    retries = 3
    while retries > 0:
        try:
            data = pd.read_csv(url)
            retries = 0
        except http.client.RemoteDisconnected as e:
            retries -= 1
            if retries <=0:
                raise e
            sleep(5)

    if data.index.size == 25000:
        raise RuntimeError('Maxed out request to NOMIS (%d rows)', data.index.size)
    return data

if __name__ == '__main__':

    population_data = get_data('https://www.nomisweb.co.uk/api/v01/dataset/NM_31_1.data.csv?geography=1811939401&date=latest&sex=7&age=0,24,5&measures=20100,20301')

    population_data.reset_index().to_csv(os.path.join(DATA_DIR, 'population.csv'), index=False)

    projected_population = get_data('https://www.nomisweb.co.uk/api/v01/dataset/NM_2006_1.data.csv?geography=1820328007&projected_year=2018...2043&gender=0&c_age=200,201,5&measures=20100')

    projected_population.reset_index().to_csv(os.path.join(DATA_DIR, 'projected_population.csv'), index=False)
