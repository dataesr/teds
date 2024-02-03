def aplatir(conteneurs):
    return [conteneurs[i][j] for i in range(len(conteneurs)) for j in range(len(conteneurs[i]))]


def dict_wg_chap_freq(row):
    for i in range(len(row['chap'])):
