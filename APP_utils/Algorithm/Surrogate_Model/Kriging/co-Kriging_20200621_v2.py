import numpy as np
import time
import matplotlib.pyplot as plt
from Kriging_20200621 import Kriging


class coKriging(object):
    def __init__(self, Cpara_arr=None, Dpara_arr=None):
        self.C_krig = None
        self.D_krig = None
        self.C_sigma2 = None
        self.D_sigma2 = None
        self.Cpara_arr = Cpara_arr
        self.Dpara_arr = Dpara_arr
        self.D_parameters = None
        self.Xc = None
        self.Xe = None
        self.Y = None
        self.beta = None
        self.C_Xe = None
        self.Xc = None
        self.Xe = None
        self.co_F = None
        self.C_inverse = None

    def corelation(self, func, X1, X2, para_array):
        list_result = []
        for i in range(X1.shape[0]):
            list_result.append(func(para_array, X1[i], X2).ravel())
        return np.array(list_result)

    def fit(self, Xc, Yc, Xe, Ye):
        self.Xc = Xc
        self.Xe = Xe
        # C
        self.C_krig = Kriging(parameters=self.Cpara_arr)
        self.C_krig.fit(Xc, Yc)

        # self.C_krig.parameters
        C_matrix_cc = self.corelation(self.C_krig.gaussian, self.Xc, self.Xc, self.C_krig.parameters)  # C的cc矩阵
        C_matrix_ee = self.corelation(self.C_krig.gaussian, self.Xe, self.Xe, self.C_krig.parameters)  # C的ee矩阵
        C_matrix_ce = self.corelation(self.C_krig.gaussian, self.Xc, self.Xe, self.C_krig.parameters)  # C的ce矩阵
        self.C_sigma2 = self.C_krig.sigma2  # C的方差sigma2
        # D
        self.C_Xe = self.C_krig.predict(Xe)
        self.D_krig = Kriging(parameters=self.Dpara_arr)
        self.D_krig.fit(self.C_Xe, Ye)
        self.D_parameters = self.D_krig.parameters[1]
        # self.D_parameters = self.D_krig.fit()[2]
        # D_matrix_ee = self.corelation(self.D_krig.gaussian, Xe, Xe, self.D_krig.parameters)  # D的ee矩阵
        D_matrix_ee = self.corelation(self.D_krig.gaussian, self.Xe, self.Xe,
                                      self.D_krig.parameters)  # D的ee矩阵
        self.D_sigma2 = self.D_krig.sigma2  # D的方差sigma2
        C1 = self.C_sigma2 * C_matrix_cc
        C2 = self.D_parameters * self.C_sigma2 * C_matrix_ce
        C3 = self.D_parameters * self.C_sigma2 * C_matrix_ce.T
        C4 = self.D_parameters ** 2 * self.C_sigma2 * C_matrix_ee + self.D_sigma2 * D_matrix_ee
        C = np.vstack((np.hstack((C1, C2)), np.hstack((C3, C4))))
        self.co_F = np.ones(C.shape[-1])
        self.C_inverse = np.linalg.pinv(C)
        self.Y = np.hstack((Yc, Ye))
        # 均值
        self.beta = self.co_F.T.dot(self.C_inverse).dot(self.Y) / (self.co_F.T.dot(self.C_inverse).dot(self.co_F))

    def predict(self, X_pre):
        x_pred_normalization = X_pre / (np.max(X_pre, axis=0) - np.min(X_pre, axis=0))
        # C_matrix_cx = self.corelation(self.C_krig.gaussian, self.Xc, X_pre, self.C_krig.parameters)  # C的cx矩阵
        C_matrix_cx = self.corelation(self.C_krig.gaussian, self.Xc, x_pred_normalization,
                                      self.C_krig.parameters)  # C的cx矩阵
        D_matrix_ex = self.corelation(self.D_krig.gaussian, self.Xe, x_pred_normalization,
                                      self.D_krig.parameters)  # D的ex矩阵
        c1 = self.D_parameters * self.C_sigma2 * C_matrix_cx
        c2 = (self.D_parameters ** 2 * self.C_sigma2 + self.D_sigma2) * D_matrix_ex
        c = np.vstack((c1, c2))
        Y_pre = self.beta + c.T.dot(self.C_inverse).dot(self.Y - self.co_F.dot(self.beta))
        return Y_pre

    def model(self):
        model1 = [self.beta, self.C_sigma2, self.D_parameters,
                  self.C_krig.parameters, self.D_krig.parameters]
        return model1


if __name__ == "__main__":
    parameter_array_c = np.array([0.5, 2])
    parameter_array_d = np.array([0.5, 2, 2.2])

    start = time.perf_counter()

    A_value = 0.5
    B_value = 10
    C_value = -5


    # 高保真的曲线函数表达式
    def high_fidelity_curve(x):
        return (6 * x - 2) ** 2 * np.sin(12 * x - 4)


    # 高保真的曲线函数表达式
    def low_fidelity_curve(x, A=A_value, B=B_value, C=C_value):
        return A * high_fidelity_curve(x) + B * (x - 0.5) + C


    # 高保真的曲线
    XE = np.linspace(0, 1)
    YE = high_fidelity_curve(XE)
    # 高保真选取的四个点
    XE_point = np.array([0, 0.4, 0.6, 1])
    YE_point = high_fidelity_curve(XE_point)
    # 低保真的曲线
    XC = np.linspace(0, 1)
    YC = low_fidelity_curve(XC)
    # 低保真选取的点
    XC_point = np.array([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
    YC_point = low_fidelity_curve(XC_point)
    # 高保真选取的四个点的插值
    kriging = Kriging(parameters=parameter_array_c)
    parameters = kriging.parameters
    kriging.fit(XE_point, YE_point)
    YE_pred = kriging.predict(XE)
    plt.plot(XE, YC, color='#ff9900', label='low fidelity data curve')
    plt.plot(XE, YE, color='#ff00ff', label='high fidelity data curve')
    plt.plot(XE, YE_pred, color='#ff0000', label='Kriging high fidelity data interpolation curve', linestyle=':')
    plt.scatter(XC_point, YC_point, color='#ff9900', label='low fidelity sample data', marker='s')
    plt.scatter(XE_point, YE_point, color='#ff00ff', label='high fidelity sample data', marker='8')  # coKriging插值

    cokriging = coKriging(Cpara_arr=parameter_array_c, Dpara_arr=parameter_array_d)
    cokriging.fit(XC_point, YC_point, XE_point, YE_point)
    XE_PRED = np.linspace(0, 1)
    # print(cokriging.D_krig.parameters)
    # YY = cokriging.C_krig.predict(XE_PRED)
    Y_results_points = cokriging.predict(XC_point)
    Y_results_curve = cokriging.predict(XE_PRED)
    plt.scatter(XC_point, Y_results_points, color='#000000',
                label='predict results data points', marker='o')
    plt.plot(XE_PRED, Y_results_curve, color='#000000',
             label= 'co-Kriging low-high fidelity data interpolation curve',
             linestyle='--')
    plt.legend()
    plt.show()
    elapsed = (time.perf_counter() - start)
    print("Time used:", elapsed)
