import numpy as np
from .read_data import Read_Data
from openmdao.surrogate_models.kriging import KrigingSurrogate
from openmdao.surrogate_models.multifi_cokriging import MultiFiCoKriging
from smt.applications.mfk import MFK
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from collections import OrderedDict
import pandas as pd
import matplotlib.patches as mpatches
import matplotlib as mpl
from Demo.Ansys_Data_Utils_2021.model_save_to_file import ModelSaveToFile
""" 
2020.12.20
20201219的节点还是不够满足，所以在这里取了另外取了10个节点，总共加上原来的节点是18个节点 
"""
""" 顔色 """
# cmaps = OrderedDict()

"""
所谓low_fidelity，其实就是Beam188单元
"""
path_prefix = r"C:\Users\asus\Desktop\Code\DT_Crane_Boom_v1.0\APP_models\\"
path_arr = \
    {
        "low": r"pre_low_fidelity_truss_point\stress_point_more_nodes\\",
        "high": r"pre_high_fidelity_truss_point\stress_point_less_samples\\",
        "verification": r"pre_verification_truss_point\stress_eighteen_nodes\\",
    }
rd = Read_Data()
""" 2020.12.21
读入高低保真的18个节点应力数据
"""
list_stress_low = rd.read_stress(path_prefix + path_arr["low"], mode='v')
list_stress_high = rd.read_stress(path_prefix + path_arr["high"], mode='v')
list_stress_verification = rd.read_stress(path_prefix + path_arr["verification"], mode='v')
""" 2020.12.21
每个点的应力放入一个数组，二维数组 
低保真样本18*10*10=18*100
高保真样本18*6
验证18*37*19=18*703
"""
array_real_stress_low = np.asarray(list_stress_low).T
array_real_stress_high = np.asarray(list_stress_high).T
_array_real_stress_verification = np.asarray(list_stress_verification).T

"""
2020.12.25
将array作为索引，需要是整数或者布尔值
"""
indices_degree = np.delete(np.arange(0, 37), np.arange(4, 36, 4))
indices_force = np.delete(np.arange(0, 19), np.arange(2, 18, 2))
list_real_stress_verification = []
for _d in _array_real_stress_verification:
    d = _d.reshape(19, 37)[indices_force, :]
    d1 = d[:, indices_degree]
    list_real_stress_verification.append(d1)
array_real_stress_verification = np.asarray(list_real_stress_verification)


# print(array_real_stress_verification.shape)


# print(array_real_stress_verification)
# print(array_real_stress_verification.shape)


# R^2
def r2(data_real, data_predict):
    RSS = np.sum((data_predict - data_real) ** 2)
    TSS = np.sum((data_real - np.average(data_real)) ** 2)
    return 1 - RSS / TSS


def create_kriging(_independent_variables, _dependent_variables):
    kriging_stress_list = []
    for _dependent_var in _dependent_variables:
        kriging_stress = KrigingSurrogate()

        kriging_stress.train(_independent_variables, _dependent_var.reshape(-1, 1))

        kriging_stress_list.append(kriging_stress)

    return kriging_stress_list


def create_co_kriging(_independent_variables_low, _independent_variables_high,
                      _dependent_variables_low, _dependent_variables_high):
    co_kriging_stress_list = []

    for _i_point in range(len(_dependent_variables_low)):
        co_kriging_stress = MultiFiCoKriging(theta0=5, thetaL=1e-5, thetaU=50.)

        # print(dependent_variables_low[_i_point].reshape(-1, 1))
        # print(independent_variables_high)
        co_kriging_stress.fit([_independent_variables_low, _independent_variables_high],
                              [_dependent_variables_low[_i_point].reshape(-1, 1),
                               _dependent_variables_high[_i_point].reshape(-1, 1)])
        co_kriging_stress_list.append(co_kriging_stress)
    return co_kriging_stress_list


