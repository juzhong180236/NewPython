#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 10:01:21 2020

@author: shuo
"""

import numpy as np
from scipy import linalg
from APP_utils.Algorithm.Surrogate_Model.RBF.RBF_Surrogate import RBF
import matplotlib.pyplot as plt


class Sur_MFSMLS(object):
    """
    参数
    --------
    xtrain: 训练样本点的输入，n*m的矩阵，n代表样本个数，m代表维度/变量个数
    ytrain: 训练样本点的响应值/观测值，n*1的矩阵
    xtest: 预测点的输入，p*m的矩阵，p为预测点的个数
    ratio：影响区半径的比率，范围为(0,1]
    **kwargs: 输入权重函数的类型，e.g., weight_type='cubic_spline', 总共三个权重函数可供选择
              分别为：'cubic_spline'， 'pcs'，和 'gaussian'. 其中psc是polynomial compactly supported function的简称


    """

    def __init__(self, XL, YL, XH, YH, Xtest, **kwargs):
        self.XL = np.array(XL)  # 最好在这里加一条np.array因为如果传入的数据是np.mat的话，那么后面的矩阵运算可能有错误，比如想元素相乘，结果实现的是矩阵想乘
        self.YL = np.array(YL)
        self.XH = np.array(XH)
        self.YH = np.array(YH)
        self.Xtest = np.array(Xtest)
        self.ntest = self.Xtest.shape[0]  # 测试点样本个数
        self.nH = self.XH.shape[0]  # 高保真训练样本点
        self.ndv = self.XH.shape[1]  # 问题维度/高保真维度/变量个数
        self.weight_type = kwargs.pop('weight_type', 'gaussian')
        self.degree = kwargs.pop('degree', 2)  # 默认基函数的次数为2

        self.radius_influence()
        self.P = self.Pmatrix()
        # print(self.P)

    def radius_influence(self):  # 这里要修改成样本点个数
        if self.degree == 1:
            self.k = self.ndv + 1
        elif self.degree == 2:
            self.k = int((self.ndv + 1) * (self.ndv + 2) / 2)

    def Pmatrix(self):
        if self.degree == 1:
            # P = np.zeros((self.nH, self.ndv+1))
            P = np.hstack((np.ones((self.nH, 1)), self.XH))
        elif self.degree == 2:
            P = np.hstack((np.ones((self.nH, 1)), self.XH))
            for j in range(self.ndv):
                P = np.hstack((P, self.XH[:, j:j + 1] * self.XH[:, j:(self.ndv + 1)]))
        else:
            P = None
        # RBF
        # 用低保真点拟合低保真模型 # RBF的参数还是不一样;0.1363; RBF的预测值和Matlab不太一样，其他没有太大问题
        sur_RBF = RBF()
        sur_RBF.fit(self.XL, self.YL)
        # 求得测试点在低保真模型处得预测值
        self.YLtest = sur_RBF.predict(self.Xtest).reshape((self.ntest, 1))
        # 求 高保真点在低保真模型处的值
        YL_H = sur_RBF.predict(self.XH).reshape((self.nH, 1))
        P = np.hstack((YL_H, P))
        return P

    def pvector(self, xnew):
        if self.degree == 1:
            # p = np.zeros((1, self.ndv+1))              #这里的self.p是不是可以直接写成p
            # self.p = np.hstack( (np.ones((1,1)), xnew.reshape(self.ndv,1)) )
            p = np.hstack((np.ones((1, 1)), xnew))  # 这里应该要修改。
        elif self.degree == 2:
            p = np.hstack((np.ones((1, 1)), xnew))
            for k in range(self.ndv):
                p = np.hstack((p, xnew[:, k:k + 1] * xnew[:, k:(self.ndv + 1)]))
        else:
            p = None
        return p

    #    def LF_Surrogate(self):
    #        #RBF
    #        # 用低保真点拟合低保真模型
    #        sur_RBF = Sur_RBF(self.XL, self.YL)
    #        sur_RBF.fit()
    #        # 求得测试点在低保真模型处得预测值
    #        self.YLtest = sur_RBF.predict(self.Xtest)
    #        # 求 高保真点在低保真模型处的值
    #        YL_H = sur_RBF.predict(self.XH)
    #        self.P = np.hstack((YL_H, self.P))

    def cubic_spline(self):  # 这里函数命名为s，里面又有变量是s，这样能行吗？
        idx1 = self.s <= 0.5
        self.w[idx1] = (2.0 / 3.0 - 4.0 * self.s[idx1] ** 2 + 4.0 * self.s[idx1] ** 3)[:,
                       np.newaxis]  # [:,np.newaxis]是把后面计算的结果变成shape=(:,1)的列向量，目的是为了和w这个列向量维度匹配
        idx2 = (self.s > 0.5) & (self.s <= 1)
        self.w[idx2] = (4.0 / 3.0 - 4.0 * self.s[idx2] + 4.0 * self.s[idx2] ** 2 - 4.0 * self.s[idx2] ** 3 / 3.0)[:,
                       np.newaxis]
        idx3 = self.s > 1
        self.w[idx3] = 0
        return self.w  # self.XXX也需要return吗？

    def pcs(self):
        idx1 = self.s <= 1
        self.w[idx1] = ((1.0 - self.s[idx1]) ** 4 * (1 + 2.0 * self.s[idx1]))[:, np.newaxis]
        idx2 = self.s > 1
        self.w[idx2] = 0
        return self.w

    def gaussian(self):
        beta = 0.5
        idx1 = self.s <= 1
        self.w[idx1] = np.exp(- (self.s[idx1] / beta) ** 2)[:, np.newaxis]
        idx2 = self.s > 1
        self.w[idx2] = 0
        return self.w

    def predict(self):
        yhat = np.zeros((self.ntest, 1))
        for i in range(self.ntest):
            p1 = self.pvector(self.Xtest[i, :].reshape(1, self.ndv)).T  # 这里可能根本就不需要reshape
            pL = np.vstack((self.YLtest[i, :], p1))  # 这里对不对呢？
            dist = np.linalg.norm(self.Xtest[i, :] - self.XH, axis=1)  # 这里shape=1了，不是二维矩阵形式了
            # 这里要修改
            dist_sort = np.sort(dist)
            kk = self.k + 1
            if self.nH < kk:
                kk = np.min((kk, self.nH))
            self.s = dist / dist_sort[int(kk - 1)]

            self.w = np.zeros((self.nH, 1))
            func_name = self.weight_type
            self._weight = getattr(self, func_name)
            weight = self._weight()
            self.W = np.diag(weight[:, 0])
            A = self.P.T @ self.W @ self.P
            B = self.P.T @ self.W
            yhat[i] = pL.T @ np.linalg.pinv(A) @ B @ self.YH
        return yhat.reshape((self.ntest, 1))


#    def model(self):
#        self.xtrain_copy = np.copy(self.xtrain)
#        self.ytrain_copy = np.copy(self.ytrain)
#        model=[self.xtrain_copy.tolist(),self.ytrain_copy.tolist(),self.ratio,
#               self.weight_type,self.degree,"MLS",self.xtrain.shape[1]]
#        return model


# def Sur_MLS_predict(X_predict,model):
#     #model = [Xtrain_copy.tolist(), Ytrain_copy.tolist(), ratio, weight_type, degree, "MLS", Xtrain.shape[1]]
#     Xtrain=np.array(model[0])
#     Ytrain=np.array(model[1])
#     ratio=model[2]
#     weight_type=model[3]
#     degree=model[4]
#     model_name=model[-2]
#     #print(model_name)
#     sur_MLS=Sur_MLS(Xtrain, Ytrain, ratio,degree=degree,weight_type=weight_type)
#     predict=sur_MLS.predict(X_predict)
#     predict=np.array(predict)
#     return predict

if __name__ == "__main__":
    # import h5py
    # import hdf5storage
    #
    # data = hdf5storage.loadmat(
    #     '/Users/shuo//Work/Phd_work/Dados_WebPlatform/code/zujian/sur_predict/TestData10D4pythonMFSMLS.mat')  # func2D2 Samples
    # XH = data['XH']
    # YH = data['YH']
    # XL = data['XL']
    # YL = data['YL']
    # Xtest = data['Xtest']
    # YHtest = data['YHtest']
    # ntest = Xtest.shape[0]
    A_value = 0.5
    B_value = 10
    C_value = -5


    # 高保真的曲线函数表达式
    def onevar(x):
        return (6 * x - 2) ** 2 * np.sin(12 * x - 4)


    # 高保真的曲线函数表达式
    def cheaponevar(x, A=A_value, B=B_value, C=C_value):
        return A * onevar(x) + B * (x - 0.5) + C


    XL = np.linspace(0, 1, 11).reshape(-1, 1)
    YL = cheaponevar(XL)
    XH = np.asarray([0, 0.4, 0.6, 0.8, 1]).reshape(-1, 1)
    YH = onevar(XH)
    Xtest = np.linspace(0, 1, 101).reshape(-1, 1)
    ytest = onevar(Xtest)
    ntest = len(ytest)
    xtrain = XH
    ytrain = YH
    ntrain = len(YH)

    example1 = Sur_MFSMLS(XL, YL, XH, YH, Xtest, weight_type='gaussian')
    yhat = example1.predict()
    # print(yhat)
    R2 = 1.0 - sum((ytest - yhat) ** 2) / sum((ytest - np.mean(ytest)) ** 2)
    # print(R2)
    plt.plot(Xtest, yhat, color='r', linestyle='-', lw=2, label='predicted value')
    plt.plot(Xtest, ytest, color='b', linestyle='--', lw=2, label='real value')
    plt.scatter(XH, YH, color='m', marker='s', lw=2, label='high fidelity train points')
    plt.scatter(XL, YL, color='g', marker='o', lw=2, label='low fidelity train points')
    plt.legend()
    plt.show()
