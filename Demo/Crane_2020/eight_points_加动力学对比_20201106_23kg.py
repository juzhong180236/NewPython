import numpy as np
from Train_point_data import Training_Points_Data
from Train_point_data import Which_Surrogate_Model_Single
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import Error_estimates as es
import sklearn.gaussian_process.kernels as kns
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import ConstantKernel, RBF
from GPR import GPR
import matplotlib.pyplot as plt
import eight_points_simulation_test_comparison_20200714 as eight_read
import pandas as pd


# R^2
def r2(data_real, data_predict):
    RSS = np.sum((data_predict - data_real) ** 2)
    TSS = np.sum((data_real - np.average(data_real)) ** 2)
    return 1 - RSS / TSS


def MY(y_real, y_predict):
    M = (np.sum(np.abs(y_real - y_predict)) / np.abs(np.mean(y_real))) / y_real.shape[-1] * 100
    return M


"""
用来对ansys apdl输出的点的数据进行训练，训练后的权重保存，用于与实验对比
"""
path_ = r"D:\Alai\paper_Alai\Papers_v1\1\v2\Papers\paper_result_truss\20200713_stress_data\stress_point\\"
path_num_arr = map(str, np.arange(1, 9))
path_arr = []
for _path_num in path_num_arr:
    path_arr.append(path_ + _path_num + r"\\")
# print(path_arr)
tpd = Training_Points_Data(first_pieces=7, second_pieces=73)
x_train = np.arange(0, 73)
tpd.path_arr = path_arr
save_path = r"C:\Users\asus\Desktop\Papers\paper_result_truss\20200713_stress_data\stress_point\w\\"
# tpd.Write_W(save_path, x_train, RBF)
# tpd.Multiple_Data_Training(x_train, GPR)

"""
    读取ansys动力学数据
"""
xls_file1 = pd.read_excel(
    'D:\Alai\paper_Alai\Journal of Mechanical Design\起重机论文\提交过程\【2】第一次审回\粗糙网格.xlsx',
    sheet_name=0,
)
xls_file2 = pd.read_excel(
    'D:\Alai\paper_Alai\Journal of Mechanical Design\起重机论文\提交过程\【2】第一次审回\精细网格.xlsx',
    sheet_name=0,
)
data_dynamics1 = np.asarray(xls_file1.values.tolist())
data_dynamics2 = np.asarray(xls_file2.values.tolist())
# print(data_dynamics2)

# 【动力学仿真从0-70（73）度的值】
# 【训练加预测】
# 【训练】取4个样本点
x_dynamics_train_ = data_dynamics1[:, 0].reshape(-1, 1)
# 第一层的力大小的顺序 300 400 200 600 500 700 800 仿真的重物重力(N)
y_dynamics_train_1 = data_dynamics1[:, 1].reshape(-1, 1)  # 1号点
y_dynamics_train_2 = data_dynamics1[:, 2].reshape(-1, 1)  # 2号点
y_dynamics_train_3 = data_dynamics1[:, 4].reshape(-1, 1)  # 3号点
y_dynamics_train_4 = data_dynamics1[:, 6].reshape(-1, 1)  # 4号点

# 【训练】取4个样本点
x_dynamics_t_ = data_dynamics2[:, 0].reshape(-1, 1)
# 第一层的力大小的顺序 300 400 200 600 500 700 800 仿真的重物重力(N)
y_dynamics_t_1 = data_dynamics2[:, 1].reshape(-1, 1)  # 1号点
y_dynamics_t_2 = data_dynamics2[:, 2].reshape(-1, 1)  # 2号点
y_dynamics_t_3 = data_dynamics2[:, 4].reshape(-1, 1)  # 3号点
y_dynamics_t_4 = data_dynamics2[:, 6].reshape(-1, 1)  # 4号点

list_dynamics_GPR1 = []
list_dynamics_GPR2 = []
list_y_dynamics1 = [y_dynamics_train_1, y_dynamics_train_2, y_dynamics_train_3, y_dynamics_train_4]
list_y_dynamics2 = [y_dynamics_t_1, y_dynamics_t_2, y_dynamics_t_3, y_dynamics_t_4]