def create_smt_co_kriging(_independent_variables_low, _independent_variables_high,
                          _dependent_variables_low, _dependent_variables_high):
    multi_kriging_stress_list = []
    for _i_point in range(len(_dependent_variables_low)):
        multi_kriging_stress = MFK(
            theta0=_independent_variables_high.shape[-1] * [1.0],
            print_global=False,
            # optim_var=True,
        )

        multi_kriging_stress.set_training_values(_independent_variables_low,
                                                 _dependent_variables_low[_i_point].reshape(-1, 1), name=0)

        multi_kriging_stress.set_training_values(_independent_variables_high,
                                                 _dependent_variables_high[_i_point].reshape(-1, 1))
        multi_kriging_stress.train()
        multi_kriging_stress_list.append(multi_kriging_stress)
    return multi_kriging_stress_list


def create_test_independent_variables(_force_arr, _degree_arr):
    _X, _Y = np.meshgrid(_force_arr, _degree_arr)
    _combine = []
    for _i in range(_X.shape[0]):
        for _j in range(_X.shape[1]):
            _combine.append((_X[_i, _j], _Y[_i, _j]))
    _test_independent_variables = np.array(_combine)
    return _test_independent_variables, _X, _Y


def create_train_independent_variables(_force_arr, _degree_arr):
    _combine = []
    for _iForce in range(len(_force_arr)):
        for _iDegree in range(len(_degree_arr)):
            _combine.append((_force_arr[_iForce], _degree_arr[_iDegree]))
    _independent_variables = np.array(_combine)
    return _independent_variables


""" 训练集数据：自变量 """
# low_samples
force_arr_low = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]  # 5 10 15 20 25 30 35 40 45 50
degree_arr_low = [0, 8, 16, 24, 32, 40, 48, 56, 64, 72]  # 0 8 16 24 32 40 48 56 64 72
# high_samples
train_high = np.asarray([[5, 0], [5, 72], [20, 24], [35, 48], [50, 0], [50, 72]])
# verification_data
'''2020.12.21
这里一定要注意使用float，不然用整数的话kriging工作会出问题
'''
degree_arr_verification = np.arange(0, 74, 2, dtype=float)
degree_arr_verification = np.delete(degree_arr_verification, np.arange(4, 36, 4))
# print(degree_arr_verification.shape)
force_arr_verification = np.arange(5, 52.5, 2.5, dtype=float)
force_arr_verification = np.delete(force_arr_verification, np.arange(2, 18, 2))
# print(force_arr_verification.shape)

verification_independent_variables, verification_X, verification_Y = create_test_independent_variables(
    force_arr_verification, degree_arr_verification)
train_low = create_train_independent_variables(force_arr_low, degree_arr_low)
# train_high = create_train_independent_variables(force_arr_high, degree_arr_high)
""" 训练得到kriging模型 """
kriging_low_list = create_kriging(train_low, array_real_stress_low)
kriging_high_list = create_kriging(train_high, array_real_stress_high)
# cokriging_list = create_co_kriging(force_arr_low, degree_arr_low, force_arr_high, degree_arr_high,
#                                    array_real_stress_low, array_real_stress_high)
multikriging_list = create_smt_co_kriging(train_low, train_high,
                                          array_real_stress_low, array_real_stress_high)
"""
测试集数据：自变量
"""
# _forceArr = np.linspace(50, 500, 19)
# _degreeArr = np.linspace(0, 72, 37)
# test_independent_variables, test_X, test_Y = create_test_independent_variables(_forceArr, _degreeArr)

