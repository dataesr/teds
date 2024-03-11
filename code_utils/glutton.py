import requests
from retrying import retry

@retry(wait_fixed=600000, stop_max_attempt_number=10000)
def get_doi_glutton(row):
    title=row.title
    if 'author' in list(row.index):
        author=str(row.author).split(',')[0]
        url=f"https://cloud.science-miner.com/glutton/service/lookup?atitle={title}&firstAuthor={author}"
        response = requests.get(url)
        data = response.json()
        return data.get('DOI')
    if 'creators' in list(row.index):
        if (isinstance(row.creators,list)):
            if (len(row.creators)>0):
                if isinstance(row.creators[0],dict):
                    author=row.creators[0].get('lastName')
                    url=f"https://cloud.science-miner.com/glutton/service/lookup?atitle={title}&firstAuthor={author}"
                    response = requests.get(url)
                    data = response.json()
                    return data.get('DOI')
                else:
                    pass
            else:
                 pass
        else:
                pass
        
def check_doi_glutton(row):
    return False
    