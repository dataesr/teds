import pandas as pd
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
import re
from tokenizers import normalizers
from tokenizers.normalizers import BertNormalizer, Sequence, Strip
from tokenizers import pre_tokenizers
from tokenizers.pre_tokenizers import Whitespace
import string

def aplatir(conteneurs):
    return [conteneurs[i][j] for i in range(len(conteneurs)) for j in range(len(conteneurs[i]))]

def wg_chap_to_dict(row):
    list_chap=[]
    if isinstance(row['wg'],list):
        for i in range(len(row['wg'])):
            list_chap.append({'name': row['chap'][i], 'wg': row['wg'][i].replace('wg',''), 'chap': int(row['chap'][i][-2:].replace('_',''))})
    else:
        list_chap.append({'name': row['chap'], 'wg': row['wg'].replace('wg',''), 'chap': int(row['chap'][-2:].replace('_',''))})
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

def get_countries(row):
    if (isinstance(row.countries_x,list)==False)&(isinstance(row.countries_y,list)==False):
        return None
    elif (isinstance(row.countries_x,list))&(isinstance(row.countries_y,list)==False):
        return row.countries_x
    elif (isinstance(row.countries_x,list)==False)&(isinstance(row.countries_y,list)):
        return row.countries_y
    else:
        return row.countries_x

def get_year_ipbes(date_str):
    if (re.match("^\d{4}-\d{2}-\d{2}$", date_str)):
        return date_str[:4]
    elif (re.match("^\d{4}-\d{2}-\d{1}$", date_str)):
        return date_str[:4]
    elif (re.match("^\d{4}-\d{1}-\d{2}$", date_str)):
        return date_str[:4]
    elif (re.match("^\d{4}-\d{1}-\d{1}$", date_str)):
        return date_str[:4]
    elif (re.match("^\d{4}\s[a-zA-Z]+$", date_str)):
        return date_str[:4] 
    elif (re.match("^\d{4}/\d{2}/\d{2}$", date_str)):
        return date_str[:4] 
    elif (re.match("^\d{4}/\d{1}/\d{2}$", date_str)):
        return date_str[:4] 
    elif (re.match("^\d{4}/\d{2}/\d{1}$", date_str)):
        return date_str[:4] 
    elif (re.match("^\d{4}/\d{1}/\d{1}$", date_str)):
        return date_str[:4] 
    elif (re.match("^\d{4}\s(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{1,2}$", date_str)):
        return date_str[:4]
    elif (re.match("^\d{4}/(?:0?[1-9]|1[0-2])$", date_str)):
        return date_str[:4] 
    elif (re.match("^\d{4}-(?:0?[1-9]|1[0-2])$", date_str)):
        return date_str[:4] 
    else:
        return date_str[-4:]

def get_year_ipcc(date_str):
    if (re.match("^(?:April|September)\s\d{4}$", str(date_str))):
        return date_str[-4:]
    elif (re.match("^\d{4}(?:a|b|c|d|b:|.|submitted)$", str(date_str))):
        return date_str[:4] 
    elif (re.match("^\((\d{4})\).\xa0$", str(date_str))):
        return date_str[1:5] 
    elif str(date_str).lower() in ['accepted','submitted','in press','n.d.','in review','forthcoming','accepted/in press','in preparation','under review']:
        return None
    elif re.match("^\d{4}a. $", str(date_str)):
        return str(date_str)[:4]
    elif re.match("^\d{4} submitted$", str(date_str)):
        return date_str[:4] 
    elif re.match("^\xa0\d{4}.\xa0$", str(date_str)):
        return date_str[1:5] 
    elif re.match("^\d{4}. $", str(date_str)):
        return date_str[:4] 
    else:
        return date_str
    
def remove_punction(s: str) -> str:
    for p in string.punctuation:
        s = s.replace(p, ' ').replace('  ', ' ')
    return s.strip()

normalizer = Sequence([BertNormalizer(clean_text=True,
        handle_chinese_chars=True,
        strip_accents=True,
        lowercase=True), Strip()])
pre_tokenizer = pre_tokenizers.Sequence([Whitespace()])

def normalize(x, min_length = 0):
    normalized = normalizer.normalize_str(x)
    for c in ['\n', '<', '>', '$',"'","’"]:
        normalized = normalized.replace(c, ' ')
    normalized = remove_punction(normalized)
    normalized = re.sub(' +', ' ', normalized)
    # keep if digit alone
    return " ".join([e[0] for e in pre_tokenizer.pre_tokenize_str(normalized) if (len(e[0]) > min_length) or (e[0] in string.digits)])

def check_doi_glutton(row):
    if (row.year!='XXXX') & (row.year!='') & (row.year_OA!='') & (pd.isna(row.year)==False) & (pd.isna(row.year_OA)==False):
        if int(row.year) in [int(row.year_OA)-1,int(row.year_OA),int(row.year_OA)+1]:
            return True
        else:
            return False
    elif (row.year=='XXXX') | (row.year=='') | (row.year_OA=='') |(pd.isna(row.year)) | (pd.isna(row.year_OA)):
        return True
    else:
        return False




