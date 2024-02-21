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

def get_open_alex_data_not_in_references(dois,cached_openalex_data_not_ipcc,year_counts,year_counts_not_ipcc,year):
    climat_concepts=['climate change','environmental science','climatology','meteorology','global warming','ecology','climate model','greenhouse gas','effects of global warming on oceans','greenhouse effect', 'abrupt climate change']
    url=f"https://api.openalex.org/works?filter=has_doi:true,concepts_count:>0,publication_year:{year}&sample=200&per-page=200"
    response = requests.get(url)
    data0 = response.json().get('results')
    print(f"plus que {year_counts[year] - year_counts_not_ipcc[year]} publications pour completer l'année {year}")
    for i in range(len(data0)):
        data=data0[i]
        concepts_name=[str(x.get('display_name')).lower() for x in data.get('concepts')]
        if ((data.get('doi') not in dois)&(pd.isna(data.get('title'))==False)&(data.get('topics')!=[])&((any(concept in climat_concepts for concept in concepts_name))==False)):
            year_counts_not_ipcc[year]+=1
            cached_openalex_data_not_ipcc[year].append(data)
            dois.append(data.get('doi'))


def get_countries_concepts_sdg(cached_openalex_data,row=True,ipcc=True,i=0):
    if ipcc:
        doi=row.doi
        if len(cached_openalex_data[doi])==0:
            topics=[]
            data=[]
        elif (len(cached_openalex_data[doi])>1)&('topics' not in list(cached_openalex_data[doi][0].keys())):
            topics=cached_openalex_data[doi][1].get('topics')
            data=cached_openalex_data[doi][1]
        elif (len(cached_openalex_data[doi])==1)&('topics' in list(cached_openalex_data[doi][0].keys())):
            topics=cached_openalex_data[doi][0].get('topics')
            data=cached_openalex_data[doi][0]
        else:
            topics=[]
            data=cached_openalex_data[doi][0]
    else:
        if isinstance(cached_openalex_data[i],list):
            if (len(cached_openalex_data[i])>1)&('topics' not in list(cached_openalex_data[i][0].keys())):
                topics=cached_openalex_data[i][1].get('topics')
                data=cached_openalex_data[i][1]
            if (len(cached_openalex_data[i])==0)&('topics' in list(cached_openalex_data[i][0].keys())):
                topics=cached_openalex_data[i][0].get('topics')
                data=cached_openalex_data[i][0]
        else:
            data=cached_openalex_data[i]
            if ('topics' in list(data.keys())):
                topics=data.get('topics')
            else:
                topics=[]
        doi=data.get('doi')
    if (data!=[]):
        authors=data.get('authorships')
        if authors!=[]:
            countries=list(set(aplatir([author.get('countries') for author in authors]))) 
        else:
            countries=[None]

        concepts=data.get('concepts')
        if concepts!=[]:
            concepts_names=[{'name': concept.get('display_name')} for concept in concepts]
        else:
            concepts_names=None

        if topics!=[]:
            topics_names=[{'name': topic.get('display_name')} for topic in topics]
        else:
            topics_names=None

        sdgs=data.get('sustainable_development_goals')
        if sdgs!=[]:
            sdgs_ids_names=[{'id': str(sdg.get('id'))[-2:].replace("/",""), 'name': sdg.get('display_name')} for sdg in sdgs]
        else:
            sdgs_ids_names=None
    else:
        return [None],None,None,None,None,None,False
    return countries,concepts_names,sdgs_ids_names,data.get('publication_year'),topics_names,doi,True