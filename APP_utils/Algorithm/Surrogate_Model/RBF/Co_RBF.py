import numpy as np
from APP_utils.Algorithm.Surrogate_Model.RBF.RBF_Surrogate import RBF
import matplotlib.pyplot as plt


class Co_RBF(object):

    def __init__(self):
        self.Xe = None
        self.Xc = None
        self.ye = None
        self.yc = None
        self.phis = None
        pass

    def _CoRBF_durantin(self, XL, YL, XH, YH, xtest, basis):
        self.Xe = XL
        self.Xc = YL
        self.ye = XH
        self.yc = YH
        K=len()
        pass


if __name__ == "__main__":
    pass
