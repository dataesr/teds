def aplatir(conteneurs):
    return [conteneurs[i][j] for i in range(len(conteneurs)) for j in range(len(conteneurs[i]))]