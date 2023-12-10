import numpy as np


def statistic_predict(Basket, N, N_column):
    buf = np.zeros((N))
    for el in Basket:
        buf += stat[el]
    n_product = buf.argsort()[-N_column:][::-1]
    return n_product


stat = np.loadtxt("stat.txt", dtype=int)
