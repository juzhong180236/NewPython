import numpy as np
from Demo.Crane_boom_2021.read_data import Read_Data
from openmdao.surrogate_models.kriging import KrigingSurrogate
from openmdao.surrogate_models.multifi_cokriging import MultiFiCoKriging
from smt.applications.mfk import MFK
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from collections import OrderedDict
import pandas as pd
from Demo.Ansys_Data_Utils_2021.Surrogate_Models.RBF_Surrogate import RBF
from Demo.Ansys_Data_Utils_2021.Surrogate_Models.MF_RBF import MF_RBF
import json

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

path_stress_arr = \
    {
        "low": r"pre_low_fidelity_truss_point\stress_point_more_nodes\\",
        "high": r"pre_high_fidelity_truss_point\stress_point_less_samples\\",
        "verification": r"pre_verification_truss_point\stress_eighteen_nodes\\",
    }
rd_stress = Read_Data()
""" 2020.12.21
读入高低保真的18个节点应力数据
"""
list_stress_low = rd_stress.read_stress(path_prefix + path_stress_arr["low"], mode='v')
list_stress_high = rd_stress.read_stress(path_prefix + path_stress_arr["high"], mode='v')
list_stress_verification = rd_stress.read_stress(path_prefix + path_stress_arr["verification"], mode='v')

path_deformation_arr = \
    {
        "low": r"pre_low_fidelity_truss_point\deformation_point_more_nodes\\",
        "high": r"pre_high_fidelity_truss_point\deformation_point_less_samples\\",
        "verification": r"pre_verification_truss_point\deformation_eighteen_nodes\\",
    }
rd_deformation = Read_Data()
""" 2020.12.21
读入高低保真的18个节点应力数据
"""
list_deformation_low = rd_deformation.read_stress(path_prefix + path_deformation_arr["low"], mode='v')
list_deformation_high = rd_deformation.read_stress(path_prefix + path_deformation_arr["high"], mode='v')
list_deformation_verification = rd_deformation.read_stress(path_prefix + path_deformation_arr["verification"], mode='v')
""" 2020.12.21
每个点的应力放入一个数组，二维数组 
低保真样本18*10*10=18*100
高保真样本18*6
验证18*37*19=18*703
"""
array_real_deformation_low = np.asarray(list_deformation_low).T
array_real_deformation_high = np.asarray(list_deformation_high).T
array_real_deformation_verification = np.asarray(list_deformation_verification).T

array_real_stress_low = np.asarray(list_stress_low).T
array_real_stress_high = np.asarray(list_stress_high).T
array_real_stress_verification = np.asarray(list_stress_verification).T


def create_rbf(_independent_variables, _dependent_variables,
               deformation_or_stress, high_or_low):
    rbf_list = []
    list_w_stress = []
    stds = None
    rbf_type = 'mq'
    _i_point = 0
    for _dependent_var in _dependent_variables:
        rbf = RBF()
        rbf.fit(_independent_variables, _dependent_var.reshape(-1, 1))
        rbf_list.append(rbf)
        list_w_stress.append(rbf.w.tolist())
        if _i_point == 0:
            stds = rbf.std
        _i_point += 1

    dict_rbf_model = {
        "stds_" + high_or_low: stds,
        "x_train_" + high_or_low: _independent_variables.flatten().tolist(),
        "w_" + deformation_or_stress + "_" + high_or_low: list_w_stress,
        "rbf_type_" + deformation_or_stress + "_" + high_or_low: rbf_type,
    }

    return dict_rbf_model


def create_mf_rbf(_independent_variables_low, _independent_variables_high,
                  _dependent_variables_low, _dependent_variables_high,
                  deformation_or_stress):
    mf_rbf_list = []

    low_model_w_list = []
    stds = None
    rbf_type = 'mq'
    x_high = None
    bf_sigma = None
    omega_list = []

    for _i_point in range(len(_dependent_variables_low)):
        mf_rbf = MF_RBF()
        mf_rbf.fit(_independent_variables_low,
                   _dependent_variables_low[_i_point].reshape(-1, 1),
                   _independent_variables_high,
                   _dependent_variables_high[_i_point].reshape(-1, 1))
        mf_rbf_list.append(mf_rbf)

        low_model_w_list.append(mf_rbf.low_model.w.tolist())
        if _i_point == 0:
            stds = mf_rbf.low_model.std
            x_high = mf_rbf.x_high.tolist()
            bf_sigma = mf_rbf.bf_sigma.tolist()
        omega_list.append(mf_rbf.omega.tolist())

    dict_mf_rbf_model = {
        "low_model_w_" + deformation_or_stress: low_model_w_list,
        "stds": stds,
        "x_train": train_low.flatten().tolist(),
        "rbf_type_" + deformation_or_stress: rbf_type,

        "x_high": x_high,
        "bf_sigma": bf_sigma,
        "omega_" + deformation_or_stress: omega_list,
    }
    return dict_mf_rbf_model


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
force_arr_verification = np.arange(5, 52.5, 2.5, dtype=float)
verification_independent_variables, verification_X, verification_Y = create_test_independent_variables(
    force_arr_verification, degree_arr_verification)

train_low = create_train_independent_variables(force_arr_low, degree_arr_low)
# train_high = create_train_independent_variables(force_arr_high, degree_arr_high)
""" 训练得到kriging模型 """
rbf_low_model = create_rbf(train_low, array_real_deformation_low, "deformation", "low")
rbf_high_model = create_rbf(train_high, array_real_deformation_high, "deformation", "high")

multirbf_deformation_model = create_mf_rbf(train_low, train_high, array_real_deformation_low,
                                           array_real_deformation_high, "deformation")

rbf_low_stress_model = create_rbf(train_low, array_real_stress_low, "stress", "low")
rbf_high_stress_model = create_rbf(train_high, array_real_stress_high, "stress", "high")

multirbf_stress_model = create_mf_rbf(train_low, train_high, array_real_stress_low,
                                      array_real_stress_high, "stress")

multirbf_deformation_model.update(rbf_low_model)
multirbf_deformation_model.update(rbf_high_model)
multirbf_stress_model.update(rbf_low_stress_model)
multirbf_stress_model.update(rbf_high_stress_model)

# print(dict(multirbf_deformation_model, **multirbf_stress_model).keys())

json_rbf_model = json.dumps(dict(multirbf_deformation_model, **multirbf_stress_model))
with open("C:/Users/asus/Desktop/multi_fidelity_truss_rbf.json", "w") as f:
    json.dump(json_rbf_model, f)
