import numpy as np


# x 数据点 c 中心点 s标准差
def RBF_result(x, c, s):
    return np.exp(-(x - c) ** 2 / (2 * s ** 2))
#
# def RBF_result(x, c, s):
#     # return np.exp(-(x - c) ** 2 / (2 * s ** 2))
#     return np.sqrt((x - c) ** 2 + s ** 2)

# 径向基函数RBF网络
class RBFNet(object):
    # 1个epoch等于使用训练集中的全部样本训练一次；
    def __init__(self, k=1, lr=0.1, epochs=200, rbf=RBF_result, inferStds=True):
        self.k = k  # 基的数量
        self.lr = lr  # 学习率
        self.epochs = epochs  # 数量
        self.rbf = rbf  # rbf名称
        self.inferStds = inferStds
        self.centers = 0
        # 标准正态分布随机数，randn(x1,x2,...)，其中x1,x2为维度
        self.w = np.random.randn(k)  # 权重
        self.b = np.random.randn(1)  # 偏差

    # 拟合函数
    def fit(self, X, y):
        self.stds = np.std(X)
        # 开始训练（反向传播算法）
        for epoch in range(self.epochs):
            for i in range(X.shape[0]):
                # 向前传播，对每一个X[i]，取的高斯函数的值
                Gaussian_result = np.array([self.rbf(X[i], self.centers, self.stds)])
                # print("第" + str(i) + '个' + str(Gaussian_result))
                # print(self.w)
                # 得到加权输出F
                F = Gaussian_result.dot(self.w) + self.b

                # cost = (y[i] - F).flatten() ** 2
                # print('Cost: {0:.2f}'.format(cost[0]))
                # 向后传播，得到计算梯度下降时需要用到的一个结果
                error = -(y[i] - F).flatten()

                # 梯度下降更新，其实要传到javascript端的是wb
                self.w = self.w - self.lr * Gaussian_result * error
                self.b = self.b - self.lr * error
        return np.concatenate((self.w, self.b))

    def predict(self, X):
        y_pred = []
        for i in range(X.shape[0]):
            Gaussian_result = np.array([self.rbf(X[i], self.centers, self.stds)])
            F = Gaussian_result.dot(self.w) + self.b
            y_pred.append(F)
        return np.array(y_pred)
