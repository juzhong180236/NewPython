import numpy as np
from Demo.Crane_boom_2021.read_data import Read_Data
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd

from Demo.Ansys_Data_Utils_2021.Surrogate_Models.MFS_RBF import MFS_RBF
from scipy.stats import norm
from matplotlib.patches import ConnectionPatch
from openpyxl import load_workbook
import os
from APP_utils.Algorithm.Surrogate_Model.RBF.RBF_Surrogate import RBF
from Demo.Ansys_Data_Utils_2021.Surrogate_Models.RBF import RBF

from Demo.Crane_boom_2021.second_review.PRS import PRS

load_np_txt_path = r"D:\Alai\paper_Alai\【1】期刊论文\【1】Journal of Mechanical Design\起重机臂架论文\crane_boom\\"
_load_arr = np.loadtxt(load_np_txt_path + r"dynamic_train\load_train_dynamic.txt")
_load_sensor_20 = _load_arr[0:20, :].T
_load_sensor_40 = _load_arr[20:40, :].T
_load_sensor_60 = _load_arr[40:60, :].T
_load_sensor_80 = _load_arr[60:80, :].T
_load_sensor_100 = _load_arr[80:100, :].T
_load_sensor_120 = _load_arr[100:120, :].T
_load_sensor_140 = _load_arr[120:140, :].T
temp_load_sensor_20_140 = [
    _load_sensor_20, _load_sensor_40, _load_sensor_60, _load_sensor_80,
    _load_sensor_100, _load_sensor_120, _load_sensor_140
]
temp_mean = []
temp_std = []
for j in range(len(temp_load_sensor_20_140)):
    for i in range(len(_load_sensor_20)):
        temp_mean.append(temp_load_sensor_20_140[j][i].mean())
        temp_std.append(temp_load_sensor_20_140[j][i].std())
temp_std = np.array(temp_std)[::20]
temp_mean = np.array(temp_mean)[::20]
_load_rbf = RBF(rbf="lin_a")
_load_rbf.fit(temp_mean.reshape(-1, 1), temp_std)
print(_load_rbf.predict(np.array([20])))

_angle_arr = np.loadtxt(load_np_txt_path + r"dynamic_train\angle_train_dynamic.txt")
_angle_sensor_20 = _angle_arr[0:20, :].T
_angle_sensor_40 = _angle_arr[20:40, :].T
_angle_sensor_60 = _angle_arr[40:60, :].T
_angle_sensor_80 = _angle_arr[60:80, :].T
_angle_sensor_100 = _angle_arr[80:100, :].T
_angle_sensor_120 = _angle_arr[100:120, :].T
_angle_sensor_140 = _angle_arr[120:140, :].T
temp_angle_sensor_20_140 = [
    _angle_sensor_20, _angle_sensor_40, _angle_sensor_60, _angle_sensor_80,
    _angle_sensor_100, _angle_sensor_120, _angle_sensor_140
]
temp_mean = []
temp_std = []
for j in range(len(temp_angle_sensor_20_140)):
    for i in range(len(_angle_sensor_20)):
        temp_mean.append(temp_angle_sensor_20_140[j][i].mean())
        temp_std.append(temp_angle_sensor_20_140[j][i].std())
temp_std = np.array(temp_std)[::20]
temp_mean = np.array(temp_mean)[::20]
_angle_rbf = RBF(rbf="lin_a")
_angle_rbf.fit(temp_mean.reshape(-1, 1), temp_std)
print(_angle_rbf.predict(np.array([20])))