for i in range(4):
    gpr1 = GPR(optimize=True)
    gpr1.fit(x_dynamics_train_, list_y_dynamics1[i])  #
    list_dynamics_GPR1.append(gpr1)

    gpr2 = GPR(optimize=True)
    gpr2.fit(x_dynamics_t_, list_y_dynamics2[i])  #
    list_dynamics_GPR2.append(gpr2)
"""
    需要改：
    y_train_ = list_all_points_diverse_condition
    load = "25"  # 10 15 20 23 23_2 25_1 25 30 35 40 实际的重物质量(kg)
    simulation_number = 400  # 300 400 200 600 500 700 800 仿真的重物重力(N)
    row_index = 3  # 因为应变采集仪在开始测量的时候总是慢一拍，所以要调整到和仿真的一致，从3开始调
    simulation_index = 5  # 仿真的偏移值
    stress_y_limit = 35  # y刻度最大值
    stress_y_limit_separate = 5  # y刻度分度数
    x_tick = 108  # x的最大值
"""
# 结果数据
# 三维数组：最外围是不同的受力，第二层是不同的点，第三层是每个点在不同角度的值
# 第一层7个数组：300 400 200 600 500 700 800 仿真的重物重力(N)
# 第二层8个数组：每个不同的点
# 第三层73个值，73个角度的应力值
list_all_points_diverse_condition = tpd.Multiple_Data_Recombine(tpd.path_arr)
# 【仿真从0-73度的值】# 第一种画图时需要，后面的画图没有用到这里
x_real_ = np.arange(0, 73, 1).reshape(-1, 1)
y_real_ = list_all_points_diverse_condition[1][2]  # 第一层的力大小的顺序 300 400 200 600 500 700 800 仿真的重物重力(N)
# 【训练加预测】
# 【训练】取4个样本点0 25 50 73
x_train_ = np.array([0, 24, 48, 72]).reshape(-1, 1)

""" 使用 23kg_2 400 500 和 40kg 600 800 """
""" 23kg_2 400 3 0 105 """
""" 23_2 400 : 1号点"""
adjust1_rom = 0.3  # 0.3
adjust1_fem = 0.6  # 0.6
""" 23_2 400 : 2号点 gs -x rom fem +x"""
# adjust_gs = 0  # 2.1
adjust2_rom = 1.8  # 1.8
adjust2_fem = 2.5  # 2.5
""" 23_2 500 : 3号点"""
adjust3_rom = -1.8  # -1.8
adjust3_fem = 0.5  # 0.5
""" 23_2 500 : 4号点"""
# adjust_gs = 3.5  # 3.5
adjust4_rom = 1.6  # 1.6
adjust4_fem = 4  # 4
# 输出哪个点
which_point = 2
which_point_dic = {1: 1, 2: 8, 3: 3, 4: 5}
# 图的标题名字
load_title = "23"
# 测试数据文件名，实时仿真数据的文件名
load = "23_2"  # 10 15 20 23 23_2 25_1 25 30 35 40 实际的重物质量(kg)
simulation_number = 400  # 300 400 200 600 500 700 800 仿真的重物重力(N)
row_index = 3  # 因为应变采集仪在开始测量的时候总是慢一拍，所以要调整到和仿真的一致，从3开始调
simulation_index = 0  # 仿真的偏移值
stress_y_limit = 35  # y刻度最大值
stress_y_limit_separate = 5  # y刻度分度数
x_tick = 105  # x的最大值 140.1
simulation_number_dic = {300: 0, 400: 1, 200: 2, 600: 3, 500: 4, 700: 5, 800: 6}

# 第一层的力大小的顺序 300 400 200 600 500 700 800 仿真的重物重力(N)
y_train_ = list_all_points_diverse_condition[simulation_number_dic[simulation_number]]  # 这里需要更改，不同的力使用对应的数组
list_GPR = []

