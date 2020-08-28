import numpy as np
import matplotlib.pyplot as plt
from ReadExcel import readExcel
import os
import printf as pf
from Train_point_data import Training_Points_Data
from rbf_2020 import RBF
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import Error_estimates as es
import sklearn.gaussian_process.kernels as kns
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import ConstantKernel
from GPR import GPR

"""
"""


def Read_TData(path, _row_index):
    data_y, data_x = readExcel(path, row_index=_row_index, column_index=4, y_column=1)
    return data_x, data_y


def Read_SData(path):
    isExisted = os.path.exists(path)
    if not isExisted:
        pf.printf(path)
        pf.printf('上面列出的路径不存在，请设置正确路径！')
        return
    else:
        pf.printf('目录[' + path + ']存在,正在读取...')

    list_different_angle = []

    file_content = open(path, 'rt')
    list_1 = []
    list_2 = []
    list_3 = []
    list_4 = []
    list_5 = []
    list_6 = []
    list_7 = []
    list_8 = []
    list_angle = []
    i = 0
    for line in file_content:
        i += 1
        if i % 16 == 1:
            list_1.append(np.abs(float(line)))
        elif i % 16 == 2:
            list_angle.append(float(line))
        elif i % 16 == 3:
            list_2.append(float(line))
        elif i % 16 == 5:
            list_3.append(float(line))
        elif i % 16 == 7:
            list_4.append(float(line))
        elif i % 16 == 9:
            list_5.append(float(line))
        elif i % 16 == 11:
            list_6.append(float(line))
        elif i % 16 == 13:
            list_7.append(float(line))
        elif i % 16 == 15:
            list_8.append(float(line))
        else:
            continue
    file_content.close()
    return list_1, list_2, list_3, list_4, list_5, list_6, list_7, list_8, list_angle


def mkdir(path_dir):
    import os
    path_dir = path_dir.strip()
    path_dir = path_dir.rstrip("\\")
    isExists = os.path.exists(path_dir)
    if not isExists:
        os.mkdir(path_dir)
        print(path_dir + ' 创建成功')
        return True
    else:
        print(path_dir + ' 目录已存在')
        return False


