import pandas as pd

def get_doi_cleaned(x):
    low_x=str(x).lower()
    if pd.isna(x):
        return None
    if low_x.find('https://doi.org/')>0:
        return low_x.replace('https://doi.org/','')
    else:
        return low_x