import numpy as np
import dat_to_file as dtf
from ele_data import ElementData
from coords_data import CoordinateData
from disp_data import DispalcementData
from stre_data import StressData
from txt_file_create import text_Create
from read_data import Read_Data
from openmdao.surrogate_models.kriging import KrigingSurrogate
from openmdao.surrogate_models.multifi_cokriging import MultiFiCoKriging
from smt.applications.mfk import MFK
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from collections import OrderedDict

""" 顔色 """
# cmaps = OrderedDict()

"""
所谓low_fidelity，其实就是Beam188单元
"""
path_prefix = r"C:\Users\asus\Desktop\Code\DT_Crane_Boom_v1.0\APP_models\\"
path_arr = \
    {
        "low": r"pre_low_fidelity_truss_point\stress_point\\",
        "high": r"pre_high_fidelity_truss_point\stress_point\\",
    }
rd = Read_Data()
""" 2020.12.18 读入高低保真的8个点应力数据"""
list_stress_low = rd.read_stress(path_prefix + path_arr["low"])
list_stress_high = rd.read_stress(path_prefix + path_arr["high"])
""" 2020.12.18 每个点的应力放入一个数组，二维数组 低保真8*100 和 高保真8*16"""
array_real_stress_low = np.asarray(list_stress_low).T
array_real_stress_high = np.asarray(list_stress_high).T


# print(array_real_stress_low[0].reshape((10, 10)))
# print(np.asarray(list_stress_low))


# R^2
def r2(data_real, data_predict):
    RSS = np.sum((data_predict - data_real) ** 2)
    TSS = np.sum((data_real - np.average(data_real)) ** 2)
    return 1 - RSS / TSS


def create_kriging(force_arr, degree_arr, dependent_variables):
    kriging_stress_list = []
    for _dependent_var in dependent_variables:

        kriging_stress = KrigingSurrogate()

        combine = []
        for iForce in range(len(force_arr)):
            for iDegree in range(len(degree_arr)):
                combine.append((force_arr[iForce], degree_arr[iDegree]))
        independent_variables = np.array(combine)
        # print(independent_variables)
        # print(_dependent_var.shape)
        kriging_stress.train(independent_variables, _dependent_var.reshape(-1, 1))

        kriging_stress_list.append(kriging_stress)

    return kriging_stress_list


def create_co_kriging(_force_arr_low, _degree_arr_low, _force_arr_high, _degree_arr_high,
                      dependent_variables_low, dependent_variables_high):
    co_kriging_stress_list = []
    for _i_point in range(len(dependent_variables_low)):

        co_kriging_stress = MultiFiCoKriging(theta0=5, thetaL=1e-5, thetaU=50.)

        combine = []
        for iForce in range(len(_force_arr_low)):
            for iDegree in range(len(_degree_arr_low)):
                combine.append((_force_arr_low[iForce], _degree_arr_low[iDegree]))
        independent_variables_low = np.array(combine)
        combine = []
        for iForce in range(len(_force_arr_high)):
            for iDegree in range(len(_degree_arr_high)):
                combine.append((_force_arr_high[iForce], _degree_arr_high[iDegree]))
        independent_variables_high = np.array(combine)
        # print(dependent_variables_low[_i_point].reshape(-1, 1))
        # print(independent_variables_high)
        co_kriging_stress.fit([independent_variables_low, independent_variables_high],
                              [dependent_variables_low[_i_point].reshape(-1, 1),
                               dependent_variables_high[_i_point].reshape(-1, 1)])
        co_kriging_stress_list.append(co_kriging_stress)
    return co_kriging_stress_list


def create_smt_co_kriging(_force_arr_low, _degree_arr_low, _force_arr_high, _degree_arr_high,
                          dependent_variables_low, dependent_variables_high):
    multi_kriging_stress_list = []
    for _i_point in range(len(dependent_variables_low)):

        combine = []
        for iForce in range(len(_force_arr_low)):
            for iDegree in range(len(_degree_arr_low)):
                combine.append((_force_arr_low[iForce], _degree_arr_low[iDegree]))
        independent_variables_low = np.array(combine)
        combine = []
        for iForce in range(len(_force_arr_high)):
            for iDegree in range(len(_degree_arr_high)):
                combine.append((_force_arr_high[iForce], _degree_arr_high[iDegree]))
        independent_variables_high = np.array(combine)
        multi_kriging_stress = MFK(
            theta0=independent_variables_high.shape[-1] * [1.0],
            print_global=False,
            # optim_var=True,
        )

        multi_kriging_stress.set_training_values(independent_variables_low,
                                                 dependent_variables_low[_i_point].reshape(-1, 1), name=0)

        multi_kriging_stress.set_training_values(independent_variables_high,
                                                 dependent_variables_high[_i_point].reshape(-1, 1))
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


