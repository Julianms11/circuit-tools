import numpy as np

def paralelo(Z: list):
    Imps = np.ones(len(Z), dtype=complex)
    for i in range(len(Z)):
        Imps[i] = 1/Z[i]
    ImpPar = 1/np.sum(Imps)
    return ImpPar

def serie(Z: list):
    return np.sum(Z)