def Plot_Simulation_Test(_num, _simulation_index, _simulation_number, _simulate_point, _test_point, _path_train,
                         _x_train):
    fig = plt.figure(figsize=(12, 6), dpi=100)
    if _simulate_point == 8:
        plt.title('Sample Point No.' + str(2) + ' (' + str(load) + 'kg)', fontsize=24)
    elif _simulate_point == 5:
        plt.title('Sample Point No.' + str(4) + ' (' + str(load) + 'kg)', fontsize=24)
    else:
        plt.title('Sample Point No.' + str(_simulate_point) + ' (' + str(load) + 'kg)', fontsize=24)
    # plt.title('Luffing angle of the crane boom (30kg)', fontsize=24)
    # 实验
    plot_1 = plt.plot(list_test_data[0][0:_num], list_test_data[1][_test_point - 1][0:_num], label="Test Stress",
                      linewidth=1.5)
    # RBF
    list_diverse_conditions_w = Read_W(_path_train)
    rbf = RBF(w=np.asarray(list_diverse_conditions_w[_simulation_number][_simulate_point - 1]))
    rbf.x = _x_train
    x_pre = np.asarray(list_real_time_simulation_data[-1][_simulation_index:_num + _simulation_index])
    list_predict_data_RBF = rbf.predict(x_pre)
    plot_2 = plt.plot(list_test_data[0][0:_num], list_predict_data_RBF, label="SPI-DT Stress", linewidth=1.5)
    # 不确定性
    # rbf_uncertainty = np.random.normal(0, 0.1, size=len(list_predict_data_RBF))
    # plt.plot(list_test_data[0][0:_num], list_predict_data_RBF + rbf_uncertainty,
    #          label="SPI-DT Stress", linewidth=1.5)
    # plt.fill_between(list_test_data[0][0:_num], list_predict_data_RBF + 1.8 + rbf_uncertainty,
    #                  list_predict_data_RBF - 1.5 + rbf_uncertainty, alpha=0.2)
    # R2
    RR = 1 - (np.sum(np.square(list_predict_data_RBF - list_test_data[1][_test_point - 1][0:_num])) / np.sum(
        np.square(list_predict_data_RBF - np.mean(list_predict_data_RBF))))
    # GPR
    # kernel = ConstantKernel(1.0, (1e-4, 1e4)) * kns.RBF(5, (1e-2, 1e2))
    # s_model = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=0)
    # s_model.fit(v_fd.reshape(-1, 1), np.asarray(list_train_data).reshape(-1, 1))
    # list_predict_data_GPR, cov = s_model.predict(x_pre.reshape(-1, 1),
    #                                              return_cov=True)
    # uncertainty = 1.96 * np.sqrt(np.diag(cov))
    # ax1.plot(list_test_data[0][0:_num], list_predict_data_GPR, label="SPI-DT Data")
    # ax1.fill_between(x_pre.ravel(), list_predict_data_GPR + uncertainty, list_predict_data_GPR - uncertainty, alpha=0.1)
    # 角度
    # plot_3 = plt.plot(list_test_data[0][0:_num], list_simulation_data[8][0:_num], label="luffing degree",
    #                   linestyle='-.')
    # gpr = GPR(optimize=True)
    # x_train = np.arange(0, 73)
    # gpr.fit(x_train.reshape(-1, 1), np.asarray(list_train_data).reshape(-1, 1))  #
    # mu, cov = gpr.predict(test_X)

    _plot = plot_1 + plot_2

    labs = [_p.get_label() for _p in _plot]
    # bbox_to_anchor=(x, y, 长, 宽),总图是1*1的 loc是bbox中落在xy位置的角点或中点
    plt.legend(_plot, labs, bbox_to_anchor=(0, 0.75, 1, 0.2), borderaxespad=0, ncol=3, loc="upper center", fontsize=20)
    #     # ax1.set_xlabel("Time (s)", fontsize=20)
    plt.xlabel("Time (s)", fontsize=20)
    plt.ylabel("Stress (Mpa)", fontsize=20)
    # plt.ylabel("Angle (deg)", fontsize=20)
    plt.ylim(0, stress_y_limit)
    plt.xlim(0, x_tick)
    x_ticks = np.arange(0, x_tick, 20)
    y_ticks = np.arange(0, stress_y_limit + 1, stress_y_limit / stress_y_limit_separate)
    # 坐标轴刻度字体大小
    BIGGER_SIZE = 18
    # plt.rc('font', size=SMALL_SIZE)  # controls default text sizes
    # plt.rc('axes', titlesize=SMALL_SIZE)  # fontsize of the axes title
    # plt.rc('axes', labelsize=MEDIUM_SIZE)  # fontsize of the x and y labels
    plt.rc('xtick', labelsize=BIGGER_SIZE)  # fontsize of the tick labels
    plt.rc('ytick', labelsize=BIGGER_SIZE)
    plt.yticks(y_ticks)
    plt.xticks(x_ticks)
    ax = plt.gca()
    # 指定 data  设置的bottom(也就是指定的x轴)绑定到y轴的0这个点上
    ax.spines['bottom'].set_position(('data', 0))
    ax.spines['left'].set_position(('data', 0))
    plt.grid(ls='--')  # x坐标轴的网格使用主刻度
    # RR = es.R2(list_test_data[1][i][0:_num], list_predict_data_RBF)
    M_1 = es.MY(list_test_data[1][_test_point - 1][0:_num], list_predict_data_RBF)
    M_2 = es.MY(list_predict_data_RBF, list_test_data[1][_test_point - 1][0:_num])
    # print("第" + str(_test_point) + "个点的偏差是：" + str(M_1))
    # print("第" + str(_test_point) + "个点的偏差是：" + str(M_2))
    # print(_path_train[:-3])
    # plt.savefig(_path_train[:-3] + load + "_" + str(simulation_number) + r"\\" + str(_simulate_point) + '.png')
    # if _test_point == 2:
    plt.show()


def Plot_Luffing_Angle(_num, _simulation_index, _path_train):
    fig = plt.figure(figsize=(12, 6), dpi=100)

    plt.title('Luffing angle of the crane boom (' + str(load) + 'kg)', fontsize=24)
    # 角度
    plot_3 = plt.plot(list_test_data[0][0:_num],
                      list_real_time_simulation_data[8][_simulation_index:_num + _simulation_index],
                      label="luffing degree",
                      linestyle='-')
    _plot = plot_3

    labs = [_p.get_label() for _p in _plot]
    # bbox_to_anchor=(x, y, 长, 宽),总图是1*1的 loc是bbox中落在xy位置的角点或中点
    plt.legend(_plot, labs, bbox_to_anchor=(0, 0.75, 1, 0.2), borderaxespad=0, ncol=3, loc="upper right", fontsize=20)
    plt.xlabel("Time (s)", fontsize=20)
    plt.ylabel("Angle (deg)", fontsize=20)
    plt.ylim(0, 91)
    plt.xlim(0, x_tick)
    x_ticks = np.arange(0, x_tick, 20)
    y_ticks = np.arange(0, 91, 10)

    SMALL_SIZE = 8
    MEDIUM_SIZE = 10
    BIGGER_SIZE = 20

    # plt.rc('font', size=SMALL_SIZE)  # controls default text sizes
    # plt.rc('axes', titlesize=SMALL_SIZE)  # fontsize of the axes title
    # plt.rc('axes', labelsize=MEDIUM_SIZE)  # fontsize of the x and y labels
    plt.rc('xtick', labelsize=BIGGER_SIZE)  # fontsize of the tick labels
    plt.rc('ytick', labelsize=BIGGER_SIZE)  # fontsize of the tick labels
    # plt.rc('legend', fontsize=SMALL_SIZE)  # legend fontsize
    # plt.rc('figure', titlesize=BIGGER_SIZE)
    plt.yticks(y_ticks)
    plt.xticks(x_ticks)
    ax = plt.gca()
    # 指定 data  设置的bottom(也就是指定的x轴)绑定到y轴的0这个点上
    ax.spines['bottom'].set_position(('data', 0))
    ax.spines['left'].set_position(('data', 0))
    plt.grid()  # x坐标轴的网格使用主刻度
    plt.savefig(_path_train[:-3] + load + "_" + str(simulation_number) + r"\\luffing_angle.png")
    # plt.show()


