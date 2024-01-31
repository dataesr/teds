import bibtexparser
import pandas as pd
from glutton import get_doi_glutton  

def read_bib_file(path, verbose=False):
    if verbose:
        print(f'reading {path} ...')
    with open(path, 'r', encoding='utf-8') as fichier:
        contenu_bib = fichier.read()
    parser = bibtexparser.bparser.BibTexParser(common_strings=True)
    bib_database = bibtexparser.loads(contenu_bib, parser=parser)
    return bib_database

def read_bib_wg(wgs,k,verbose=False):
    for i in wgs[k][f'listdir{k}']:
        df=pd.DataFrame(read_bib_file(f"../IPCC_bibliography/AR6/WG{k}/{i}", verbose).entries)
        df['wg']='wg{k}'
        df['chap']=f"wg1_chap_{wgs[k][f'listdir{k}'][-9:].replace('.bib','').replace('ter','')}"
        wgs[k][f'wg{k}'].append(len(df.doi.dropna())/len(df))
        if k in ['2','2_CROSS']:
            df.loc[pd.isna(df.doi),'doi']=df.loc[pd.isna(df.doi),:].progress_apply(get_doi_glutton, axis=1)
        df_name = f"df_{i[-9:].replace('.bib','').replace('ter','')}"
        wgs[k][f'dataframes_{k}'][df_name] = df
    df_wg = pd.concat(list(wgs[i][f'dataframes_{i}'].values()), ignore_index=True)
    return df_wg

