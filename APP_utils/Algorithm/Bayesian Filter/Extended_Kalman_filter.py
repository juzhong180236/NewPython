import numpy as np
import matplotlib.pyplot as plt

"""
对非线性的状态和观测方程线性化，即使用泰勒公式近似
扩展卡尔曼滤波对非线性问题解决不太好，需要进行很多调试
但是计算速度快，基本和卡尔曼滤波一样快，需要内存也小
非线性比较弱，实时性要求不高的场景可以用

EKF

x(k)=sin(3*x(k-1))
y(k)=x(k)^2

注意似然概率是多峰分布，具有强烈的非线性，
"""
# X(k-1)服从期望为X(k-1)+，方差为P(k-1)+的正态分布

# 时间序列
time = np.arange(0.1, 1, 0.01)
time = np.insert(time, len(time), 1)
length = len(time)
x = np.zeros(shape=(length,))
y = np.zeros(shape=(length,))

# 设定初值
x[0] = 0.1
y[0] = 0.1 ** 2

# 生成真实数据与观测数据
for i in range(1, length):
    x[i] = np.sin(3 * x[i - 1])  # 状态
    y[i] = x[i] ** 2 + np.random.normal(0, 0.7)  # 观测

X_plus = np.zeros(shape=(length,))
# 设置初值，假设X_plus1[0]~N(0.01,0.01^2)，对初值比较自信，方差小一些
X_plus[0] = 0.1
P_plus = 0.1
Q = 0.1
R = 1

for i in range(1, length):
    # 预测步
    A = 3 * np.cos(3 * X_plus[i - 1])
    if type(A) == np.float64:
        A = np.asarray(A).reshape(-1, 1)
    X_minus = np.sin(3 * X_plus[i - 1])
    P_minus = A.dot(P_plus).dot(A.T) + Q

    # 更新步
    C = 2 * X_minus
    if type(C) == np.float64:
        C = np.asarray(C).reshape(-1, 1)
    K = P_minus.dot(C).dot(np.linalg.inv(C.dot(P_minus).dot(C.T) + R))
    X_plus[i] = X_minus + K.dot(y[i] - X_minus ** 2)
    P_plus = (np.eye(1) - K.dot(C)).dot(P_minus)

plt.plot(time, x, label="real value")
plt.plot(time, y, label="observed value")
plt.plot(time, X_plus, label="predicted value")
plt.legend()
plt.show()