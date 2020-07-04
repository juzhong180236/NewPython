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


def _getData(string, fileType):
    # 将多个文件（5个）合并过的变形、应力、坐标值数据等字符串以换行符分解为list
    list_separateByNewline = string.split('\n')
    print('第一个进来的数据' + str(len(list_separateByNewline[0].split(','))))
    # 将上述list的每一个str元素以逗号分解为list,用作计数
    # list_EachPart_Str2List = [listEle.split(',') for listEle in list_separateByNewline]
    list_EachPart_Str2List = list_separateByNewline[0].split(',')
    # 将所有数据放在一个list中
    list_allFile = ','.join(list_separateByNewline).split(',')
    # 获取
    if fileType == 'coord':
        list_x = []
        list_y = []
        list_z = []
        for j in range(0, len(list_EachPart_Str2List), 3):
            list_x_temp = []
            list_y_temp = []
            list_z_temp = []
            for h in range(j, len(list_allFile), len(list_EachPart_Str2List)):
                list_x_temp.append(float(list_allFile[h]))
                list_y_temp.append(float(list_allFile[h + 1]))
                list_z_temp.append(float(list_allFile[h + 2]))
            list_x.append(list_x_temp)
            list_y.append(list_y_temp)
            list_z.append(list_z_temp)
        return list_x, list_y, list_z
    elif fileType == 'stressOrdSum':
        list_stress = []
        for j in range(0, len(list_EachPart_Str2List)):
            list_stress_temp = []
            for h in range(j, len(list_allFile), len(list_EachPart_Str2List)):
                list_stress_temp.append(float(list_allFile[h]))
            list_stress.append(list_stress_temp)
        return list_stress, len(list_separateByNewline[0].split(','))


