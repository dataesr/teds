import os
from dotenv import load_dotenv
load_dotenv()
import requests
import base64
from elasticsearch import Elasticsearch
from urllib import parse
import pandas as pd
import matplotlib.pyplot as plt

def get_from_es(body, nature='teds-bibliography'):
    if nature=='teds-bibliography':
        passw = f"{os.getenv('ES_LOGIN_TEDS_BACK')}:{os.getenv('ES_PASSWORD_TEDS_BACK')}"
        base64_bytes = passw.encode('ascii')
        message_bytes = base64.b64encode(base64_bytes)
        token = message_bytes.decode('ascii')
        url = os.getenv('ES_URL')+'teds-bibliography/_search'
    else:
        passw = f"{os.getenv('ES_LOGIN_scanR')}:{os.getenv('ES_PASSWORD_scanR')}"
        base64_bytes = passw.encode('ascii')
        message_bytes = base64.b64encode(base64_bytes)
        token = message_bytes.decode('ascii')
        url = os.getenv('ES_URL')+'scanr-publications-20241128/_search'  #14
    return requests.post(url, json=body, headers={f'Authorization': f'Basic {token}'}).json()

def get_data_from_elastic(my_filters,nature, size=20):
    body = {
            'size': 0,
            'query': {
                'bool': my_filters,
                },
                'aggs': {
                    'by_countries': {
                        'terms': {
                            'field': 'countries.keyword', 'size': size
                        },
                    }
                },
                'track_total_hits': True
            }
    res = get_from_es(body,nature)
    return res

def plot_graph(data,list_wg,type='Part',ip=['IPCC','Working Group.s']):
    data_counts={}
    for x in data.get('aggregations').get('by_countries').get('buckets'):
        if type=='Part':
            data_counts[x.get('key')]=round(x.get('doc_count')*100/data.get('hits').get('total').get('value'),1)
        if type=='Number':
            data_counts[x.get('key')]=x.get('doc_count')
    data_counts=pd.Series(data_counts)
    color_dict = {'FR': '#BE2125'}
    plt.figure(figsize=(24, 10))
    ax = data_counts[:20].plot(kind='bar', color=[color_dict.get(u, 'grey') for u in data_counts[:20].index], width=0.8)

    if type=='Part':
        pourc='%'
    else:
        pourc=''

    for i, v in enumerate(data_counts[:20]):
        ax.text(i, v + 0.1, f'{v}{pourc}', ha='center', va='bottom', color='black', size=20)
        
    plt.suptitle(f"{type} of {ip[0]} references by country - {ip[1]} {', '.join([x.replace('_',' ') for x in list_wg])}", size=25)
    plt.title('Source : OpenAlex\nTraitement : Science et Ingénierie des Données, SIES', size=10, loc='right')

    ax.set_xticklabels(data_counts.index[:20], rotation='vertical', fontsize=15)
    if type=='Part':
        ax.set_yticklabels([f'{tick:.0f}%' for tick in ax.get_yticks()], fontsize=15)
    ax.set_ylabel(f'{type} of IPCC references', fontsize=15)
    plt.show()


def interfaces_evaluation(list_wg,country):
    data_and = get_data_from_elastic({
                'must': [{'match': {'ipcc.wg.keyword': x}} for x in list_wg]+[{'match':{'countries.keyword': country}}]
            })
    data_or = get_data_from_elastic({
                'should': [{'term': {'ipcc.wg.keyword': x}} for x in list_wg],
                'must': [
                    {'match':{'countries.keyword': country}},
                ],
                'minimum_should_match': 1
            })
    nb_publi_total = data_or['hits']['total']['value']
    nb_publi_fr = [k['doc_count'] for k in data_and['aggregations']['by_countries']['buckets'] if k['key']=='FR'][0]
    print(f"Pour la recherches aux interfaces, pour les working groups {', '.join(list_wg)}, \n{int(10000 * nb_publi_fr/nb_publi_total)/100} % des publications citées dans l'un des groupes le sont aussi dans le.s autre.s")
