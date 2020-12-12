from __future__ import division

__author__ = 'wanghai'
import numpy as np
from matplotlib.ticker import MultipleLocator, FuncFormatter
import matplotlib.pyplot as pl


def LHSample(variables_type, variables_bounds, samples_number):
    '''
    :param variables_type:特征种类，或变量种类有几种
    :param variables_bounds:特征或变量对应范围（list）
    :param samples_number:最后得到的样本个数
    :return:样本数据
    '''
    # 创建空的ndarray用于存储最后的输出，layer_number*parameters_number
    # layer_number是最后的样本点数目，parameters_number是特征的个数
    result = np.empty([samples_number, variables_type])
    # 创建空的ndarray装每一个特征的样本点
    temp = np.empty([samples_number])

    d = 1.0 / samples_number

    for i in range(variables_type):

        # 以下两个for循环的作用是，抽取lay_number个随机数，比如lay_number=10，抽取10个随机数，
        # 然后将这10个随机数打乱，（第二个for循环）将这些打乱的随机数放到最终结果result的对应特征
        for j in range(samples_number):
            # 生成区间[low,high]上均匀分布随机数，生成一个一维随机数(list)，所以取[0]
            # 按照顺序在0-1之间取值，第一循环取0-1/layer_number，第二个循环取1/layer_number-2/layer_number
            # 依次类推
            temp[j] = np.random.uniform(low=j * d, high=(j + 1) * d, size=1)[0]
        # 洗牌，无返回值。对于多维度的array来说，只对第一维进行洗牌
        np.random.shuffle(temp)
        # 将得到的随机数放到结果样本的第一个特征的维度
        for j in range(samples_number):
            result[j, i] = temp[j]

    # 对样本数据进行拉伸
    b = np.asarray(variables_bounds)
    # 取所有特征的下界
    lower_bound = b[:, 0]
    # 取所有特征的上界
    upper_bound = b[:, 1]
    # 下界大于上界报错
    if np.any(lower_bound > upper_bound):
        print('范围出错')
        return None

    #   sample * (upper_bound - lower_bound) + lower_bound
    # 得到的均匀分布的随机数和上界减去下界的值相乘，
    # 相乘后的结果和下界相加，得到的结果就是我们需要的结果
    np.add(
        np.multiply(result, (upper_bound - lower_bound), out=result),
        lower_bound,
        out=result
    )
    return result


if __name__ == '__main__':
    var_type = 2
    sam_number = 64
    bounds = [[0, 72], [50, 400]]
    samples = LHSample(var_type, bounds, sam_number)
    XY = np.array(samples)
    X = XY[:, 0]
    Y = XY[:, 1]
    print(np.around(XY, 1))
    xs = (bounds[0][1] - bounds[0][0]) / sam_number
    ys = (bounds[1][1] - bounds[1][0]) / sam_number
    ax = pl.gca()
    # pl.ylim(bounds[1][0] - ys, bounds[1][1] + ys)
    # pl.xlim(bounds[0][0] - xs, bounds[0][1] + xs)
    pl.xlim(bounds[0][0], bounds[0][1])
    pl.ylim(bounds[1][0], bounds[1][1])
    x_ticks = np.arange(0, bounds[0][1] + 3, 3)
    y_ticks = np.arange(bounds[1][0], bounds[1][1] + 25, 25)
    pl.yticks(y_ticks)
    pl.xticks(x_ticks)
    pl.grid()

    # ax.xaxis.set_major_locator(MultipleLocator(xs))
    # ax.yaxis.set_major_locator(MultipleLocator(ys))

    # print(len(samples))
    pl.scatter(X, Y)
    pl.show()
