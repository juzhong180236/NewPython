import numpy as np
import matplotlib.pyplot as plt

"""
x(i)=sin(x(i-1))+5*x(i-1)/(x(i-1)^2+1)+Q
y(i)=x(i)^2+R

注意，滤波之前一定要写出状态方程和观测方程形式
xk=F(xk-1)
大多数情况下，是不能直接得到xk和xk-1的关系

而是x=f(t)
要将x=f(t)转化为xk=F(xk-1),具体可以看第八讲，还有更精细的模型，可以看《数值分析》第九章《常微分方程的数值解法》
第八讲实际就是欧拉法

可以用改进欧拉法或龙格库塔法，这些方法可以得到,更精细的xk=F(xk-1)之间的关系

"""
# 粒子滤波不断调整Q,R以及重采样和粒子的个数

# 生成100个信号
# 时间序列 # 卡尔曼滤波里面有dt而这里没有，这里直接给出了xk和xk-1的关系，所以不需要dt
time = np.arange(0.01, 1, 0.01)
time = np.insert(time, len(time), 1)
length = len(time)
x = np.zeros(shape=(length,))
y = np.zeros(shape=(length,))

# 设定初值
x[0] = 0.1
y[0] = 0.01 ** 2

# 生成真实数据与观测数据
for i in range(1, length):
    x[i] = np.sin(x[i - 1]) + 5 * x[i - 1] / (x[i - 1] ** 2 + 1)  # 状态
    y[i] = x[i] ** 2 + np.random.normal(0, 1)  # 观测

# PF
# 设粒子集合
n = 100
x_old = np.zeros(shape=(n,))
x_new = np.zeros(shape=(n,))
x_plus = np.zeros(shape=(100,))  # x_plus用于存放滤波值，就是每一次后验概率的期望
w = np.zeros(shape=(n,))

# 设置初值x0(i),可以直接在正态分布中采样，如果对初值有自信，也可以让所有粒子都相同，

for i in range(n):
    x_old[i] = 0.1
    w[i] = 1 / n

# PF 核心
for i in range(1, length):

    # 预测步 由x0推出x1 对每一个粒子进行预测，得到下一步的粒子【位置变，权重未变】
    for j in range(n):
        # 观测噪声 Q
        x_old[j] = np.sin(x_old[j]) + 5 * x_old[j] / (x_old[j] ** 2 + 1) + np.random.normal(0, 0.1)  # 1 0.1
    # 预测步完毕

    # 更新步
    for j in range(n):
        # w(j)=w(j)*fR(...)
        # fR=(2*pi*R)^(-0.5)*exp(-((-y+x_old(j)^2)^2/(2*R)))
        # 状态噪声 R
        w[j] = np.exp(-((y[i] - x_old[j] ** 2) ** 2 / (2 * 0.1)))  # 0.00001 0.0001 0.001 0.1
    # 归一化
    w = w / np.sum(w)  # w/sum(w)与k*w/sum(k*w)结果一模一样
    # (2*pi*R)^(-0.5)是常数，w(j),如果每次都重采样，每次w(j)都会被设为1/n,也是常数，所以可以去掉
    # 重采样
    # N<1/sum(wi^2),若不是每次都是重采样，那么前面求w(j)那里就应该把w(j)乘上去

    # 生成数组c
    c = np.zeros(shape=(n,))
    # 数组c中第一个数字是w[0]
    c[0] = w[0]
    # 之后的数依次是w[0]+w[1],w[0]+w[1]+w[2],...,1最后一个是1
    for j in range(2, n):
        c[j] = c[j - 1] + w[j]
    # 生成随机数，看落在哪个区间，即重采样n个粒子，粒子个数要与之前相同
    a = np.random.uniform(size=n)
    for j in range(n):
        # a = np.random.uniform(0, 1)
        a_j = a[j]
        for k in range(n):
            if a_j < c[k]:  # 每一个原先的粒子与新采样的粒子比较，新采样的粒子属于哪个原先的粒子就把原先的粒子赋值给新的粒子
                x_new[j] = x_old[k]
                break  # 一定要break，否则重采样粒子会被最后一个粒子覆盖
    # 重采样完毕
    # 把新的粒子赋值给x_old，为下一步递推做准备
    x_old = x_new
    # 把权重设置为1/n
    for j in range(n):
        w[j] = 1 / n
    # 把每一步的后验概率期望赋值给x_plus
    x_plus[i] = np.sum(x_new) / n
plt.plot(time, x, label="real value", linewidth=2)
plt.plot(time, y, label="observed value")
plt.plot(time, x_plus, label="predicted value", linewidth=1)
plt.legend()
plt.show()

# y = x^2+R 似然概率是一个多峰分布，y=4,x=2或-2
# 非线性问题一步一个坑，处处是雷
# 如果问题本身性质就是强烈的非线性，比如多峰分布这种，粒子滤波并不能化腐朽为神奇；观测和状态方程不能两个都是多峰的，要不很难准确
# 粒子滤波的计算速度是大硬伤

# 以上代码准确是因为预测方程非常准确，在实际中很难找到很准的预测方程