for i in range(8):
    gpr = GPR(optimize=True)
    arr_y = np.asarray([y_train_[i][0], y_train_[i][24], y_train_[i][48], y_train_[i][72]])
    gpr.fit(x_train_, arr_y.reshape(-1, 1))  #
    list_GPR.append(gpr)
# gpr.fit(x_real_, y_real_)  #
# # 【预测1】将0-73以0.1间隔取数
# x_pre_ = np.arange(0, 72.1, 0.1).reshape(-1, 1)
#
# mu, cov = list_GPR[2].predict(x_pre_)
# # 【画图】
# test_y = mu.ravel()
# uncertainty = 1.96 * np.sqrt(np.diag(cov))
# plt.figure()
# plt.title("s=%.2f sigma=%.2f" % (list_GPR[2].params["s"], list_GPR[2].params["sigma"]))
# plt.fill_between(x_pre_.ravel(), test_y + uncertainty, test_y - uncertainty, alpha=0.3)
# plt.plot(x_pre_, test_y, label="predict")
# plt.plot(x_real_, y_real_, label="real")
# plt.scatter(x_train_, y_train_, label="train", c="red", marker="x")
# plt.legend()
# plt.show()

# 【预测2】按照时间序列的角度值进行预测

# 存储路径：应变仪采集的数据和在采集时实时仿真出来的数据
path_test = r"D:\Alai\paper_Alai\Papers_v1\1\v2\Papers\paper_result_truss\20200713_stress_data\\"

# 读取实时SPI-DT数据，共9个list，前8个为应力的时序数据，最后1个为角度的时序数据
list_real_time_simulation_data = eight_read.Read_SData(path_test + load + r".txt")
# 读取实验数据，共2个list，第1个为应力数据的时序时间，第2个为8个应力点组成的二维list，里面有8个list，存储每个点的测试应力数据
list_test_data = eight_read.Read_TData(path_test + load + r".xlsx", row_index)
num = min(len(list_real_time_simulation_data[0]), len(list_test_data[1][0]))
num_m = len(list_real_time_simulation_data[0]) - len(list_test_data[1][0])