def Read_W(_path_train):
    list_diverse_conditions_w = []
    w_files = os.listdir(_path_train)
    for i_path_train in range(len(w_files)):
        isExisted = os.path.exists(_path_train)
        if not isExisted:
            pf.printf(_path_train)
            pf.printf('上面列出的路径不存在，请设置正确路径！')
        else:
            pass
            # pf.printf('目录[' + _path_train + ']存在,正在读取...')
        list_same_condition_w = []
        file_content = open(_path_train + str(i_path_train) + ".txt", 'rt')
        # 将训练数据得到的权重w给出
        for line in file_content:
            list_same_condition_w.append(list(map(float, line.strip("\n").split(','))))
        list_diverse_conditions_w.append(list_same_condition_w)
    return list_diverse_conditions_w


if __name__ == "__main__":
    # 存储路径：应变仪采集的数据和在采集时实时仿真出来的数据
    path_test = r"D:\Alai\paper_Alai\Papers_v1\1\v2\Papers\paper_result_truss\20200713_stress_data\\"
    # 测试数据文件名，实时仿真数据的文件名
    load = "25"  # 10 15 20 23 23_2 25_1 25 30 35 40 实际的重物质量(kg)
    simulation_number = 500  # 300 400 200 600 500 700 800 仿真的重物重力(N)
    row_index = 3  # 因为应变采集仪在开始测量的时候总是慢一拍，所以要调整到和仿真的一致，从3开始调
    simulation_index = 5  # 仿真的偏移值
    stress_y_limit = 35  # y刻度最大值
    stress_y_limit_separate = 5  # y刻度分度数
    x_tick = 108  # x的最大值

    simulation_number_dic = {300: 0, 400: 1, 200: 2, 600: 3, 500: 4, 700: 5, 800: 6}
    x_train = np.arange(0, 73)
    # 读取实时仿真数据，共9个list，前8个为应力的时序数据，最后1个为角度的时序数据
    list_real_time_simulation_data = Read_SData(path_test + load + r".txt")
    # 读取实验数据，共2个list，第1个为应力数据的时序时间，第2个为8个应力点组成的二维list，里面有8个list，存储每个点的测试应力数据
    list_test_data = Read_TData(path_test + load + r".xlsx", row_index)
    # 因为开启两个采样的时间总会差一两秒，虽然采样频率一样，但是数据总个数会差一些，所以选择小的来对比
    # 不过要注意不要偏移了
    num = min(len(list_real_time_simulation_data[0]), len(list_test_data[1][0]))
    num_m = len(list_real_time_simulation_data[0]) - len(list_test_data[1][0])
    # print(len(list_real_time_simulation_data[0]))
    # print(len(list_test_data[1][0]))
    # print(num_m)
    # print(str(simulation_number) + "N   " + load + "kg  " + str(row_index) + "  " + str(simulation_index))
    # num = 531
    # 其实在上面的测试中，只需要有时序的角度数据就可以，这样可以用已经建立的模型来插值预测
    # 训练后的数据权重存放的路径
    path_train = r"D:\Alai\paper_Alai\Papers_v1\1\v2\Papers\paper_result_truss\20200713_stress_data\stress_point\w\\"

    # 创建文件夹
    mkdir(path_train[:-3] + load + "_" + str(simulation_number))
    # 读取RBF训练的权重w数据

    for i in range(1, 9):
    # 几个时序的点，仿真从第几个时序开始，仿真的哪个状态的数据，仿真第几个点，实验第几个点，仿真的训练权重读取路径,训练数据的已知点
        Plot_Simulation_Test(num, simulation_index, simulation_number_dic[simulation_number], i, i, path_train, x_train)
    Plot_Luffing_Angle(num, simulation_index, path_train)
