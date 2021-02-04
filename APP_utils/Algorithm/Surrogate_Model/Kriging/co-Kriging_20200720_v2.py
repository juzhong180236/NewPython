import numpy as np
import time
import matplotlib.pyplot as plt
from .Kriging import Kriging


class coKriging(object):
    def __init__(self, Cpara_arr=None, Dpara_arr=None):
        self.C_krig = None
        self.D_krig = None
        self.C_sigma2 = None
        self.D_sigma2 = None
        self.Cpara_arr = Cpara_arr
        self.Dpara_arr = Dpara_arr
        self.D_parameters = None
        self.Y = None
        self.beta = None
        self.Yc_Xe = None
        self.Xc = None
        self.Xe = None
        self.co_F = None
        self.C_inverse = None
        self.d = None
        self.Xc_normalization = None
        self.Xe_normalization = None

    def corelation(self, func, X1, X2, para_array):
        list_result = []
        for i in range(X1.shape[0]):
            list_result.append(func(para_array, X1[i], X2).ravel())
        return np.array(list_result)

    def fit(self, Xc, Yc, Xe, Ye):
        self.Xc = Xc
        self.Xe = Xe
        self.Xc_normalization = self.Xc / (np.max(self.Xc, axis=0) - np.min(self.Xc, axis=0))
        self.Xe_normalization = self.Xe / (np.max(self.Xe, axis=0) - np.min(self.Xe, axis=0))

        # C
        # 得到低保真点的均值、方差、para_1、para_2(=2)，需要训练Xc和Yc
        self.C_krig = Kriging(parameters=self.Cpara_arr)
        self.C_krig.fit(Xc, Yc)
        self.C_sigma2 = self.C_krig.sigma2  # C的方差sigma2

        # C_matrix_cc = self.corelation(self.C_krig.gaussian, self.Xc, self.Xc, self.C_krig.parameters)  # C的cc矩阵
        # C_matrix_ee = self.corelation(self.C_krig.gaussian, self.Xe, self.Xe, self.C_krig.parameters)  # C的ee矩阵
        # C_matrix_ce = self.corelation(self.C_krig.gaussian, self.Xc, self.Xe, self.C_krig.parameters)  # C的ce矩阵
        C_matrix_cc = self.corelation(self.C_krig.gaussian, self.Xc_normalization, self.Xc_normalization,
                                      self.C_krig.parameters)  # C的cc矩阵
        # C_matrix_ee = self.corelation(self.C_krig.gaussian, Xe, Xe, self.C_krig.parameters)  # C的ee矩阵
        C_matrix_ee = self.corelation(self.C_krig.gaussian, self.Xe_normalization, self.Xe_normalization,
                                      self.C_krig.parameters)  # C的ee矩阵
        # C_matrix_ce = self.corelation(self.C_krig.gaussian, Xc, Xe, self.C_krig.parameters)  # C的ce矩阵
        C_matrix_ce = self.corelation(self.C_krig.gaussian, self.Xc_normalization, self.Xe_normalization,
                                      self.C_krig.parameters)  # C的ce矩阵

        # D
        # 得到高保真点的均值、方差、para_1、para_2(=2)，ρ，需要训练Xe和d=Ye-ρ*Yc(Xe)
        self.D_krig = Kriging(parameters=self.Dpara_arr)
        self.Yc_Xe = self.C_krig.predict(Xe)
        self.D_krig.fit(self.Xe, Ye, yc_xe=self.Yc_Xe, c_matrix=C_matrix_cc)
        self.D_parameters = self.D_krig.parameters[1]

        D_matrix_ee = self.corelation(self.D_krig.gaussian, self.Xe, self.Xe, self.D_krig.parameters)  # D的ee矩阵
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
        C_matrix_cx = self.corelation(self.C_krig.gaussian, self.Xc_normalization, x_pred_normalization,
                                      self.C_krig.parameters)  # C的cx矩阵
        D_matrix_ex = self.corelation(self.D_krig.gaussian, self.Xe_normalization, x_pred_normalization,
                                      self.D_krig.parameters)  # D的ex矩阵
        # C_matrix_cx = self.corelation(self.C_krig.gaussian, self.Xc, X_pre, self.C_krig.parameters)  # C的cx矩阵
        # D_matrix_ex = self.corelation(self.D_krig.gaussian, self.Xe, X_pre, self.D_krig.parameters)  # D的ex矩阵
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
    parameter_array_c = np.array([0.5])
    parameter_array_d = np.array([0.5, 0.999])

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

    plt.plot(XE, YC, color='#231fb4', label='low fidelity data curve')
    plt.plot(XE, YE, color='#ff7f0e', label='high fidelity data curve')
    plt.scatter(XC_point, YC_point, color='#ff0000', label='low fidelity sample data', marker='s')
    plt.scatter(XE_point, YE_point, color='#000000', label='high fidelity sample data', marker='8')  # coKriging插值

    kriging = Kriging(parameters=parameter_array_c)
    kriging.fit(XE_point, YE_point)
    cokriging = coKriging(Cpara_arr=parameter_array_c, Dpara_arr=parameter_array_d)
    cokriging.fit(XC_point, YC_point, XE_point, YE_point)

    XE_PRED = np.linspace(0, 1)
    y_pre_E = kriging.predict(XE_PRED)
    Y_results_curve = cokriging.predict(XE_PRED)
    plt.plot(XE_PRED, y_pre_E, color='#ff00ff',
             label='Kriging high fidelity data interpolation curve',
             linestyle='--')
    plt.plot(XE_PRED, Y_results_curve, color='#000000',
             label='co-Kriging low-high fidelity data interpolation curve',
             linestyle='--')
    plt.legend()
    plt.show()
    elapsed = (time.perf_counter() - start)
    print("Time used:", elapsed)