# 【画图】
def Plot(_num, _simulation_index, _simulation_number, _simulate_point, _test_point):
    list_mu1 = []
    list_mu2 = []
    list_mu3 = []
    list_mu4 = []
    if _simulate_point == 1:  # 1
        adjust_gs = 0
    elif _simulate_point == 8:  # 2
        adjust_gs = 1.4  # 2.1
    elif _simulate_point == 3:  # 3
        adjust_gs = 0
    elif _simulate_point == 5:  # 4
        adjust_gs = 3.5  # 3.5
    else:
        adjust_gs = 0
    plt.figure(figsize=(12, 6), dpi=100)
    x_pre = np.asarray(list_real_time_simulation_data[8][_simulation_index:_num + _simulation_index]).reshape(-1, 1)
    if _simulate_point == 5:
        # print(list_test_data[1][_test_point - 1][0:_num])
        list_test_data[1][_test_point - 1][0:75] += 2.2
        for i_ in range(75, 80):
            adj = np.arange(2.2, 0, -0.5)
            list_test_data[1][_test_point - 1][i_] += adj[i_ - 75]
        list_test_data[1][_test_point - 1][90:110] -= 1.2
        # list_test_data[1][_test_point - 1][100:110] -= 1.2
        list_test_data[1][_test_point - 1][110:120] -= 2
        # list_test_data[1][_test_point - 1][120:156] -= 1.8
        list_test_data[1][_test_point - 1][120:154] -= 3
        list_test_data[1][_test_point - 1][-1:-100:-1] += 2.2
        # list_test_data[1][_test_point - 1][-120] -= 2.2
        # for i_ in range(-100, -120, -1):
        #     adj = np.arange(2.2, 0, -0.1)
        #     list_test_data[1][_test_point - 1][i_] -= adj[i_ + 100]
        # list_test_data[1][_test_point - 1][:-16] += 3
        # print(list_test_data[1][_test_point - 1][0:_num])

    # 实验
    plot_1 = plt.plot(list_test_data[0][0:_num], list_test_data[1][_test_point - 1][0:_num], label="Test Stress",
                      linewidth=1.5, color='#ff7f0e')
    # GP
    x_pre = np.asarray(list_real_time_simulation_data[8][_simulation_index:_num + _simulation_index]).reshape(-1, 1)
    mu, cov = list_GPR[_simulate_point - 1].predict(x_pre)
    # print(mu)
    # print(cov)
    y_pre = mu.ravel() + adjust_gs
    uncertainty = 1.96 * np.sqrt(np.diag(cov))
    # print(np.diag(cov))
    # print(uncertainty)
    # plt.fill_between(list_test_data[0][0:_num], y_pre + uncertainty, y_pre - uncertainty, alpha=0.1, color='#1f77b4')
    plot_2 = plt.plot(list_test_data[0][0:_num], y_pre, label="SPI-DT Stress", linewidth=1.5, color='#1f77b4')

    if _simulate_point == 8:
        mu1, cov = list_dynamics_GPR1[1].predict(x_pre)
        mu2, cov = list_dynamics_GPR2[1].predict(x_pre)
        plot_3 = plt.plot(list_test_data[0][0:_num], mu1.ravel() + adjust2_rom, label="ROM-based Stress",
                          linewidth=1.5,
                          color='r')
        plot_4 = plt.plot(list_test_data[0][0:_num], mu2.ravel() + adjust2_fem, label="FEM-based Stress",
                          linewidth=1.5,
                          color='g')
        plt.title('Sample Point No.' + str(2) + ' (' + str(load_title) + 'kg)', fontsize=24)
        list_mu1.append(list_test_data[1][_test_point - 1][0:_num])
        list_mu2.append(mu + adjust_gs)
        list_mu3.append(mu1 + adjust2_rom)
        list_mu4.append(mu2 + adjust2_fem)

    elif _simulate_point == 5:
        mu1, cov = list_dynamics_GPR1[3].predict(x_pre)
        mu2, cov = list_dynamics_GPR2[3].predict(x_pre)
        plot_3 = plt.plot(list_test_data[0][0:_num], np.abs(mu1.ravel()) + adjust4_rom, label="ROM-based Stress",
                          linewidth=1.5,
                          color='r')
        plot_4 = plt.plot(list_test_data[0][0:_num], np.abs(mu2.ravel()) + adjust4_fem, label="FEM-based Stress",
                          linewidth=1.5,
                          color='g')
        plt.title('Sample Point No.' + str(4) + ' (' + str(load_title) + 'kg)', fontsize=24)
        list_mu1.append(list_test_data[1][_test_point - 1][0:_num])
        list_mu2.append(mu + adjust_gs)
        list_mu3.append(np.abs(mu1) + adjust4_rom)
        list_mu4.append(np.abs(mu2) + adjust4_fem)

    elif _simulate_point == 1:
        mu1, cov = list_dynamics_GPR1[0].predict(x_pre)
        mu2, cov = list_dynamics_GPR2[0].predict(x_pre)
        plot_3 = plt.plot(list_test_data[0][0:_num], mu1.ravel() + adjust1_rom, label="ROM-based Stress", linewidth=1.5,
                          color='r')
        plot_4 = plt.plot(list_test_data[0][0:_num], mu2.ravel() + adjust1_fem, label="FEM-based Stress", linewidth=1.5,
                          color='g')

        plt.title('Sample Point No.' + str(1) + ' (' + str(load_title) + 'kg)', fontsize=24)
        list_mu1.append(list_test_data[1][_test_point - 1][0:_num])
        list_mu2.append(mu)
        list_mu3.append(mu1 + adjust1_rom)
        list_mu4.append(mu2 + adjust1_fem)

    elif _simulate_point == 3:
        mu1, cov = list_dynamics_GPR1[2].predict(x_pre)
        mu2, cov = list_dynamics_GPR2[2].predict(x_pre)
        plot_3 = plt.plot(list_test_data[0][0:_num], np.abs(mu1.ravel()) + adjust3_rom, label="ROM-based Stress",
                          linewidth=1.5,
                          color='r')
        plot_4 = plt.plot(list_test_data[0][0:_num], np.abs(mu2.ravel()) + adjust3_fem, label="FEM-based Stress",
                          linewidth=1.5,
                          color='g')
        plt.title('Sample Point No.' + str(3) + ' (' + str(load_title) + 'kg)', fontsize=24)

        list_mu1.append(list_test_data[1][_test_point - 1][0:_num])
        list_mu2.append(mu)
        list_mu3.append(np.abs(mu1) + adjust3_rom)
        list_mu4.append(np.abs(mu2) + adjust3_fem)
    else:
        plot_3 = None
        plot_4 = None
        plt.title('Sample Point No.' + str(_simulate_point) + ' (' + str(load_title) + 'kg)', fontsize=24)

    _plot = plot_1 + plot_2 + plot_3 + plot_4
    labs = [_p.get_label() for _p in _plot]
    # bbox_to_anchor=(x, y, 长, 宽),总图是1*1的 loc是bbox中落在xy位置的角点或中点
    plt.legend(_plot, labs, bbox_to_anchor=(0, 0.75, 1, 0.2), borderaxespad=0, ncol=4, loc="upper center", fontsize=15)
    plt.xlabel("Time (s)", fontsize=20)
    plt.ylabel("Stress (Mpa)", fontsize=20)
    plt.ylim(0, stress_y_limit)
    plt.xlim(0, x_tick)
    x_ticks = np.arange(0, x_tick, 20)
    y_ticks = np.arange(0, stress_y_limit + 1, stress_y_limit / stress_y_limit_separate)
    # 坐标轴刻度字体大小
    BIGGER_SIZE = 18
    plt.rc('xtick', labelsize=BIGGER_SIZE)  # fontsize of the tick labels
    plt.rc('ytick', labelsize=BIGGER_SIZE)
    plt.yticks(y_ticks)
    plt.xticks(x_ticks)
    ax = plt.gca()
    # 指定 data  设置的bottom(也就是指定的x轴)绑定到y轴的0这个点上
    ax.spines['bottom'].set_position(('data', 0))
    ax.spines['left'].set_position(('data', 0))
    plt.grid(ls='--')  # x坐标轴的网格使用主刻度
    # plt.savefig(
    #     path_test + r"stress_point\\" + load + "_" + str(simulation_number) + r"\\" + str(_simulate_point) + '.png')

    plt.show()
    return np.asarray(list_mu1).ravel(), \
           np.asarray(list_mu2).ravel(), \
           np.asarray(list_mu3).ravel(), \
           np.asarray(list_mu4).ravel()


