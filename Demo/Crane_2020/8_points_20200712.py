import numpy as np
import matplotlib.pyplot as plt
from ReadExcel import readExcel
import os
import printf as pf
from rbf_2020 import RBF
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import Error_estimates as es
import sklearn.gaussian_process.kernels as kns
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import ConstantKernel

"""
这个程序是展示最后的结果，仿真数据在C#算好，实验数据在excel中，预测数据用paper_result_pulley给出
"""


def Read_TData(path):
    data_y, data_x = readExcel(path, row_index=3, column_index=4, y_column=1)
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


# path = r"C:\Users\asus\Desktop\stress data\\"
# 存储路径：应变仪采集的数据和在采集时实时仿真出来的数据
path_test = r"C:\Users\asus\Desktop\stress 20200704\\"
# 测试数据文件名，实时仿真数据的文件名
load = "23_2"
# 读取实时仿真数据，共9个list，前8个为应力的时序数据，最后1个为角度的时序数据
list_simulation_data = Read_SData(path_test + load + r".txt")
# 读取实验数据，共2个list，第1个为应力数据的时序时间，第2个为8个应力点组成的二维list，里面有8个list，存储每个点的测试应力数据
list_test_data = Read_TData(path_test + load + r".xlsx")
# 因为开启两个采样的时间总会差一两秒，虽然采样频率一样，但是数据总个数会差一些，所以选择小的来对比
# 不过要注意不要偏移了
num = min(len(list_simulation_data[0]), len(list_test_data[1][0]))
# print(num)
# path_train = r"C:\Users\asus\Desktop\Papers\paper_result_truss\equivalent_stress_point_v2_72\w_4.txt"
# 其实在上面的测试中，只需要有时序的角度数据就可以，这样可以用已经建立的模型来插值预测
path_train = r"C:\Users\asus\Desktop\Papers\paper_result_truss\equivalent_stress_point_v2_72_400N\w_4.txt"
# dict_1 = {}
# list_stress = []
# for angle in list_simulation_data[8]:
#     dict_1[angle] = []
#
# list1 = sorted(list(set(list_simulation_data[8])), key=lambda x: int(x))
# for angle, stress in zip(list_simulation_data[8][0:num], list_test_data[1][0][0:num]):
#     dict_1[angle].append(stress)
# print(dict_1)
# for value in sorted(dict_1):
#     list_stress.append(np.average(dict_1[value], axis=-1))
# 创建文件夹
mkdir(path_test + load)
# 读取RBF训练的权重w数据
isExisted = os.path.exists(path_train)
if not isExisted:
    pf.printf(path_train)
    pf.printf('上面列出的路径不存在，请设置正确路径！')
else:
    pf.printf('目录[' + path_train + ']存在,正在读取...')
list_w = []
file_content = open(path_train, 'rt')
# 将训练数据得到的权重w给出
for line in file_content:
    list_w.append(list(map(float, line.strip("\n").split(','))))


def Read_Data_Single(path):
    """
    :param path: 多个static structural数据路径
    :param angle_pieces: 数据按照角度分了多少份
    :param train_pieces: 训练数据有多少份
    :return:
    """
    isExisted = os.path.exists(path)
    if not isExisted:
        pf.printf(path)
        pf.printf('上面列出的路径不存在，请设置正确路径！')
        return
    else:
        pf.printf('目录[' + path + ']存在,正在读取...')
    files = os.listdir(path)  # 获取当前文档下的文件
    abandon_files = ["file0.page", "file1.page"]
    for file in files:
        file_name = os.path.basename(file)
        if file_name in abandon_files:
            os.remove(path + file_name)
    # 按照角度排序
    files = os.listdir(path)
    files_cut = sorted(files, key=lambda x: int(x[:-4]))
    # 真实的所有角度的数据
    list_different_angle = []
    # 训练用的提取出的角度数据
    list_selected_train_data_angle = []
    angle_arr = ["0", "24", "48", "72"]
    # 取出所有的数据，因为前面排序好了，取出来就是先按照角度排序，后按照力排序的数据
    for file in files_cut:
        file_content = open(path + os.path.basename(file), 'rt')
        first_line = file_content.read()
        each_ele = first_line.split()
        list_different_angle.append(np.abs(float(each_ele[-1])))
        file_content.close()
        # 根据文件名判断是不是训练数据
        which_angle = str(int(file[:-4]) - 1)  # 因为apdl导出的文件一直是从1开始
        # 取出训练的数据
        if which_angle in angle_arr:
            list_selected_train_data_angle.append(np.abs(float(each_ele[-1].strip())))
    return np.asarray(list_different_angle), np.asarray(
        list_selected_train_data_angle)


fd_train = np.arange(0, 73)
v_fd = np.array([0, 24, 48, 72])
path_train_data = r"C:\Users\asus\Desktop\Papers\paper_result_truss\equivalent_stress_point_v2_72\\"
# 画出每一个点的实验、仿真、预测的值
# 1 8 3 6
which_point = 1
stress_y_limit = 35