""" 测试集数据：预测得到的因变量 """
list_test_predict_stress_low = []
list_test_predict_stress_high = []
list_test_predict_stress_co = []
list_test_predict_stress_multi = []
# print(test_independent_variables.reshape((20, 20, 2)))
for i in range(len(kriging_low_list)):
    test_predict_stress_low = kriging_low_list[i].predict(verification_independent_variables).reshape(
        verification_X.shape)
    test_predict_stress_high = kriging_high_list[i].predict(verification_independent_variables).reshape(
        verification_X.shape)
    # test_predict_stress_co = cokriging_list[i].predict(verification_independent_variables)[0].reshape(verification_X.shape)
    test_predict_stress_multi = multikriging_list[i].predict_values(verification_independent_variables).reshape(
        verification_X.shape)

    list_test_predict_stress_low.append(test_predict_stress_low)
    list_test_predict_stress_high.append(test_predict_stress_high)
    # list_test_predict_stress_co.append(test_predict_stress_co)
    list_test_predict_stress_multi.append(test_predict_stress_multi)


# print(list_test_predict_stress_co)


def create_figure(_ax, _test_X, _test_Y, _predict_stress_results,
                  color_map='rainbow', _alpha=0.6, _count=50):
    _ax.plot_surface(
        _test_X,
        _test_Y,
        _predict_stress_results,
        # rstride=1,
        rcount=_count,
        # cstride=1,
        ccount=_count,
        cmap=plt.get_cmap(color_map),  # coolwarm
        alpha=_alpha,
        antialiased=True,
    )


def save_to_excel():
    pd_results_excel = pd.DataFrame(list_results_excel)
    pd_results_excel.columns = ['verification_high', 'verification_low', 'verification_co', 'improvement']
    pd_results_excel.index = range(1, 19)
    writer = pd.ExcelWriter('r2_results_new.xlsx')  # 创建名称为hhh的excel表格
    pd_results_excel.to_excel(writer, 'page_1',
                              float_format='%.10f')  # float_format 控制精度，将data_df写到hhh表格的第一页中。若多个文件，可以在page_2中写入
    writer.save()  #


'''
2020.12.19
cmaps['Perceptually Uniform Sequential'] = [
            'viridis', 'plasma', 'inferno', 'magma', 'cividis']

cmaps['Sequential'] = [
            'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
            'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
            'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn']
cmaps['Sequential (2)'] = [
            'binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink',
            'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia',
            'hot', 'afmhot', 'gist_heat', 'copper']
cmaps['Diverging'] = [
            'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu',
            'RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic']
cmaps['Cyclic'] = ['twilight', 'twilight_shifted', 'hsv']
cmaps['Qualitative'] = ['Pastel1', 'Pastel2', 'Paired', 'Accent',
                        'Dark2', 'Set1', 'Set2', 'Set3',
                        'tab10', 'tab20', 'tab20b', 'tab20c']
cmaps = [
    'flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern',
    'gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg',
    'gist_rainbow', 'rainbow', 'jet', 'turbo', 'nipy_spectral',
    'gist_ncar']
'''
list_results_excel = []
list_r2_verification_high = []
list_r2_verification_low = []
list_r2_verification_co = []
list_r2_verification_improvement = []


def ax_fun(_ax, _str):
    BIGGER_SIZE = 16
    MIDDLE_SIZE = 12
    _ax.set_xlabel("The mass of lifting load (Kg)", fontsize=BIGGER_SIZE)
    _ax.set_ylabel("The degree of luffing angle (deg)", fontsize=BIGGER_SIZE)
    _ax.set_zlabel('Stress (Mpa)', fontsize=BIGGER_SIZE)

    plt.tick_params(labelsize=MIDDLE_SIZE)  # fontsize of the tick labels
    _ax.view_init(elev=30., azim=-135)  # 调整视角
    # plt.savefig(r"C:\Users\asus\Desktop\pics_train_test_different\\" + _str + ".png", bbox_inches='tight')


