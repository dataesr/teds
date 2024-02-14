import requests
import pandas as pd
import concurrent.futures
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

def get_publi_not_in_references(dois,dict_year,year_counts,year_counts_not_ipcc,year):
    climat_concepts=['climate change','environmental science','climatology','meteorology','global warming','ecology','climate model','greenhouse gas','effects of global warming on oceans','greenhouse effect', 'abrupt climate change']
    url=f"https://api.openalex.org/works?filter=has_doi:true,concepts_count:>0,publication_year:{year}&sample=200&per-page=200"
    response = requests.get(url)
    data0 = response.json().get('results')
    print(f"plus que {year_counts[year] - year_counts_not_ipcc[year]} publications pour completer l'année {year}")
    for i in range(len(data0)):
        data=data0[i]
        concepts_name=[str(x.get('display_name')).lower() for x in data.get('concepts')]
        if ((data.get('doi') not in dois)&(pd.isna(data.get('title'))==False)&(data.get('sustainable_development_goals')!=[])&((any(concept in climat_concepts for concept in concepts_name))==False)):
            year_counts_not_ipcc[year]+=1
            dict_year[year].append({"doi": data.get('doi'), "year": year, "title": data.get('title'), "sdg": data.get('sustainable_development_goals'), "concepts": data.get('concepts'), "topics": data.get('topics')})
            dois.append(data.get('doi'))