for i in range(which_point - 1, which_point):
    list_real_data, list_train_data = Read_Data_Single(path_train_data + str(i + 1) + r"\\")

    fig = plt.figure(figsize=(10.5, 5), dpi=100)
    # ax1 = fig.add_subplot(111)
    # ax2 = ax1.twinx()
    if i == 7:
        plt.title('Sample Point No.' + str(2), fontsize=24)
    elif i == 5:
        plt.title('Sample Point No.' + str(4), fontsize=24)
    else:
        plt.title('Sample Point No.' + str(i + 1), fontsize=24)
    # plt.title('Luffing angle of the crane boom (30kg)', fontsize=24)
    # 仿真
    # plot_0 = plt.plot(list_test_data[0][0:num], list_simulation_data[i][0:num], label="SPI-DT Stress", linewidth=1.5)
    # 实验
    plot_1 = plt.plot(list_test_data[0][0:num], list_test_data[1][i][0:num], label="Test Stress", linewidth=1.5)
    # RBF
    rbf = RBF(w=np.asarray(list_w[i]))
    rbf.x = fd_train
    x_pre = np.asarray(list_simulation_data[8][0:num])
    list_predict_data_RBF = rbf.predict(x_pre)
    plot_2 = plt.plot(list_test_data[0][0:num], list_predict_data_RBF, label="SPI-DT Stress", linewidth=1.5)
    print(list_predict_data_RBF)
    # GPR
    # kernel = ConstantKernel(1.0, (1e-4, 1e4)) * kns.RBF(5, (1e-2, 1e2))
    # s_model = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=0)
    # s_model.fit(v_fd.reshape(-1, 1), np.asarray(list_train_data).reshape(-1, 1))
    # list_predict_data_GPR, cov = s_model.predict(x_pre.reshape(-1, 1),
    #                                              return_cov=True)
    # uncertainty = 1.96 * np.sqrt(np.diag(cov))
    # ax1.plot(list_test_data[0][0:num], list_predict_data_GPR, label="SPI-DT Data")
    # ax1.fill_between(x_pre.ravel(), list_predict_data_GPR + uncertainty, list_predict_data_GPR - uncertainty, alpha=0.1)
    # 角度
    # plot_3 = plt.plot(list_test_data[0][0:num], list_simulation_data[8][0:num], label="luffing degree",
    #                   linestyle='-.')

    # _plot = plot_1 + plot_2 + plot_3
    _plot = plot_1 + plot_2
    # _plot = plot_1 + plot_0
    # _plot = plot_3
    labs = [_p.get_label() for _p in _plot]
    # 1轴
    # bbox_to_anchor=(x, y, 长, 宽),总图是1*1的 loc是bbox中落在xy位置的角点或中点
    # ax1.legend(_plot, labs, bbox_to_anchor=(0, 0.75, 1, 0.2), borderaxespad=0, ncol=3, loc="upper center", fontsize=24)
    plt.legend(_plot, labs, bbox_to_anchor=(0, 0.75, 1, 0.2), borderaxespad=0, ncol=3, loc="upper right", fontsize=24)
    # ax1.set_xlabel("Time (s)", fontsize=20)
    plt.xlabel("Time (s)", fontsize=20)
    plt.ylabel("Stress (Mpa)", fontsize=20)
    # plt.ylabel("Angle (deg)", fontsize=20)
    plt.ylim(0, stress_y_limit)
    # x_ticks = np.arange(0, max(list_test_data[0][0:num]), max(list_test_data[0][0:num]) // 5)
    x_ticks = np.arange(0, 101, 20)
    y_ticks = np.arange(0, stress_y_limit + 1, stress_y_limit / 7)
    plt.yticks(y_ticks, fontsize=20)
    plt.xticks(x_ticks, fontsize=20)
    # ax1_ymajorLocator = MultipleLocator(stress_y_limit / 6)
    # ax1.yaxis.set_major_locator(ax1_ymajorLocator)
    # ax1_ymajorFormatter = FormatStrFormatter('%d')
    # ax1.yaxis.set_major_formatter(ax1_ymajorFormatter)
    plt.grid()  # x坐标轴的网格使用主刻度
    # ax1.yaxis.grid(True, which='major')
    # 2轴
    # ax2.set_ylabel("Angle (deg)", fontsize=13)
    # ax2.set_ylim(0, 90)
    # ax2_ymajorLocator = MultipleLocator(30)
    # ax2.yaxis.set_major_locator(ax2_ymajorLocator)

    # plt.savefig(path_train[:-7] + load + r"\\" + str(i + 1) + '.png')
    # ax1.grid()
    RR = es.R2(list_test_data[1][i][0:num], list_predict_data_RBF)
    M = es.MY(list_test_data[1][i][0:num], list_predict_data_RBF)
    M11 = es.MY(list_predict_data_RBF, list_test_data[1][i][0:num])
    M1 = es.MY(list_test_data[1][i][0:num], list_simulation_data[i][0:num])
    print(M)
    print(M11)
    # print(M1)
    # print(RR)
    plt.show()
