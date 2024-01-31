import requests

def get_doi_glutton(title, first_author_lastname):
    url=f"https://cloud.science-miner.com/glutton/service/lookup?atitle={title}&firstAuthor={first_author_lastname}"
    response = requests.get(url)
    data = response.json()
    return data.get('DOI')
