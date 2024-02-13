import pandas as pd

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
    
