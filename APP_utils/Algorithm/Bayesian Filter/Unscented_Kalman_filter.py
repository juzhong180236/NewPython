import numpy as np
import matplotlib.pyplot as plt

"""
很多变量，很多行向量，很多列向量
plus +
minus -
hat
"""

# 生成100个信号
# 时间序列
time = np.arange(0.01, 1, 0.01)
time = np.insert(time, len(time), 1)
length = len(time)

# 真实值x和观测值z
x = np.zeros(shape=(2, length))
z = np.zeros(shape=(2, length))

x[0, 0] = 0.2
x[1, 0] = 0.2

# 非线性的预测方程
# 生成真实数据与观测数据
for i in range(1, length):
    x[0, i] = np.sin(x[0, i - 1]) + 2 * np.cos(x[1, i - 1])  # 状态
    x[1, i] = 3 * np.cos(x[0, i - 1]) + np.sin(x[1, i - 1])  # 状态
    z[0, i] = x[0, i] + x[1, i] ** 3 + np.random.normal(0, 1)  # 观测
    z[1, i] = x[0, i] ** 3 + x[1, i] + np.random.normal(0, 1)  # 观测

plt.plot(time, z[0, :], label="real value")
plt.plot(time, z[1, :], label="observed value")
plt.legend()
plt.show()
