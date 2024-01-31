import bibtexparser
import pandas as pd

def read_bib_file(path, verbose=False):
    if verbose:
        print(f'reading {path} ...')
    with open(path, 'r', encoding='utf-8') as fichier:
        contenu_bib = fichier.read()
    parser = bibtexparser.bparser.BibTexParser(common_strings=True)
    bib_database = bibtexparser.loads(contenu_bib, parser=parser)
    return bib_database

def read_bib_wgi(verbose=False):
    wgi=[]
    dataframes_i={}
    for i in ['01','02','03','04','05','06','07','08','09','10','11','12']:
        df=pd.DataFrame(read_bib_file(f"../IPCC_bibliography/AR6/WG1/IPCC_AR6_WGI_References_Chapter{i}.bib", verbose).entries)
        df['wg']='wg1'
        df['chap']=f"wg1_chap_{i}"
        wgi.append(len(df.doi.dropna())/len(df))
        df_name = f'df_i_{i}'
        dataframes_i[df_name] = df
    df_wgi = pd.concat(list(dataframes_i.values()), ignore_index=True)
    return df_wgi
