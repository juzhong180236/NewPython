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
    sam_number = 46  # 最后得到的样本个数
    bounds = [[0, 72], [5, 50]]
    samples = LHSample(var_type, bounds, sam_number)
    XY = np.array(samples)
    X = XY[:, 0]
    Y = XY[:, 1]
    # print(np.around(XY, 1))
    xs = (bounds[0][1] - bounds[0][0]) / sam_number
    ys = (bounds[1][1] - bounds[1][0]) / sam_number
    pl.figure(figsize=(10, 8))
    ax = pl.gca()
    # pl.ylim(bounds[1][0] - ys, bounds[1][1] + ys)
    # pl.xlim(bounds[0][0] - xs, bounds[0][1] + xs)
    pl.xlim(bounds[0][0], bounds[0][1])
    pl.ylim(bounds[1][0], bounds[1][1])
    x_ticks = np.arange(0, bounds[0][1] + 6, 6)
    y_ticks = np.arange(bounds[1][0], bounds[1][1] + 5, 5)
    pl.yticks(y_ticks)
    pl.xticks(x_ticks)
    pl.tick_params(labelsize=15)
    pl.yticks(y_ticks, weight='semibold')
    pl.xticks(x_ticks, weight='semibold')
    ax.set_axisbelow(True)  # 网格线靠后
    pl.grid()
    pl.xlabel("The degree of luffing angle (deg)", fontsize=24, weight='semibold')
    pl.ylabel("The mass of lifting load (Kg)", fontsize=24, weight='semibold')
    # ax.xaxis.set_major_locator(MultipleLocator(xs))
    # ax.yaxis.set_major_locator(MultipleLocator(ys))
    """2020.12.27
    手动添加边缘点
    """
    X = np.append(X, [0, 0, 72, 72, 24, 48])
    Y = np.append(Y, [5, 50, 5, 50, 20, 35])
    pl.scatter(X, Y, clip_on=False)  # 边缘点显示
    # pl.savefig(r"C:\Users\asus\Desktop\pics\samples.png", bbox_inches='tight')
    file_name = "50.tif"
    pl.savefig(
        r"D:\Alai\paper_Alai\【1】期刊论文\【1】Journal of Mechanical Design\起重机臂架论文\提交过程\【2】第一次审回\图片更新_visio\Fig 4 figures\\" + file_name,
        bbox_inches='tight')

    """2020.12.27
    高保真手动画图
    """
    # # 50
    # X1 = np.array([24, 48, 36])
    # Y1 = np.array([20, 35, 27.5])
    #
    # # 100_2
    # # X1 = np.array([48, 36])
    # # Y1 = np.array([35, 27.5])
    #
    # # 100_3
    # # X1 = np.array([24, 36])
    # # Y1 = np.array([20, 27.5])
    #
    # # 100_6
    # # X1 = np.array([24, 48])
    # # Y1 = np.array([20, 35])
    #
    # # 150_2
    # # X1 = np.array([24])
    # # Y1 = np.array([20])
    #
    # # 150_3
    # # X1 = np.array([48])
    # # Y1 = np.array([35])
    #
    # # 150_6
    # # X1 = np.array([36])
    # # Y1 = np.array([27.5])
    #
    # # 200
    # # X1 = np.array([])
    # # Y1 = np.array([])
    #
    # X1 = np.append(X1, [0, 0, 72, 72])
    # Y1 = np.append(Y1, [5, 50, 5, 50])
    #
    # file_name = "50.tif"
    # pl.scatter(X1, Y1, clip_on=False, c='r', s=200)  # 边缘点显示
    # pl.savefig(
    #     r"D:\Alai\paper_Alai\【1】期刊论文\【1】Journal of Mechanical Design\起重机臂架论文\提交过程\【2】第一次审回\图片更新_visio\Fig 4 figures\\" + file_name,
    #     bbox_inches='tight')
    # # pl.show()
