import requests

def get_doi_glutton(row):
    title=row.title
    author=str(row.author).split(',')[0]
    url=f"https://cloud.science-miner.com/glutton/service/lookup?atitle={title}&firstAuthor={author}"
    response = requests.get(url)
    data = response.json()
    return data.get('DOI')