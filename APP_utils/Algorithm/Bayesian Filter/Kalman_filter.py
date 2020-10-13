import numpy as np
import matplotlib.pyplot as plt

# 时间序列
time = np.arange(0.1, 1, 0.01)
time = np.insert(time, len(time), 1)
length = len(time)

# 真实信号x
x = time ** 2
# 观测值y，带有正态分布的噪音 # 实际在大多数时候，观测值（信号）是杂乱无章的
y = x + np.random.normal(0, 0.1, size=length)
y2 = x + np.random.normal(0, 0.01, size=length)

Y = np.vstack([y, y2])


def Model_1():
    # 滤波算法
    # 【预测方程，观测方程】怎么写
    # 【观测方程】好写，Y(K)=X(K)+R R~N(0,1) Q和R的选择非常重要，但是得多次调试
    # 【预测方程】不好写，在这里大概可以猜是线性增长，但是大多数问题，信号是杂乱无章的，怎么办

    # 模型一，最粗糙的模型
    # X(K)=X(K-1)+Q f(X)系数为1的线性函数
    # Y(K)=X(K)+R   h(X)系数为1的线性函数
    # 猜 Q~N(0,1)
    F1 = np.array([1]).reshape(-1, 1)  # f(X)系数
    H1 = np.array([1]).reshape(-1, 1)  # h(X)系数
    # 调整Q和R
    Q1 = np.array([1]).reshape(-1, 1)  # Q的方差 调为0.01
    R1 = np.array([1]).reshape(-1, 1)  # R的方差 调为0.01

    X_plus1 = np.zeros(shape=length)

    # 设置初值，假设X_plus1[0]~N(0.01,0.01^2)，对初值比较自信，方差小一些
    X_plus1[0] = 0.01
    P_plus1 = 0.01 ** 2

    # 卡尔曼滤波算法
    # X(K)minus=F*X(K-1)plus K时刻先验分布的均值
    # P(K)minus=F*P(K-1)plus*F'+Q K时刻先验分布的方差
    # K=P(K)minus*H*inv(H*P(K)minus*H'+R) 卡尔曼增益
    # X(K)plus=X(K)minus+K*(y(k)-H*X(K)minus) K时刻的后验分布的均值
    # P(K)plus=(1-K*H)*P(K)minus K时刻后验分布的方差
    for i in range(1, length):
        # 预测步
        X_minus1 = F1.dot(X_plus1[i - 1])  # 通过k-1步后验的均值预测出k步的先验均值
        # Q1 = np.asarray(np.abs(np.random.normal(0, 0.5))).reshape(-1, 1)
        P_minus = F1.dot(P_plus1).dot(F1.T) + Q1  # 通过k-1步的后验方差预测k步的先验方差
        # 更新步
        # 卡尔曼增益
        K1 = P_minus.dot(H1.T).dot(np.linalg.inv(H1.dot(P_minus).dot(H1.T) + R1))
        X_plus1[i] = X_minus1 + K1.dot(y[i] - H1.dot(X_minus1))  # 用k步的先验均值和方差得到k步的后验方差
        P_plus1 = (1 - K1.dot(H1)).dot(P_minus)  # 用k步的先验方差得到k步的后验方差
    return X_plus1
    # plt.plot(time, x, label="real value")
    # plt.plot(time, y, label="observed value")
    # plt.plot(time, X_plus1, label="predicted value")
    # plt.legend()
    # plt.show()


# 模型二
# X(K)=X(K-1)+X’(K-1)*dt+X''(K-1)*dt^2*(1/2!)+Q2 f(X)为一个二阶的泰勒展开
# Y(K)=X(K)+R2   h(X)系数为1的线性函数
# 此时模型的状态变量 X = [X(K) X'(K) X''(K)].T 【列向量】
# Y(K)=H*X+R2 H=[1 0 0] 【行向量】
# X(K)=X(K-1)+X’(K-1)*dt+X''(K-1)*dt^2*(1/2!)+Q2
# X'(K)=0*X(K-1)+X’(K-1)+X''(K-1)*dt+Q3 对dt求导
# X''(K)=0*X(K-1)+0*X’(K-1)+X''(K-1)+Q4 对dt求导 和模型1类似，这个模型建立的很粗糙

# 有一个假设，信号是多项式函数，多次求导后总会比较平缓，就会与粗糙的高阶假设类似
# 所以对导数建立平稳的随机过程的模型比直接多项式函数建立平稳模型要好，除非信号是一个指数的，怎么求导都是指数
# 而X’‘(K)=X’‘(K-1)+Q4正是描述平缓的随机过程，这种建模相对精细一些，使用范围也较广
# 如果信号是指数，就不太好用了，但一般不太可能
# F = 1 dt 0.5*dt^2
#     0 1  dt
#     0 0  1
# H = [1 0 0]
# Q = Q2 0  0
#     0  Q3 0
#     0  0  Q4 预测噪声的协方差矩阵

