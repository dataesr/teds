import pandas as pd
import pickle

def write_cache(cached_openalex_data,path):
    pickle.dump(cached_openalex_data, open(path+f'{cached_openalex_data}.pkl', 'wb'))

def load_cache(cached_openalex_data,path):
    cached_openalex_data = pickle.load(open(path+f'{cached_openalex_data}.pkl', 'rb'))
    print(f'{len(cached_openalex_data)} data in cached openalex data')
    return cached_openalex_data