import numpy as np

'''原始下载的基于NN的RBF包——基函数为Gauss'''

# x 数据点 c 中心点 s标准差
def RBF_result(x, c, s):
    return np.exp(-(x - c) ** 2 / (2 * s ** 2))


# 对一个一维输入执行K-means
#     参数:
#         X {ndarray} -- 一个M×1矩阵
#         k {int} -- 聚类的个数
#     返回:
#         ndarray -- 一个包含聚类中心的k×1数组
def k_means(X, k):
    # 输入的X向量，从数组实体中删除单维项，得到数组X_temp
    # 从X_temp中抽取元素，形成size为k的新数组clusters
    clusters = np.random.choice(np.squeeze(X), size=k)
    # print(clusters)

    copyClusters = clusters.copy()
    # 取一个k阶全零矩阵stds
    stds = np.zeros(k)
    # 是否收敛
    converged = False
    #
    while not converged:

        # 计算聚类中心与每个点的距离，其中(distance [i, j]表示第i个点到第j个簇的距离)
        # X[:, np.newaxis]获得X的5*1矩阵，clusters[np.newaxis, :]获得clusters的1*5矩阵
        # 获得每个点和聚类中心的距离
        distances = np.squeeze(np.abs(X[:, np.newaxis] - clusters[np.newaxis, :]))
        # numpy中的轴，比如维度为(3,4,5)数据，0轴为3组元素，1轴为4组元素，2轴5组元素
        # 找到每个点最近的聚类中心编号。np.argmin给出根据axis轴取得的最小值的下标
        closestCluster = np.argmin(distances, axis=1)

        # 将分配给某一聚类的所有点取平均值，借此更新聚类的中心
        for i in range(k):
            # 将第i个中心点的对应的X向量中的数值分配给它，这个语法选取X中满足条件的元素组成array
            pointsForCluster = X[closestCluster == i]
            # 如果这个聚类的点至少有一个
            if len(pointsForCluster) > 0:
                # 得到新的中心点
                clusters[i] = np.mean(pointsForCluster, axis=0)

        # 如果聚类中心点没有移动，则收敛
        # numpy.linalg模块包含线性代数的函数。使用这个模块，可以计算逆矩阵、求特征值、解线性方程组以及求解行列式等。
        # norm默认求sqrt(x1^2+x2^2+...)
        converged = np.linalg.norm(clusters - copyClusters) < 1e-6
        # 复制数组clusters到copyClusters，进行比较是否有改变，无改变就表示收敛
        copyClusters = clusters.copy()
    # 获得每个点和聚类中心的距离
    distances = np.squeeze(np.abs(X[:, np.newaxis] - clusters[np.newaxis, :]))
    # 找到每个点最近的聚类中心编号。np.argmin给出根据axis轴取得的最小值的下标
    closestCluster = np.argmin(distances, axis=1)

    # 考虑只有一个点或没有点的聚类
    clustersWithNoPoints = []
    for i in range(k):
        pointsForCluster = X[closestCluster == i]
        if len(pointsForCluster) < 2:
            # 跟踪没有点或只有一个点的聚类
            clustersWithNoPoints.append(i)
            continue
        else:
            # 计算沿指定轴的标准差。
            # stds[i] = np.std(X[closestCluster == i])
            stds[i] = np.std(X[closestCluster == i])

    # 如果有0或1个点的聚类，取其他聚类的std均值
    if len(clustersWithNoPoints) > 0:
        pointsToAverage = []
        for i in range(k):
            # 将大于0或1个点的聚类所含的元素放入list，pointsToAverage
            if i not in clustersWithNoPoints:
                pointsToAverage.append(X[closestCluster == i])
        # 将pointsToAverage中的多个数组数据拼接为1个，reval将多维数组降为一维（flatten,copy）
        pointsToAverage = np.concatenate(pointsToAverage).ravel()
        # 取聚类中点数量超过1个的数据组成的array的标准差的均值（数据已经是一维，其实不需要取均值了吧）std[[3,5]]
        stds[clustersWithNoPoints] = np.mean(np.std(pointsToAverage))
    return clusters, stds


# 径向基函数RBF网络
class RBFNet(object):
    # 1个epoch等于使用训练集中的全部样本训练一次；
    def __init__(self, k=2, lr=0.01, epochs=100, rbf=RBF_result, inferStds=True):
        self.k = k  # 基的数量
        self.lr = lr  # 学习率
        self.epochs = epochs  # 数量
        self.rbf = rbf  # rbf名称
        self.inferStds = inferStds

        # 标准正态分布随机数，randn(x1,x2,...)，其中x1,x2为维度
        self.w = np.random.randn(k)  # 权重
        self.b = np.random.randn(1)  # 偏差

    # 拟合函数
    def fit(self, X, y):
        if self.inferStds:
            # 使用k_means方法得到高斯的均值和标准差
            self.centers, self.stds = k_means(X, self.k)
        else:
            # 使用k_means找到聚类中心
            self.centers, _ = k_means(X, self.k)
            # 任何两个聚类中心之间的最大距离
            dMax = max([np.abs(c1 - c2) for c1 in self.centers for c2 in self.centers])
            # 最大距离/sqrt(2k),一个固定的公式，使用repeat给每个中心分配一个标准差
            # repeat函数：不设置axis，将数值降维为一维，并按照第二个参数重复k次
            self.stds = np.repeat(dMax / np.sqrt(2 * self.k), self.k)

        # 开始训练（反向传播算法）
        for epoch in range(self.epochs):
            for i in range(X.shape[0]):
                # 向前传播，对每一个X[i]，取的高斯函数的值
                # zip每次返回一对center和stds
                Gaussian_result = np.array([self.rbf(X[i], c, s) for c, s, in zip(self.centers, self.stds)])
                print("第" + str(i) + '个' + str(Gaussian_result))
                # .T对Gaussian_result转置
                F = Gaussian_result.T.dot(self.w) + self.b
                # 代价函数Cost Function
                loss = (y[i] - F).flatten() ** 2
                # print('Loss: {0:.2f}'.format(loss[0]))

                # 向后传播
                error = -(y[i] - F).flatten()

                # online update
                self.w = self.w - self.lr * Gaussian_result * error
                self.b = self.b - self.lr * error

    def predict(self, X):
        y_pred = []
        for i in range(X.shape[0]):
            a = np.array([self.rbf(X[i], c, s) for c, s, in zip(self.centers, self.stds)])
            F = a.T.dot(self.w) + self.b
            y_pred.append(F)
        return np.array(y_pred)