# R2 观测只有一个，没有协方差矩阵。如果观测有两个，就应该写成协方差矩阵，但是这里只有一个
def Model_2():
    dt = time[1] - time[0]
    # 若dt特别小【传感器采样频率比较快】，dt的三次方、四次方、五次方……会导致精度丢失，认为是零
    # 从而丢失一个维度
    F2 = np.array([
        [1, dt, 0.5 * dt ** 2],
        [0, 1, dt],
        [0, 0, 1]
    ])
    H2 = np.array([[1, 0, 0]])  # 两层括号才是(1,3)向量，单层括号就是个(3,)
    # X(K)的噪声变化，X(K-1)的噪声如何变化，应该建立一个Q2的协方差矩阵
    Q2 = np.array([
        [1, 0, 0],
        [0, 0.01, 0],
        [0, 0, 0.0001]
    ])
    R2 = 20
    # 初值以及方差
    X_plus2 = np.zeros(shape=(3, length))
    X_plus2[0][0] = 0.01
    X_plus2[1][0] = 0
    X_plus2[2][0] = 0
    P_plus2 = np.array([
        [0.01, 0, 0],
        [0, 0.01, 0],
        [0, 0, 0.0001],
    ])
    for i in range(1, length):
        # 预测步
        # 因为通过[:,i-1]选出来的实际是个行向量,所以要加T转置为列向量
        X_minus2 = F2.dot(X_plus2[:, i - 1].T)
        P_minus2 = F2.dot(P_plus2).dot(F2.T) + Q2
        # 更新步 可以dot一个数字
        K2 = P_minus2.dot(H2.T).dot(np.linalg.inv((H2.dot(P_minus2).dot(H2.T) + R2)))
        # 因为通过[:,i]接收的其实是一个行向量，所以要把列向量转置，或者也可以用flatten或ravel对数组进行扁平化操作
        X_plus2[:, i] = (X_minus2 + K2.dot(y[i] - H2.dot(X_minus2).T)).T
        P_plus2 = (np.eye(3) - K2.dot(H2)).dot(P_minus2)
    return X_plus2[0]


# 问题2 两个传感器，进行滤波
# Y1(K)=X(K)+R
# Y2(K)=X(K)+R
# 模型一 H=[1 1].T 【列向量】X=X(K)
# 模型二 H = 1 0 0 X = [X(K) X'(K) X''(K)].T
#           1 0 0

def Model_3():
    dt = time[1] - time[0]
    # 若dt特别小【传感器采样频率比较快】，dt的三次方、四次方、五次方……会导致精度丢失，认为是零
    # 从而丢失一个维度
    F3 = np.array([
        [1, dt, 0.5 * dt ** 2],
        [0, 1, dt],
        [0, 0, 1]
    ])
    H3 = np.array([[1, 0, 0], [1, 0, 0]])  # 两层括号才是(1,3)向量，单层括号就是个(3,)
    # X(K)的噪声变化，X(K-1)的噪声如何变化，应该建立一个Q2的协方差矩阵
    Q3 = np.array([
        [1, 0, 0],
        [0, 0.01, 0],
        [0, 0, 0.0001]
    ])
    R3 = np.array([
        [3, 0],
        [0, 3],
    ])
    # 初值以及方差
    X_plus3 = np.zeros(shape=(3, length))
    X_plus3[0][0] = 0.01
    X_plus3[1][0] = 0
    X_plus3[2][0] = 0
    P_plus3 = np.array([
        [0.01, 0, 0],
        [0, 0.01, 0],
        [0, 0, 0.0001],
    ])
    for i in range(1, length):
        # 预测步
        # 因为通过[:,i-1]选出来的实际是个行向量,所以要加T转置为列向量
        X_minus3 = F3.dot(X_plus3[:, i - 1].T)
        P_minus3 = F3.dot(P_plus3).dot(F3.T) + Q3
        # 更新步 可以dot一个数字
        K3 = P_minus3.dot(H3.T).dot(np.linalg.inv((H3.dot(P_minus3).dot(H3.T) + R3)))
        # 因为通过[:,i]接收的其实是一个行向量，所以要把列向量转置，或者也可以用flatten或ravel对数组进行扁平化操作
        X_plus3[:, i] = (X_minus3 + K3.dot(Y[:, i] - H3.dot(X_minus3).T)).T
        P_plus3 = (np.eye(3) - K3.dot(H3)).dot(P_minus3)

    return X_plus3[0]


M_1 = Model_1()
M_2 = Model_2()
M_3 = Model_3()

plt.plot(time, x, label="real value")
plt.plot(time, y, label="observed value")
plt.plot(time, M_1, label="predicted value 1")
plt.plot(time, M_2, label="predicted value 2")
plt.plot(time, M_3, label="predicted value 3")
plt.legend()
plt.show()
