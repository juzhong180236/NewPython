import os
from surf_data_process import SurfaceData
from rbf_2020 import RBF
from GPR import GPR
import sklearn.gaussian_process.kernels as kns
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import ConstantKernel
from PRS import PRS
import txt_file_create as tfc
import print_f as pf
from ele_data import ElementData
from coords_data import CoordinateData
from disp_data import DispalcementData
from stre_data import StressData
import matplotlib.pyplot as plt
import numpy as np


class Training_Points_Data(object):
    def __init__(self, first_pieces=None, second_pieces=None):
        self.first_pieces = first_pieces
        self.second_pieces = second_pieces
        self.path = None
        self.path_arr = None
        pass

    def Read_Multiple_Data(self, path, input_dimension=3):

        """
        :param input_dimension:
        :param second_pieces:
        :param path: 多个static structural数据路径
        :param first_pieces: 数据按照角度分了多少份
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
        files = os.listdir(path)  # 获取当前文档下的文件
        # 先按照文件名的第二个数字排列

        files_cut_sorted_2 = sorted(files, key=lambda x: int(x[:-4].split('_')[1]))

        # 再按照文件名的第一个数字排列
        files_cut_sorted_1 = sorted(files_cut_sorted_2, key=lambda x: int(x[:-4].split('_')[0]))

        # 一维问题，只看角度的时候就取出第一分数字n个第二个不相同的数据
        if input_dimension == 1:
            second_arr = list(map(str, np.arange(1, self.second_pieces + 1, 1)))
        # 二维问题，就取出角度和力都为4个的训练数据
        elif input_dimension == 2:
            second_arr = ["1", "14", "26", "39"]
        else:
            second_arr = []
        first_arr = np.arange(1, self.first_pieces + 1, 1)  # 如果预测的是力不变，角度变
        # 取出所有的数据用的list，因为前面排序好了，取出来就是先按照第二个数排序，后按照第一个数排序的数据
        list_first_arr = []
        # 外循环根据第一个数
        for first_number in first_arr:
            # 内循环是第二个数
            list_second_arr = []
            # print(files_cut_sorted_1[second_pieces * (first_number - 1):second_pieces * first_number])
            for file in files_cut_sorted_1[self.second_pieces * (first_number - 1):self.second_pieces * first_number]:
                # 根据文件名判断是不是训练数据
                # which_first = file[:-4].split('_')[0]
                # which_second = file[:-4].split('_')[1]
                file_content = open(path + os.path.basename(file), 'rt')
                first_line = file_content.read()
                each_ele = first_line.split()
                list_second_arr.append(np.abs(float(each_ele[-1])))
                file_content.close()
            list_first_arr.append(list_second_arr)
            # 取出训练的数据
        return list_first_arr

    def Multiple_Data_Recombine(self, path_arr):
        list_all_points_diverse_condition = np.empty((self.first_pieces, len(path_arr)), dtype=list)
        # print(list_all_points_diverse_condition)
        for i_path in range(len(path_arr)):
            list_single_point_diverse_condition = self.Read_Multiple_Data(path_arr[i_path])
            for i_condition in range(self.first_pieces):
                list_all_points_diverse_condition[i_condition][i_path] = list_single_point_diverse_condition[
                    i_condition]
        # 最外围是不同的受力，内层是不同的点，再内层是每个点在不同角度的值
        return list_all_points_diverse_condition

    def Multiple_Data_Training(self, x_train, func):
        if self.path_arr is None:
            return "self.path_arr is None"
        list_all_points_diverse_condition = self.Multiple_Data_Recombine(self.path_arr)
        list_w_diverse_condition = []
        for _i_condition in range(self.first_pieces):
            list_w_same_condition = []
            for _i_point in range(len(self.path_arr)):
                # RBF训练出来的就是字符串类型的权重w
                _w, _cov = Which_Surrogate_Model_Single(x_train,
                                                        list_all_points_diverse_condition[_i_condition][_i_point], func)
                # print(list_all_points_diverse_condition[_i_condition][_i_point])

                list_w_same_condition.append(_w)
            list_w_diverse_condition.append(list_w_same_condition)
        return list_w_diverse_condition

    def Write_W(self, save_path, x_train, func):
        list_w = self.Multiple_Data_Training(x_train, func)
        # print(list_w[0][2])
        for i_condition_w in range(len(list_w)):
            w_txt = '\n'.join(list_w[i_condition_w])
            tfc.text_Create(save_path, str(i_condition_w), w_txt)


def Which_Surrogate_Model_Single(_x_train, _y_train, func):
    _cov = 0
    if func.__name__ == 'GPR':
        s_model = func()
        _w = s_model.fit(_x_train.reshape(-1, 1), np.asarray(_y_train).reshape(-1, 1))
        # list_predict_results = s_model.predict(_x_pre.reshape(-1, 1))
    elif func.__name__ == 'GaussianProcessRegressor':
        kernel = ConstantKernel(1.0, (1e-4, 1e4)) * kns.RBF(5, (1e-2, 1e2))
        s_model = func(kernel=kernel, n_restarts_optimizer=20)
        _w = s_model.fit(_x_train.reshape(-1, 1), np.asarray(_y_train).reshape(-1, 1))
        # list_predict_results, _cov = s_model.predict(_x_pre.reshape(-1, 1), return_cov=True)
    else:
        s_model = func()
        _w = s_model.fit(_x_train, _y_train)
        # list_predict_results = s_model.predict(_x_pre)
    return _w, _cov


def Which_Surrogate_Model_Mutiple(x_train, x_pre, func, list_train):
    list_predict_results = []
    for train_data in list_train:
        if func.__name__ == 'GPR':
            s_model = func()
            _w = s_model.fit(x_train.reshape(-1, 1), np.asarray(train_data).reshape(-1, 1))
            list_predict_results.append(s_model.predict(x_pre.reshape(-1, 1)))
        elif func.__name__ == 'GaussianProcessRegressor':
            kernel = ConstantKernel(1.0, (1e-4, 1e4)) * kns.RBF(5, (1e-2, 1e2))
            s_model = func(kernel=kernel, n_restarts_optimizer=0)
            _w = s_model.fit(x_train.reshape(-1, 1), np.asarray(train_data).reshape(-1, 1))
            list_predict_results.append(s_model.predict(x_pre.reshape(-1, 1), return_cov=True))
        else:
            s_model = func()
            _w = s_model.fit(x_train, train_data)
            list_predict_results.append(s_model.predict(x_pre))
    return list_predict_results