""" 训练集数据：自变量 """
# low
force_arr_low = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500]  # 50 100 150 200 250 300 350 400 450 500
degree_arr_low = [0, 8, 16, 24, 32, 40, 48, 56, 64, 72]  # 0 8 16 24 32 40 48 56 64 72
# high
force_arr_high = [50, 200, 350, 500]
degree_arr_high = [0, 24, 48, 72]

__test_temp_1, train_X_low, train_Y_low = create_test_independent_variables(force_arr_low, degree_arr_low)
__test_temp_2, train_X_high, train_Y_high = create_test_independent_variables(force_arr_high, degree_arr_high)
""" 训练得到kriging模型 """
kriging_low_list = create_kriging(force_arr_low, degree_arr_low, array_real_stress_low)
kriging_high_list = create_kriging(force_arr_high, degree_arr_high, array_real_stress_high)
# cokriging_list = create_co_kriging(force_arr_low, degree_arr_low, force_arr_high, degree_arr_high,
#                                    array_real_stress_low, array_real_stress_high)
multikriging_list = create_smt_co_kriging(force_arr_low, degree_arr_low, force_arr_high, degree_arr_high,
                                          array_real_stress_low, array_real_stress_high)
""" 测试集数据：自变量 """
_forceArr = np.linspace(50, 500, 20)
_degreeArr = np.linspace(0, 72, 20)
test_independent_variables, test_X, test_Y = create_test_independent_variables(_forceArr, _degreeArr)
""" 测试集数据：预测得到的因变量 """
list_test_predict_stress_low = []
list_test_predict_stress_high = []
list_test_predict_stress_co = []
list_test_predict_stress_multi = []
# print(test_independent_variables.reshape((20, 20, 2)))
for i in range(len(kriging_low_list)):
    test_predict_stress_low = kriging_low_list[i].predict(test_independent_variables).reshape(test_X.shape)
    test_predict_stress_high = kriging_high_list[i].predict(test_independent_variables).reshape(test_X.shape)
    # test_predict_stress_co = cokriging_list[i].predict(test_independent_variables)[0].reshape(test_X.shape)
    test_predict_stress_multi = multikriging_list[i].predict_values(test_independent_variables).reshape(test_X.shape)

    list_test_predict_stress_low.append(test_predict_stress_low)
    list_test_predict_stress_high.append(test_predict_stress_high)
    # list_test_predict_stress_co.append(test_predict_stress_co)
    list_test_predict_stress_multi.append(test_predict_stress_multi)
# print(list_test_predict_stress_co)
fig = plt.figure()
ax = Axes3D(fig)


def create_figure(_ax, _test_X, _test_Y, _predict_stress_results, _train_X, _train_Y, _real_stress,
                  color_map='rainbow', point_color='k'):
    _ax.plot_surface(
        _test_X,
        _test_Y,
        _predict_stress_results,
        rstride=1,
        cstride=1,
        cmap=plt.get_cmap(color_map)  # coolwarm
    )
    _ax.scatter(
        _train_X,
        _train_Y,
        _real_stress.reshape(_train_X.shape).T,
        c=point_color,
    )


def create_figure_co(_ax, _test_X, _test_Y, _predict_stress_results, color_map='rainbow'):
    _ax.plot_surface(
        _test_X,
        _test_Y,
        _predict_stress_results,
        rstride=1,
        cstride=1,
        cmap=plt.get_cmap(color_map)  # coolwarm
    )


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
for i_point in [7]:
    """
    2020.12.19 颜色中比较常用的是:viridis, rainbow, coolwarm, inferno, ocean
    """
    create_figure(ax,
                  test_X, test_Y, list_test_predict_stress_high[i_point],
                  train_X_high, train_Y_high, array_real_stress_high[i_point].reshape(train_X_high.shape),
                  'coolwarm', 'r')
    create_figure(ax,
                  test_X, test_Y, list_test_predict_stress_low[i_point],
                  train_X_low, train_Y_low, array_real_stress_low[i_point].reshape(train_X_low.shape))
    # create_figure_co(ax, test_X, test_Y, list_test_predict_stress_co[i_point], 'inferno')
    create_figure_co(ax, test_X, test_Y, list_test_predict_stress_multi[i_point], 'viridis')

    co_high = r2(list_test_predict_stress_multi[i_point], list_test_predict_stress_high[i_point])
    co_low = r2(list_test_predict_stress_multi[i_point], list_test_predict_stress_low[i_point])
    high_low = r2(list_test_predict_stress_high[i_point], list_test_predict_stress_low[i_point])
    low_co = r2(list_test_predict_stress_low[i_point], list_test_predict_stress_multi[i_point])
    high_co = r2(list_test_predict_stress_high[i_point], list_test_predict_stress_multi[i_point])
    low_high = r2(list_test_predict_stress_low[i_point], list_test_predict_stress_high[i_point])
    print(
        'co_high', str(co_high) + '\n',
        'co_low', str(co_low) + '\n',
        'high_low', str(high_low) + '\n',
        'low_co', str(low_co) + '\n',
        'high_co', str(high_co) + '\n',
        'low_high', str(low_high) + '\n',
    )
plt.show()
