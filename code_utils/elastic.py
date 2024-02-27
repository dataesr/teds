import os
from dotenv import load_dotenv
load_dotenv()
import requests
import base64
from elasticsearch import Elasticsearch
from urllib import parse
import pandas as pd
import matplotlib.pyplot as plt

passw = f"{os.getenv('ES_LOGIN_TEDS_BACK')}:{os.getenv('ES_PASSWORD_TEDS_BACK')}"
base64_bytes = passw.encode('ascii')
message_bytes = base64.b64encode(base64_bytes)
token = message_bytes.decode('ascii')
url = os.getenv('ES_URL')+'teds-bibliography/_search'

def get_from_es(body):
    return requests.post(url, json=body, headers={f'Authorization': f'Basic {token}'}).json()

def get_body(list_wg,terms=True,french=False):
    if terms:
        if french:
            body = {
                'size': 0,
                'query': {
                    'bool': {
                        'must': [
                                {"terms": {
                                    "ipcc.wg.keyword": list_wg,
                                    }
                                },  
                                {'match':{
                                    'countries.keyword':'FR'
                                    }  
                                }  
                            ],
                    }
                },
                'aggs': {
                    'by_countries': {
                        'terms': {
                            'field': 'countries.keyword', 'size': 20
                        },
                    }
                },
                'track_total_hits': True
            }
        else:
            body = {
                'size': 0,
                'query': {
                    'bool': {
                        'must': [
                                {"terms": {
                                    "ipcc.wg.keyword": list_wg,
                                    }
                                },    
                        ],
                    }
                },
                'aggs': {
                    'by_countries': {
                        'terms': {
                            'field': 'countries.keyword', 'size': 20
                        },
                    }
                },
                'track_total_hits': True
            }
    else:
        body = {
            'size': 0,
            'query': {
                'bool': {
                    'must': [{f'match': {'ipcc.wg.keyword': x}} for x in list_wg],
                }
            },
            'aggs': {
                'by_countries': {
                    'terms': {
                        'field': 'countries.keyword', 'size': 20
                    },
                }
            },
            'track_total_hits': True
        }
    res = get_from_es(body)
    return res

def plot_elastic(list_wg,terms=True,interfaces=False):
    if interfaces==False:
        res=get_body(list_wg,terms)
        data_counts={}
        for x in res.get('aggregations').get('by_countries').get('buckets'):
            #print(x.get('key'),x.get('doc_count')*100/res.get('hits').get('total').get('value'))
            data_counts[x.get('key')]=round(x.get('doc_count')*100/res.get('hits').get('total').get('value'),2)
        data_counts=pd.Series(data_counts)
        color_dict = {'FR': '#BE2125'}
        plt.figure(figsize=(24, 10))
        ax = data_counts[:20].plot(kind='bar', color=[color_dict.get(u, 'grey') for u in data_counts[:20].index], width=0.8)

        for i, v in enumerate(data_counts[:20]):
            ax.text(i, v + 0.1, f'{v}', ha='center', va='bottom', color='black', size=20)
            
        plt.suptitle(f"Percentage of IPCC references in which France participated", size=25)
        plt.title('Source : OpenAlex\nTraitement : Science et Ingénierie des Données, SIES', size=10, loc='right')

        ax.set_xticklabels(data_counts.index[:20], rotation='vertical', fontsize=15)
        plt.show()
    else:
        res1=get_body(list_wg,terms=False)
        res2=get_body(list_wg,terms=True,french=True)
        data_counts={}
        for x in res1.get('aggregations').get('by_countries').get('buckets'):
            if x.get('key')=='FR':
                print(f"Pour la recherches aux interfaces, pour les working group {', '.join(list_wg)}, \n{round(x.get('doc_count')*100/res2.get('hits').get('total').get('value'),2)} % des publications citées dans l'un des groupes le sont aussi dans le.s autre.s")
    
