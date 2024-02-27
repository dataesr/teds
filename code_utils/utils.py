import pandas as pd
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
import re

def aplatir(conteneurs):
    return [conteneurs[i][j] for i in range(len(conteneurs)) for j in range(len(conteneurs[i]))]

def wg_chap_to_dict(row):
    list_chap=[]
    if isinstance(row['wg'],list):
        for i in range(len(row['wg'])):
            list_chap.append({'name': row['chap'][i], 'wg': row['wg'][i].replace('wg',''), 'chap': int(row['chap'][i][-2:].replace('_','')), 'freq_ipcc': row['freq']})
    else:
        list_chap.append({'name': row['chap'], 'wg': row['wg'].replace('wg',''), 'chap': int(row['chap'][-2:].replace('_','')), 'freq_ipcc': row['freq']})
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

def remove_too_long(d):
    assert(isinstance(d, dict))
    current_fields = list(d.keys())
    for f in current_fields:
        if isinstance(d[f], str):
            if len(d[f]) > 1000:
                logger.debug(f"shortening str field {f} as too long !")
                d[f] = d[f][0:1000]+'...'
        elif isinstance(d[f], list):
            if len(d[f]) > 50:
                logger.debug(f"shortening list field {f}  as too long !")
                d[f] = d[f][0:50]
        elif isinstance(d[f], dict):
            d[f]=remove_too_long(d[f].copy())
    return d

def type_score(x):
    openalex_concepts_list = x
    for concept in openalex_concepts_list:
        current_score = float(concept.get('score', 0.0))
        concept['score'] = current_score

def preprocess(text):
    text = re.sub(r'[^\w\s\']',' ', text)
    text = re.sub(' +', ' ', text)
    return text.strip().lower() 
    
def get_wg(wg_chap,wg1=False,wg2=False,wg2_cross=False,wg3=False):
    wgs=[x.get("wg") for x in wg_chap]
    if wg1 & wg2 & wg2_cross & wg3 :
        if [x for x in ['1','2','2_cross','3'] if x in wgs]==['1','2','2_cross','3']:
            return True
        else:
            return False
    if wg1 & wg2 & wg2_cross:
        if [x for x in ['1','2','2_cross'] if x in wgs]==['1','2','2_cross']:
            return True
        else:
            return False
    if wg1 & wg2:
        if [x for x in ['1','2'] if x in wgs]==['1','2']:
            return True
        else:
            return False
    if wg1 & wg3:
        if [x for x in ['1','3'] if x in wgs]==['1','3']:
            return True
        else:
            return False
    if wg3 & wg2 & wg2_cross:
        if [x for x in ['3','2','2_cross'] if x in wgs]==['3','2','2_cross']:
            return True
        else:
            return False
    if wg2 & wg3:
        if [x for x in ['2','3'] if x in wgs]==['2','3']:
            return True
        else:
            return False
    if wg1:
        if [x for x in ['1'] if x in wgs]==['1']:
            return True
        else:
            return False
    if wg2 & wg2_cross:
        if [x for x in ['2','2_cross'] if x in wgs]==['2','2_cross']:
            return True
        else:
            return False
    if wg2 :
        if [x for x in ['2'] if x in wgs]==['2']:
            return True
        else:
            return False
    if wg2_cross:
        if [x for x in ['2_cross'] if x in wgs]==['2_cross']:
            return True
        else:
            return False
    if wg3:
        if [x for x in ['3'] if x in wgs]==['3']:
            return True
        else:
            return False