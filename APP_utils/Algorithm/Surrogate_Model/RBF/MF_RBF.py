# Input:
#	xtest: testing points
#	xH: training points
#	yL_H: value of low-fidelity model at high-fidelity training points
#	yH: value of high-fidelity model at high-fidelity training points
#	bf_type: basis function type
#       'LN'--Linear,phi(r) = r;
#       'CB'--Cubic,phi(r) = r^3;
#       'TPS'--Thin Plate Spline,phi(r) = r^2*log10(r);
#       'G'--Gaussian,phi(r) = exp(-r^2/(2*sigma^2));
#       'MQ'--Multiquadric, phi(r) = sqrt(r^2+sigma^2);
#       'IMQ'--Inverse multiquadric,phi(r) = 1/sqrt(r^2+sigma^2)...
# Output:
#   MFS: a struct including the scaling factor and the weight
import numpy as np


class MF_RBF(object):

    def __init__(self):
        pass

    def coefgenerate_fix(self, xtest, xH, yL_H, yH, bf_type):
        ntrain = xH.shape[0]
        dist = np.zeros((ntrain, ntrain))
        print(xH[0])
        for i in range(ntrain):
            dist1 = (xH - np.tile(xH[i, :], (ntrain, 1))) ** 2
            dist[i, :] = np.sqrt(np.sum(dist1, axis=1))
            print(dist1)
        print(dist)


if __name__ == "__main__":
    xH = np.asarray([0.4, 0.6, 0.8, 1]).reshape(-1, 2)
    print(xH)
    mf_rbf = MF_RBF()
    mf_rbf.coefgenerate_fix(1, xH, 2, 2, 2)