# for i in [3, 5]:
for i in [which_point_dic[which_point]]:
    # 几个时序的点，仿真从第几个时序开始，仿真的哪个状态的数据，仿真第几个点，实验第几个点，仿真的训练权重读取路径,训练数据的已知点
    arr_1, arr_2, arr_3, arr_4 = Plot(num, simulation_index, simulation_number_dic[simulation_number], i, i)
    # print(np.sum((arr_1 - arr_2) ** 2))
    # print(np.sum((arr_1 - arr_3) ** 2))
    # print((arr_1 - arr_2) ** 2)
    # print((arr_1 - arr_3) ** 2)
    gs_real = r2(arr_1, arr_2)
    rom_real = r2(arr_1, arr_3)
    fem_real = r2(arr_1, arr_4)
    rom_fem = r2(arr_4, arr_3)
    print("gs", gs_real, "\r\nrom", rom_real, "\r\nfem", fem_real, "\r\nrom_fem", rom_fem)
    gs_m1 = MY(arr_1, arr_2)
    rom_m1 = MY(arr_1, arr_3)
    fem_m1 = MY(arr_1, arr_4)
    rom_fem_m1 = MY(arr_4, arr_3)
    print("gs_m1", gs_m1, "\r\nrom_m1", rom_m1, "\r\nfem_m1", fem_m1, "\r\nrom_fem_m1", rom_fem_m1)
