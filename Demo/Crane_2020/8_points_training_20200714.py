import numpy as np
from Train_point_data import Training_Points_Data
from rbf_2020 import RBF
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import Error_estimates as es
import sklearn.gaussian_process.kernels as kns
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import ConstantKernel

"""
用来对ansys apdl输出的点的数据进行训练，训练后的权重保存，用于与实验对比
"""
path_ = r"C:\Users\asus\Desktop\Papers\paper_result_truss\20200713_stress_data\stress_point\\"
path_num_arr = map(str, np.arange(1, 9))
path_arr = []
for _path_num in path_num_arr:
    path_arr.append(path_ + _path_num + r"\\")
# print(path_arr)
tpd = Training_Points_Data(first_pieces=7, second_pieces=73)
x_train = np.arange(0, 73)
tpd.path_arr = path_arr
save_path = r"C:\Users\asus\Desktop\Papers\paper_result_truss\20200713_stress_data\stress_point\w\\"
tpd.Write_W(save_path, x_train, RBF)
# tpd.Multiple_Data_Training(x_train, RBF)