__alpha = 1
__count = 100
for i_point in range(1):
    # for i_point in [0]:
    """
    2020.12.19 颜色中比较常用的是:viridis, rainbow, coolwarm, inferno, ocean
    """
    fig = plt.figure(figsize=(10, 8))
    ax = Axes3D(fig)
    create_figure(ax,
                  verification_X,
                  verification_Y,
                  list_test_predict_stress_high[i_point],
                  color_map='ocean',
                  _alpha=__alpha,
                  _count=__count,
                  )
    ax_fun(ax, str(i_point) + "high")

    fig = plt.figure(figsize=(10, 8))
    ax = Axes3D(fig)
    create_figure(ax,
                  verification_X,
                  verification_Y,
                  list_test_predict_stress_low[i_point],
                  color_map='rainbow',
                  _alpha=__alpha,
                  _count=__count,
                  )
    ax_fun(ax, str(i_point) + "low")

    fig = plt.figure(figsize=(10, 8))
    ax = Axes3D(fig)
    # create_figure_co(ax, verification_X, verification_Y, list_test_predict_stress_co[i_point], 'inferno')
    create_figure(ax,
                  verification_X,
                  verification_Y,
                  list_test_predict_stress_multi[i_point],
                  color_map='viridis',
                  _alpha=__alpha,
                  _count=__count,
                  )
    ax_fun(ax, str(i_point) + "co")

    fig = plt.figure(figsize=(10, 8))
    ax = Axes3D(fig)
    create_figure(ax,
                  verification_X,
                  verification_Y,
                  array_real_stress_verification[i_point].reshape(verification_X.T.shape).T,
                  color_map='inferno',
                  _alpha=__alpha,
                  _count=__count,
                  )

    ax_fun(ax, str(i_point) + "real")
    # BIGGER_SIZE = 16
    # MIDDLE_SIZE = 12
    # ax.set_xlabel("The mass of lifting load (Kg)", fontsize=BIGGER_SIZE)
    # ax.set_ylabel("The degree of luffing angle (deg)", fontsize=BIGGER_SIZE)
    # ax.set_zlabel('Stress (Mpa)', fontsize=BIGGER_SIZE)
    #
    # plt.tick_params(labelsize=MIDDLE_SIZE)  # fontsize of the tick labels
    # ax.view_init(elev=30., azim=-135)  # 调整视角
    # # plt.savefig(r"C:\Users\asus\Desktop\pics\\" + str(i_point) + '.png', bbox_inches='tight')
    """
    2020.12.19 避免画图内存泄露
    """
    plt.close('all')  # 避免内存泄漏

    verification_high = r2(array_real_stress_verification[i_point].T,
                           list_test_predict_stress_high[i_point])
    verification_low = r2(array_real_stress_verification[i_point].T,
                          list_test_predict_stress_low[i_point])
    verification_co = r2(array_real_stress_verification[i_point].T,
                         list_test_predict_stress_multi[i_point])

    temp_max = max(verification_high, verification_low)
    improvement = (verification_co - temp_max) / temp_max * 100
    print(improvement)
    list_r2_verification_improvement.append(improvement)

    list_r2_verification_high.append(verification_high)
    list_r2_verification_low.append(verification_low)
    list_r2_verification_co.append(verification_co)
    list_results_excel.append(np.asarray([verification_high, verification_low, verification_co, improvement]))
    # print(
    #     'verification_high', str(verification_high) + '\n',
    #     'verification_low', str(verification_low) + '\n',
    #     'verification_co', str(verification_co) + '\n',
    # )
# fig = plt.figure(figsize=(10, 8))
# x_14 = list(np.arange(1, 19))
# x_15 = [i + 0.2 for i in x_14]
# x_16 = [i + 0.4 for i in x_14]
# plt.bar(np.arange(1, 19), list_r2_verification_high)
# plt.bar(x_15, list_r2_verification_low)
# plt.bar(x_16, list_r2_verification_co)
# Add legend with proxy artists

# fake2Dline = mpl.lines.Line2D([0],[0], linestyle="none", c='b', marker = 'o')
# ax.legend([fake2Dline], ['Lyapunov function on XY plane'], numpoints = 1)
# col1_patch = mpatches.Patch(color='r', label='very blue')
# col2_patch = mpatches.Patch(color='g', label='very red')
# plt.legend(handles=[col1_patch, col2_patch])
# plt.show()
save_to_excel()
