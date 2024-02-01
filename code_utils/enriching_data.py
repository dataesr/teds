import requests
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

def get_countries(df,row):
    doi=row.doi
    data=df[df.doi==doi]
    i=df[df.doi==doi].index[0]
    if data['results'][i]!=[]:
        authors=data['results'][i][0].get('authorships')
        if authors!=[]:
            countries=list(set(aplatir([author.get('countries') for author in authors]))) 
        else:
            countries=[None]
    else:
        return [None]

    return countries