class DataToFile(object):
    def __init__(self, path_read=None, path_write=None, geometry_type=None):
        self.path_read = path_read
        self.path_write = path_write
        self.geometry_type = geometry_type

    def dataToMidFile(self, path_write=None):
        if not path_write:
            path_write = self.path_write + '/mid/'
            pathisExists = os.path.exists(path_write)
            if not pathisExists:
                os.makedirs(path_write)  # 不存在创建目录
                pf.printf('文件夹[' + path_write + ']创建成功,正在写入文件...')
        surfaced = SurfaceData(self.path_read, self.geometry_type)
        txt_ele = surfaced.get_Ele_Data()
        txt_coord_x = surfaced.get_Coord_Data('x')
        txt_dopCoord, txt_dopSum, txt_DstepandMin = surfaced.get_DopCoord_DopSum_DStepandMin()
        txt_stress, txt_SstepandMin = surfaced.get_Stress_SStepandMin()

        ele = 'ele'
        coord_x = 'coord_x'
        dopCoord = 'dopCoord'
        stress = 'stress'
        dopSum = 'dopSum'
        stepAndMin = 'step_min'

        tfc.text_Create(path_write, ele, txt_ele)
        tfc.text_Create(path_write, coord_x, txt_coord_x)
        tfc.text_Create(path_write, dopCoord, txt_dopCoord)
        tfc.text_Create(path_write, stress, txt_stress)
        tfc.text_Create(path_write, dopSum, txt_dopSum)
        tfc.text_Create(path_write, stepAndMin, txt_DstepandMin + ',' + txt_SstepandMin)

    def dataToPostFile_v1(self, v_fd, rbf_type='lin_a', which_axis_fixed='x'):
        """
        :param v_fd:
        :param rbf_type:
        :param which_axis_fixed:
        :return:
        """
        import numpy as np
        surfaced = SurfaceData(self.path_read, self.geometry_type)
        txt_ele = surfaced.get_Ele_Data()
        txt_fixed_axis = surfaced.get_Coord_Data(which_axis_fixed)
        txt_dopCoord, txt_dopSum, txt_DstepandMin = surfaced.get_DopCoord_DopSum_DStepandMin()
        txt_stress, txt_SstepandMin = surfaced.get_Stress_SStepandMin()
        # coordsFile = open(self.path_read + 'pure_coord.txt', "rt")
        coordsFile = open(self.path_read + 'dop_coord.txt', "rt")
        # coordsFile = open(self.path_read + 'mesh_shell_coord.txt', "rt")
        str_coords = coordsFile.read()
        coordsFile.close()

        stds = ''
        list_x, list_y, list_z = _getData(str_coords, 'coord')
        list_stress = _getData(txt_stress, 'stressOrdSum')
        list_dopSum = _getData(txt_dopSum, 'stressOrdSum')
        list_w_1 = []
        list_w_2 = []
        list_w_stress = []
        list_w_dSum = []
        # list_y_name = []
        cycle_index = len(list_x)
        for i in range(cycle_index):
            if which_axis_fixed == 'x':
                real_1 = list_y[i]
                real_2 = list_z[i]
            elif which_axis_fixed == 'y':
                real_1 = list_x[i]
                real_2 = list_z[i]
            else:
                real_1 = list_x[i]
                real_2 = list_y[i]
            stress_real = list_stress[i]
            dSum_real = list_dopSum[i]
            rbfnet_1 = RBF(rbf_type)
            rbfnet_2 = RBF(rbf_type)
            rbfnet_stress = RBF(rbf_type)
            rbfnet_dSum = RBF(rbf_type)
            w_1 = rbfnet_1.fit(v_fd, real_1)
            w_2 = rbfnet_2.fit(v_fd, real_2)
            w_stress = rbfnet_stress.fit(v_fd, stress_real)
            w_dSum = rbfnet_dSum.fit(v_fd, dSum_real)
            # y = str(rbfnet_y.predict(np.array([[0, 200]])).tolist())
            # list_y_name.append(y)
            stds = str(rbfnet_1.std)
            list_w_1.append(w_1)
            list_w_2.append(w_2)
            list_w_stress.append(w_stress)
            list_w_dSum.append(w_dSum)
            print("\r" + rbfnet_1.__class__.__name__ + "程序当前已完成：" + str(round(i / len(list_y) * 10000) / 100) + '%',
                  end="")

        ele = 'ele'
        coord_fixed_axis = 'coord_fixed_axis'
        stepAndMin = 'step_min'
        w_1 = 'w_1'
        w_2 = 'w_2'
        dSum_w = 'dSum_w'
        stress_w = 'stress_w'
        # y_name = 'y'

        tfc.text_Create(self.path_write, ele, txt_ele)
        tfc.text_Create(self.path_write, coord_fixed_axis, txt_fixed_axis)
        tfc.text_Create(self.path_write, stepAndMin, txt_DstepandMin + ',' + txt_SstepandMin)

        tfc.text_Create(self.path_write, w_1,
                        '\n'.join(list_w_1) + '\n' + which_axis_fixed + '\n' + stds + '\n' + ','.join(
                            map(lambda x: ','.join(map(str, x)), v_fd.tolist())) + '\n' + rbf_type)
        tfc.text_Create(self.path_write, w_2, '\n'.join(list_w_2) + '\n' + rbf_type)
        tfc.text_Create(self.path_write, dSum_w, '\n'.join(list_w_dSum) + '\n' + rbf_type)
        tfc.text_Create(self.path_write, stress_w, '\n'.join(list_w_stress) + '\n' + rbf_type)
        # tfc.text_Create(self.path_write, y_name, '\n'.join(list_y_name) + '\n' + rbf_type)

    def dataToPostFile_v2(self, v_fd, rbf_type='lin_a', which_part='truss'):
        """
        和上一版本的区别是，位移数据和坐标数据分开导出
        :param v_fd: 输入的训练自变量
        :param rbf_type: 使用的rbf类型
        :param which_part: 存储的数据是哪个零件的
        :return:
        """
        import numpy as np
        surfaced = SurfaceData(self.path_read, self.geometry_type)
        """以下为节点数据"""
        # 索引
        txt_ele = surfaced.get_Ele_Data()
        surfaced.get_Coord_Data()
        # 位移
        txt_displacement, txt_dopSum, txt_DstepandMin = surfaced.get_Displacement_DopSum_Dcolor()
        # 应力
        txt_stress, txt_SstepandMin = surfaced.get_Stress_SStepandMin()

        stds = ''
        list_stress = _getData(txt_stress, 'stressOrdSum')
        list_dopSum = _getData(txt_dopSum, 'stressOrdSum')
        # list_w_1 = []
        # list_w_2 = []
        list_w_stress = []
        list_w_dSum = []
        # list_y_name = []
        cycle_index = len(list_stress)
        for i in range(cycle_index):
            stress_real = list_stress[i]
            dSum_real = list_dopSum[i]
            # rbfnet_1 = RBF(rbf_type)
            # rbfnet_2 = RBF(rbf_type)
            rbfnet_stress = RBF(rbf_type)
            rbfnet_dSum = RBF(rbf_type)
            # w_1 = rbfnet_1.fit(v_fd, real_1)
            # w_2 = rbfnet_2.fit(v_fd, real_2)
            w_stress = rbfnet_stress.fit(v_fd, stress_real)
            w_dSum = rbfnet_dSum.fit(v_fd, dSum_real)
            stds = str(rbfnet_stress.std)
            # list_w_1.append(w_1)
            # list_w_2.append(w_2)
            list_w_stress.append(w_stress)
            list_w_dSum.append(w_dSum)
            print("\r" + rbfnet_stress.__class__.__name__ + "程序当前已完成：" + str(
                round(i / len(list_stress) * 10000) / 100) + '%',
                  end="")

        w_1 = 'w_1'
        w_2 = 'w_2'

        stepAndMin = which_part + '_others'
        ele = which_part + 'ele'
        dSum_w = which_part + '_dSum_w'
        stress_w = which_part + '_stress_w'

        # 步数和最小值，方差，输入值
        tfc.text_Create(self.path_write, stepAndMin,
                        txt_DstepandMin + ',' + txt_SstepandMin + '\n' + stds + '\n' + ','.join(
                            map(lambda x: ','.join(map(str, x)), v_fd.tolist())))
        # 索引文件
        tfc.text_Create(self.path_write, ele, txt_ele)
        # 总位移文件
        tfc.text_Create(self.path_write, dSum_w, '\n'.join(list_w_dSum) + '\n' + rbf_type)
        # 应力文件
        tfc.text_Create(self.path_write, stress_w, '\n'.join(list_w_stress) + '\n' + rbf_type)

    def dataToPostFile_v2_Bysorted(self, v_fd, rbf_type='lin_a', which_part='truss'):
        """
        和上一版本的区别是，位移数据和坐标数据分开导出
        :param v_fd: 输入的训练自变量
        :param rbf_type: 使用的rbf类型
        :param which_part: 存储的数据是哪个零件的
        :return:
        """
        import numpy as np
        surfaced = SurfaceData(self.path_read, self.geometry_type)
        """以下为节点数据"""
        # 索引
        txt_ele = surfaced.get_Ele_Data()
        # print(len(set(sorted(map(int, txt_ele.split(',')), key=lambda x: x))))
        txt_coord = surfaced.get_Coord_Data()
        # 位移
        txt_displacement, txt_dopSum, txt_DstepandMin = surfaced.get_Displacement_DopSum_Dcolor_Bysorted()
        # 应力
        txt_stress, txt_SstepandMin = surfaced.get_Stress_SStepandMin_Bysorted()
        # print(len(txt_coord.split('\n')[0].split(',')))
        stds = ''
        list_stress, len_data_stress = _getData(txt_stress, 'stressOrdSum')
        list_dopSum, len_data_dopSum = _getData(txt_dopSum, 'stressOrdSum')
        if len_data_stress != len_data_dopSum:
            print('displacement数据与stress数据数目不同!\n'
                  'displacemen数据个数：' + str(len_data_dopSum)
                  + '      stress数据个数:' + str(len_data_stress))
            return
        # list_w_1 = []
        # list_w_2 = []
        list_w_stress = []
        list_w_dSum = []
        # list_y_name = []
        cycle_index = len(list_stress)
        for i in range(cycle_index):
            # for i in range(1):
            stress_real = list_stress[i]
            dSum_real = list_dopSum[i]
            # rbfnet_1 = RBF(rbf_type)
            # rbfnet_2 = RBF(rbf_type)
            rbfnet_stress = RBF(rbf_type)
            rbfnet_dSum = RBF(rbf_type)
            # w_1 = rbfnet_1.fit(v_fd, real_1)
            # w_2 = rbfnet_2.fit(v_fd, real_2)
            w_stress = rbfnet_stress.fit(v_fd, stress_real)
            w_dSum = rbfnet_dSum.fit(v_fd, dSum_real)
            stds = str(rbfnet_stress.std)
            # list_w_1.append(w_1)
            # list_w_2.append(w_2)
            list_w_stress.append(w_stress)
            list_w_dSum.append(w_dSum)
            print("\r" + rbfnet_stress.__class__.__name__ + "程序当前已完成：" + str(
                round(i / len(list_stress) * 10000) / 100) + '%', end="")
            # x = np.array([0, 90, 180, 270, 360])
            # plt.plot(x, rbfnet_stress.predict(np.array([[0, 125],
            #                                             [90, 125],
            #                                             [180, 125],
            #                                             [270, 125],
            #                                             [360, 125],
            #                                             ])))
            # plt.show()

        w_1 = 'w_1'
        w_2 = 'w_2'

        stepAndMin = which_part + '_others'
        ele = which_part + '_ele'
        dSum_w = which_part + '_dSum_w'
        stress_w = which_part + '_stress_w'
        coord = which_part + '_coord'

        if v_fd.ndim == 1:
            x_train = ','.join(map(str, v_fd.tolist()))
        elif v_fd.ndim == 2:
            x_train = ','.join(map(lambda x: ','.join(map(str, x)), v_fd.tolist()))
        else:
            x_train = "null"
        # 步数和最小值，方差，输入值
        tfc.text_Create(self.path_write, stepAndMin,
                        txt_DstepandMin + ',' + txt_SstepandMin + '\n' + stds + '\n' + x_train)
        # 索引文件
        tfc.text_Create(self.path_write, ele, txt_ele)
        # 总位移文件
        tfc.text_Create(self.path_write, dSum_w, '\n'.join(list_w_dSum) + '\n' + rbf_type)
        # 应力文件
        tfc.text_Create(self.path_write, stress_w, '\n'.join(list_w_stress) + '\n' + rbf_type)
        # # 坐标文件【坐标一般需要变换一下，就不直接输出了】
        tfc.text_Create(self.path_write, coord, txt_coord)

    def dataToPostFile_paper_result_pulley(self, v_fd, data_title="", input_dimension=1, which_point=None,
                                           data_test=None):
        """
        :param data_test: 测试点数据
        :param which_point: 8个采样点中的哪一个
        :param v_fd: 输入的训练自变量
        :param data_title: 数据的标题
        :param input_dimension: 问题的维度，目前先是一维的
        :return:
        """
        import numpy as np

        def Read_Data_Mutiple(path, angle_pieces, train_pieces):
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
            # 按照角度排序
            files_cut = sorted(files, key=lambda x: int(x[:-4].split('_')[0]))
            # 再按照力排序
            files_cut_sorted = sorted(files_cut, key=lambda x: int(x[:-4].split('_')[1]))
            # 真实的所有角度的数据
            list_different_angle = []
            # 训练用的提取出的角度数据
            list_selected_train_data_angle = []
            # 一维问题，只看角度的时候就取出每个角度40个不同力的训练数据
            if input_dimension == 1:
                force_arr = list(map(str, np.arange(1, 40, 1)))
            # 二维问题，就取出角度和力都为4个的训练数据
            elif input_dimension == 2:
                force_arr = ["1", "14", "26", "39"]
            else:
                force_arr = []
            angle_arr = ["1", "22", "43", "65"]  # 如果预测的是力不变，角度变
            # 取出所有的数据，因为前面排序好了，取出来就是先按照角度排序，后按照力排序的数据
            for file in files_cut_sorted:
                file_content = open(path + os.path.basename(file), 'rt')
                first_line = file_content.read()
                list_different_angle.append(float(first_line.strip()))
                # list_different_angle.append(file)
                file_content.close()
                # 根据文件名判断是不是训练数据
                which_angle = file[:-4].split('_')[0]
                which_force = file[:-4].split('_')[1]
                # 取出训练的数据
                if which_angle in angle_arr and which_force in force_arr:
                    list_selected_train_data_angle.append(float(first_line.strip()))
            return np.asarray(list_different_angle).reshape(-1, angle_pieces), np.asarray(
                list_selected_train_data_angle).reshape(
                -1, train_pieces)

        # list_real_data, list_train_data = Read_Data_Mutiple(self.path_read, 65, 4)
        def Which_Surrogate_Model_Mutiple(x_pre, func, list_train):
            list_predict_results = []
            for train_data in list_train:
                if func.__name__ == 'GPR':
                    s_model = func()
                    s_model.fit(v_fd.reshape(-1, 1), np.asarray(train_data).reshape(-1, 1))
                    list_predict_results.append(s_model.predict(x_pre.reshape(-1, 1)))
                elif func.__name__ == 'GaussianProcessRegressor':
                    kernel = ConstantKernel(1.0, (1e-4, 1e4)) * kns.RBF(5, (1e-2, 1e2))
                    s_model = func(kernel=kernel, n_restarts_optimizer=0)
                    s_model.fit(v_fd.reshape(-1, 1), np.asarray(train_data).reshape(-1, 1))
                    list_predict_results.append(s_model.predict(x_pre.reshape(-1, 1)))
                else:
                    s_model = func()
                    s_model.fit(v_fd, train_data)
                    list_predict_results.append(s_model.predict(x_pre))
            return list_predict_results

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
            if input_dimension == 1:
                angle_arr = ["1", "42", "83", "126"]
            else:
                angle_arr = []
            # 取出所有的数据，因为前面排序好了，取出来就是先按照角度排序，后按照力排序的数据
            for file in files_cut:
                file_content = open(path + os.path.basename(file), 'rt')
                first_line = file_content.read()
                each_ele = first_line.split()
                list_different_angle.append(np.abs(float(each_ele[-1])))
                file_content.close()
                # 根据文件名判断是不是训练数据
                which_angle = file[:-4]
                # 取出训练的数据
                if which_angle in angle_arr:
                    list_selected_train_data_angle.append(np.abs(float(each_ele[-1].strip())))
            return np.asarray(list_different_angle), np.asarray(
                list_selected_train_data_angle)

        list_real_data, list_train_data = Read_Data_Single(self.path_read)
        print(list_train_data)
        # print(list_train_data)

        def Which_Surrogate_Model_Single(_x_pre, func, train_data):
            _cov = 0
            if func.__name__ == 'GPR':
                s_model = func()
                _w = s_model.fit(v_fd.reshape(-1, 1), np.asarray(train_data).reshape(-1, 1))
                list_predict_results = s_model.predict(_x_pre.reshape(-1, 1))
            elif func.__name__ == 'GaussianProcessRegressor':
                kernel = ConstantKernel(1.0, (1e-4, 1e4)) * kns.RBF(5, (1e-2, 1e2))
                s_model = func(kernel=kernel, n_restarts_optimizer=20)
                _w = s_model.fit(v_fd.reshape(-1, 1), np.asarray(train_data).reshape(-1, 1))
                list_predict_results, _cov = s_model.predict(_x_pre.reshape(-1, 1), return_cov=True)
            else:
                s_model = func()
                _w = s_model.fit(v_fd, train_data)
                list_predict_results = s_model.predict(_x_pre)

            return list_predict_results, _w, _cov

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

        path = r"C:\Users\asus\Desktop\stress data\\"
        load = "25"
        list_simulation_data = Read_SData(path + load + r".txt")
        x_pre2 = np.asarray(list_simulation_data[8])
        x_pre = np.arange(0, 73, 1)
        x_pre1 = np.arange(3.5, 66.5, 0.5)
        # y_pre = Which_Surrogate_Model_Mutiple(x_pre, GaussianProcessRegressor,list_train_data)
        y_pre, w, cov = Which_Surrogate_Model_Single(x_pre, RBF, list_real_data)

        # uncertainty = 1.96 * np.sqrt(np.diag(cov))
        # plt.fill_between(x_pre2.ravel(), y_pre.ravel() + uncertainty, y_pre.ravel() - uncertainty, alpha=0.1)
        # #1f77b4 蓝色 #1fb4ab 青色 #ff7f0e 褐色
        dic_color = {'蓝色': '#1f77b4', '青色': '#1fb4ab', '褐色': '#ff7f0e', '紫色': '#501fb4', '深蓝色': '#231fb4'}
        # plt.plot(x_pre1, list_real_data, c=dic_color['蓝色'],
        #          label="ANSYS data", linewidth=2)
        plt.plot(x_pre, y_pre, label="GPR predicted data",
                 c=dic_color['褐色'], linewidth=1)
        # plt.plot(data_test[2], data_test[3][which_point - 1],
        #          c=dic_color['青色'],
        #          label="experimental continuous sampling data",
        #          linewidth=2)
        # plt.plot(data_test[0], data_test[1][which_point - 1],
        #          c=dic_color['褐色'],
        #          label="experimental single sampling data",
        #          linewidth=2)
        # plt.scatter(v_fd, list_train_data, label="GPR training data", c=dic_color['深蓝色'], marker="o")
        plt.title(data_title)
        plt.ylabel("Stress(Mpa)")
        plt.xlabel("Luffing angle(°)")
        plt.legend()
        plt.show()
        # 应力文件
        return w
