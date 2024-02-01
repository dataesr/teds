import os
import pandas as pd
import spacy
import pycld2
from unidecode import unidecode
import string
import ast

DATA_PATH = "/run/media/julia/DATA/fall2023_patstat/tls214/"
os.chdir(DATA_PATH)


def remove_ucode(txt):
    txt2 = ""
    for c in txt:
        if c.isalnum():
            txt2 = txt2 + c
        else:
            d = unidecode(c)
            txt2 = txt2 + d

    liste = list(map(lambda a: a.strip(), txt2))
    liste = [item for item in liste if item != "'"]

    txt3 = ""
    for item in liste:
        if item != "":
            txt3 = txt3 + item
        else:
            txt3 = txt3 + " "

    return txt3

df = pd.read_csv("tls214_part01.csv", sep=",", nrows=201, engine="python",
                 parse_dates=['npl_publn_date', 'npl_publn_end_date', 'online_search_date'], date_format="%Y%m%d")
df = df.loc[df["npl_publn_id"]!="0"]

dfa = df.loc[df["npl_type"]=="a"]

# mapping_table = str.maketrans('', '', string.punctuation)

nlp = spacy.load("en_core_web_sm")

# dfa["biblio2"] = dfa["npl_biblio"].apply(lambda a: a.translate(mapping_table))
dfa["biblio2"] = dfa["npl_biblio"].apply(lambda a: remove_ucode(a))
dfa["spacy"] = dfa["biblio2"].apply(lambda a: nlp(a).lang_)
dfa["pycld2"] = dfa["biblio2"].apply(lambda a: list(pycld2.detect(a, returnVectors=False)))

