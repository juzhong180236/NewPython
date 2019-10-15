import numpy as np


def Gaussian(x, c, s):
    return np.exp(-(x - c) ** 2 / (2 * s ** 2))

def RBF(X,y):

