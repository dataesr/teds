import requests
import pandas as pd
from code_utils.utils import aplatir

def get_open_alex_data(cached_openalex_data,doi):
    if pd.isna(doi)==False:
        if doi in cached_openalex_data:
            return cached_openalex_data[doi]
        else:
            url=f"https://api.openalex.org/works?filter=doi:{doi}"
            response = requests.get(url)
            try:
                data = response.json()

                if 'results' in data.keys():
                    cached_openalex_data[doi] = data.get('results')
                else:
                    cached_openalex_data[doi] = []
            except:
                pass          

def get_countries_concepts_sdg(cached_openalex_data,row):
    doi=row.doi
    data=cached_openalex_data[doi]
    if data!=[]:
        authors=data[0].get('authorships')
        if authors!=[]:
            countries=list(set(aplatir([author.get('countries') for author in authors]))) 
        else:
            countries=[None]

        concepts=data[0].get('concepts')
        if concepts!=[]:
            concepts_names=[{'name': concept.get('display_name')} for concept in concepts]
        else:
            concepts_names=None

        sdgs=data[0].get('sustainable_development_goals')
        if sdgs!=[]:
            sdgs_ids_names=[{'id': str(sdg.get('id'))[-2:].replace("/",""), 'name': sdg.get('display_name')} for sdg in sdgs]
        else:
            sdgs_ids_names=None
    else:
        return [None],None,None,None
    return countries,concepts_names,sdgs_ids_names,data[0].get('publication_year')

def get_publi_not_in_ipcc(dois,dict_year,year_counts,year_counts_not_ipcc):
    climat_concepts=['climate change','environmental science','climatology','meteorology','global warming','ecology','climate model','greenhouse gas','effects of global warming on oceans','greenhouse effect', 'abrupt climate change']
    url=f"https://api.openalex.org/works/random"
    response = requests.get(url)
    data = response.json()
    year = data.get('publication_year')
    if ((year<=2021)&(data.get('doi') not in dois)&(pd.isna(data.get('doi'))==False)&(pd.isna(data.get('title'))==False)&(data.get('sustainable_development_goals')!=[])&(data.get('concepts')!=[])&(year in list(year_counts.keys()))):
        concepts_name=[str(x.get('display_name')).lower() for x in data.get('concepts')]
        if any(concept in climat_concepts for concept in concepts_name):
            if year in list(dict_year.keys()):
                if year_counts[year]>year_counts_not_ipcc[year]:
                    year_counts_not_ipcc[year]+=1
                    dict_year[year].append({"doi": data.get('doi'), "year": year, "title": data.get('title'), "sdg": data.get('sustainable_development_goals'), "concepts": data.get('concepts')})
            else:
                year_counts_not_ipcc[year]=1
                dict_year[year]=[{"doi": data.get('doi'), "year": year, "title": data.get('title'), "sdg": data.get('sustainable_development_goals'), "concepts": data.get('concepts')}]

