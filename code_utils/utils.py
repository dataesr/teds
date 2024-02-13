import os
import sys
import pandas as pd
import concurrent.futures
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)
from code_utils.enriching_data_OpenAlex import get_publi_not_in_references


def aplatir(conteneurs):
    return [conteneurs[i][j] for i in range(len(conteneurs)) for j in range(len(conteneurs[i]))]

def wg_chap_to_dict(row):
    list_chap=[]
    for i in range(len(row['wg'])):
        list_chap.append({'name': row['chap'][i], 'wg': row['wg'][i].replace('wg',''), 'chap': int(row['chap'][i][-2:].replace('_','')), 'freq_ipcc': row['freq']})
    return list_chap

def get_doi_cleaned(x):
    low_x=str(x).lower()
    if pd.isna(x):
        return None
    elif low_x.find('10.')>=0:
        split1=f"10.{low_x.split('10.',1)[1]}"
        split2=split1.split(' ')[0]
        split3=split2.split('\n')[0]
        return split3.rstrip('.')
    else:
        return None
    
def parallel_execution(dois, dict_year, year_counts, year_counts_not_ipcc, n_iterations):
    while sum(list(year_counts_not_ipcc.values())) < n_iterations:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(get_publi_not_in_ipcc, dois, dict_year, year_counts, year_counts_not_ipcc) for _ in range(n_iterations - sum(list(year_counts_not_ipcc.values())))]
            concurrent.futures.wait(futures)