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

def bool_topics(climat_topics,topics_name):
    for x in climat_topics:
        for y in topics_name: 
            if str(y).lower().find(str(x).lower())>0:
                return False
    return True

def get_open_alex_data_not_in_references(dois,cached_openalex_data_not_ipcc,year_counts,year_counts_not_ipcc,year,ipcc="ipcc"):
    if ipcc=="ipcc":
        climat_topics=['climate change','ecological','climate variability','flood risk assessment','cryospheric studies','paleoclimatology','cyclones research','plant water relations','carbon dynamics','ecosystem','sustainability','atmospheric processes','atmospheric chemistry','disaster management','environment','ice dynamics','drought analysis','land use','agricultural risk','air quality','biodiversity','atmospheric ozone','ocean acidification','water resource','water-energy-food','sustainability','sustainable','resilience','aquaculture studies','marine management','marine dynamics','climate responses','urban green space','building energy','forest management','plant responses to elevated co2','atmospheric aerosols','urban heat island','renewable energy','island studies','carbon dioxide capture technologies','soil carbon','climate adaptation','landslides','vehicle emissions and performance']
        #climat_topics=['climate change','ecological','global methane emissions and impacts','impact of ocean acidification on marine ecosystems','arctic sea ice variability and decline','environmental impact','climate ethics','climate and hydrological cycle','global energy transition','environmental behavior','influence of climate','urban heat islands and mitigation strategies','impact on climate','environmental policies','carbon dioxide capture and storage technologies','soil carbon dynamics and nutrient cycling in ecosystems','sustainable development','environmental governance']
    else:
        climat_topics=['biodiversity','environmental','marine ecosystems','plant and animal studies','species distribution and climate change','marine biology','ocean acidification effects and responses','marine and fisheries research','indigenous studies and ecology','sustainability','ecosystem services','land use']
    url=f"https://api.openalex.org/works?filter=has_doi:true,concepts_count:>0,publication_year:{year}&sample=200&per-page=200"
    response = requests.get(url)
    data0 = response.json().get('results')
    print(f"plus que {year_counts[year] - year_counts_not_ipcc[year]} publications pour completer l'année {year}")
    for i in range(len(data0)):
        data=data0[i]
        if 'topics' in list(data.keys()):
            if data.get('topics')!=[]:
                topics_name=[str(x.get('display_name')).lower() for x in data.get('topics')]
                if ((data.get('doi') not in dois)&(pd.isna(data.get('title'))==False)&((data.get('topics'))!=[])&((data.get('locations'))!=[])&((bool_topics(climat_topics,topics_name))==True)):
                    for x in data.get('locations'):
                        if isinstance(x,dict):
                            if 'source' in list(x.keys()):
                                if isinstance(x.get('source'),dict):
                                    if (('display_name' in list(x.get('source')))&('issn_l' in list(x.get('source')))&('type' in list(x.get('source')))):
                                        if ((pd.isna(x.get('source').get('display_name'))==False)&(x.get('source').get('type')=='journal')&(pd.isna(x.get('source').get('issn_l'))==False))&(pd.isna(x.get('source').get('display_name'))==False):
                                            year_counts_not_ipcc[year]+=1
                                            cached_openalex_data_not_ipcc[year].append(data)
                                            dois.append(data.get('doi'))
                                            break


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
            name=[(author.get('author').get('display_name'),author.get('countries')) for author in authors]
            institutions=[author.get('institutions') for author in authors]
            if len(institutions)>0:
                rors=[(y.get('ror'),y.get('country_code')) for x in institutions for y in x ]
                institutions_names=[(y.get('display_name'),y.get('country_code')) for x in institutions for y in x ]
            else:
                rors=[None]
                institutions_names=[None]
        else:
            countries=[None]
            name=[None]
            rors=[None]
            institutions_names=[None]
        

        concepts=data.get('concepts')
        if concepts!=[]:
            concepts_names=[concept.get('display_name') for concept in concepts]
        else:
            concepts_names=None

        locations=data.get('locations')
        if (locations!=[]):
            s=0
            for k in range(len(locations)):
                if pd.isna(locations[k].get('source'))==False:
                    if locations[k].get('source').get('type')=='journal':
                        s+=1
                        locations_names=locations[k].get('source').get('display_name')
                        locations_id=locations[k].get('source').get('issn_l') 
                        break
            if s==0:
                locations_names=None
                locations_id=None
        else:
            locations_names=None
            locations_id=None

        if topics!=[]:
            topics_names=[topic.get('display_name') for topic in topics]
        else:
            topics_names=None

        sdgs=data.get('sustainable_development_goals')
        if sdgs!=[]:
            sdgs_ids_names=[{'id': str(sdg.get('id'))[-2:].replace("/",""), 'name': sdg.get('display_name')} for sdg in sdgs]
        else:
            sdgs_ids_names=None
    else:
        return [None],None,None,None,None,None,False,None,None,None,None,None,None,None,None
    return countries,concepts_names,sdgs_ids_names,data.get('publication_year'),topics_names,doi,True,data.get('title'),name,rors,institutions_names,locations_names,locations_id,data.get('type'),data.get('type_crossref')