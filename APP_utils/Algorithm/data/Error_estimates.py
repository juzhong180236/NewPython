import numpy as np


def R2(y_real, y_predict):
    RR = 1 - (np.sum(np.square(y_real - y_predict)) / np.sum(
        np.square(y_predict - np.mean(y_predict))))
    return RR


def MY(y_real, y_predict):
    M = (np.sum(np.abs(y_real - y_predict)) / np.abs(np.mean(y_real))) / np.asarray(y_real).shape[-1] * 100
    return M
