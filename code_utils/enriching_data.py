import requests
import pandas as pd
from code_utils.utils import aplatir

def get_open_alex_data(json_OA,doi):
    if pd.isna(doi)==False:
        url=f"https://api.openalex.org/works?filter=doi:{doi}"
        response = requests.get(url)
        data = response.json()
        if 'results' in data.keys():
            json_OA.append({"doi": doi, "results": data.get('results')})
        else:
            json_OA.append({"doi": doi, "results": []})

def get_countries_concepts_sdg(df,row):
    doi=row.doi
    data=df[df.doi==doi]
    i=df[df.doi==doi].index[0]
    if data['results'][i]!=[]:
        authors=data['results'][i][0].get('authorships')
        if authors!=[]:
            countries=list(set(aplatir([author.get('countries') for author in authors]))) 
        else:
            countries=[None]

        concepts=data['results'][i][0].get('concepts')
        if concepts!=[]:
            concepts_names=[{'name': concept.get('display_name')} for concept in concepts]
        else:
            concepts_names=None

        sdgs=data['results'][i][0].get('sustainable_development_goals')
        if sdgs!=[]:
            sdgs_ids_names=[{'id': str(sdg.get('id'))[-2:].replace("/",""), 'name': sdg.get('display_name')} for sdg in sdgs]
        else:
            sdgs_ids_names=None
    else:
        return [None],None,None
    return countries,concepts_names,sdgs_ids_names

def get_publi_not_in_ipcc(dois,dict_year,year_counts,year_counts_not_ipcc):
    url=f"https://api.openalex.org/works/random"
    response = requests.get(url)
    data = response.json()
    year = data.get('publication_year')
    if ((year<=2021)&(data.get('doi') not in dois)&(pd.isna(data.get('title'))==False)&(data.get('sustainable_development_goals')!=[])&(data.get('concepts')!=[])&(year in list(year_counts.keys()))):
        if year in list(dict_year.keys()):
            year_counts_not_ipcc[year]+=1
        else:
            year_counts_not_ipcc[year]=1
        if (year_counts_not_ipcc[year]<year_counts[year]):
            if year in list(dict_year.keys()):
                dict_year[year].append({"doi": data.get('doi'), "year": year, "title": data.get('title'), "sdg": data.get('sustainable_development_goals'), "concepts": data.get('concepts')})
            else:
                dict_year[year]=[{"doi": data.get('doi'), "year": year, "title": data.get('title'), "sdg": data.get('sustainable_development_goals'), "concepts": data.get('concepts')}]
    
