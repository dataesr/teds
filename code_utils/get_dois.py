import requests

def get_doi_from_apis(title, author=None):

    doi = _get_doi_crossref(title, author)
    if doi:
        return doi
    else:
        return _get_doi_openalex(title, author)


def _get_doi_crossref(title, author=None):
    try:
        url = "https://api.crossref.org/works"
        query = f"{title} {author}" if author else title
        params = {
            "query": query,
            "rows": 1,
            "select": "DOI,score"
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        items = response.json().get("message", {}).get("items", [])
        if items and items[0].get("score", 0) > 50:
            return items[0].get("DOI")
    except Exception as e:
        print(f"Crossref error: {e}")
    return None


def _get_doi_openalex(title, author=None):
    try:
        url = "https://api.openalex.org/works"
        query = f"{title} {author}" if author else title
        params = {
            "search": query,
            "per_page": 1,
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        results = response.json().get("results", [])
        if results:
            doi = results[0].get("doi")
            if doi:
                return doi.replace("https://doi.org/", "")
    except Exception as e:
        print(f"OpenAlex error: {e}")
    return None


def get_doi(row):
    title = row.title
    author = None

    if 'author' in list(row.index):
        author = str(row.author).split(',')[0]
    elif 'creators' in list(row.index):
        if isinstance(row.creators, list) and len(row.creators) > 0:
            if isinstance(row.creators[0], dict):
                author = row.creators[0].get('lastName')

    return get_doi_from_apis(title, author)