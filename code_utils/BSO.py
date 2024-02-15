import pickle
import logging
import sys
import os
import pandas as pd 

module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)

FORMATTER = '%(asctime)s | %(name)s | %(levelname)s | %(message)s'


def get_formatter() -> logging.Formatter:
    formatter = logging.Formatter(FORMATTER)
    return formatter


def get_console_handler() -> logging.StreamHandler:
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(get_formatter())
    return console_handler

def get_logger(name: str = __name__, level: int = logging.DEBUG) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(get_console_handler())
    return logger

logger = get_logger(__name__)

def update_bso_publications():
    logger.debug('update bso publications files')
    df_bso = pd.read_csv('https://storage.gra.cloud.ovh.net/v1/AUTH_32c5d10cb0fe4519b957064a111717e3/bso_dump/bso-publications-latest.csv.gz', sep=';')
    bso_doi_dict = {}
    for row in df_bso.itertuples():
        if isinstance(row.doi, str) and isinstance(row.bso_country, str) and 'fr' in row.bso_country:
            bso_doi_dict[row.doi] = {}
            rors = []
            if isinstance(row.rors, str):
                rors = [r.split('/')[-1] for r in row.rors.split('|')]
            bso_doi_dict[row.doi]['rors'] = rors
            bso_local_affiliations = []
            if isinstance(row.bso_local_affiliations, str):
                bso_local_affiliations = [a for a in row.bso_local_affiliations.split('|')]
            bso_doi_dict[row.doi]['bso_local_affiliations'] = bso_local_affiliations
    logger.debug(f'writing {len(bso_doi_dict)} dois info from bso publications')
    pickle.dump(bso_doi_dict, open(module_path+f'\\IPCC_bibliography\\AR6\\structured_data\\bso_doi_dict.pkl', 'wb'))

def get_bso_publications():
    return pickle.load(open(module_path+f'\\IPCC_bibliography\\AR6\\structured_data\\bso_doi_dict.pkl', 'rb'))