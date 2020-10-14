import math
import matplotlib.pyplot as plt
import numpy as np
import pylab as mpl


def clip(x, path):
    for i in range(len(x)):
        if x[i] >= path:
            x[i] %= path


if __name__ == "__main__":
    # sans-serif就是无衬线字体，是一种通用字体族
    mpl.rcParams['font.sans-serif'] = [u'SimHei']  # 指定默认字体
    mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
    path = 5000  # 环形公路的长度
    n = 100  # 公路上的车辆数量
    v0 = 5  # 车辆的初始速度
    p = 0.3  # 随机减速概率
    Times = 3000

    np.random.seed(0)
    x = np.random.rand(n) * path
    x.sort()
    v = np.tile([v0], n).astype(np.float)

    plt.figure(figsize=(10, 8), facecolor="w")
    for t in range(Times):
        plt.scatter(x, [t] * n, s=1, c='k', alpha=0.05)
        for i in range(n):
            if x[(i + 1) % n] > x[i]:
                d = x[(i + 1) % n] - x[i]  # 距离前车的距离
            else:
                d = path - x[i] + x[(i + 1) % n]
            if v[i] < d:
                if np.random.rand() > p:
                    v[i] += 1
                else:
                    v[i] -= 1
            else:
                v[i] = d - 1
        v = v.clip(0, 150)
        x += v
        clip(x, path)
    plt.xlim(0, path)
    plt.ylim(0, Times)
    plt.xlabel(u"车辆位置", fontsize=16)
    plt.ylabel(u"模拟时间", fontsize=16)
    plt.title(u"环形公路堵车模型", fontsize=16)
    plt.tight_layout(pad=2)
    plt.show()
