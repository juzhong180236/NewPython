import os
import numpy as np
from surf_data_process import SurfaceData
from rbf_2020 import RBF
from GPR import GPR
from PRS import PRS
import txt_file_create as tfc
import print_f as pf
from ele_data import ElementData
from coords_data import CoordinateData
from disp_data import DispalcementData
from stre_data import StressData
from openmdao.surrogate_models.kriging import KrigingSurrogate
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

"""
这个程序的用处是将应力或者位移数据从一个第一维为M个状态，第二维为N个节点的列表
转换为一个第一维为N个节点，第二维为M个状态的列表。
例如，100个状态，力10个，角度10个，总共100个。节点数为336个。
则输入100*336的列表，输出336*100的列表。
"""


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
        pathisExists = os.path.exists(self.path_write)
        if not pathisExists:
            os.makedirs(self.path_write)  # 不存在创建目录
            pf.printf('文件夹[' + self.path_write + ']创建成功,正在写入文件...')
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

    def dataToPostFile_paper_result_pulley(self, v_fd, path_real_data, rbf_type='lin_a'):
        """
        :param v_fd: 输入的训练自变量
        :param path_real_data: 真实数据的路径
        :param rbf_type: 使用的rbf类型
        :return:
        """
        import numpy as np

        def Read_Data(path):
            isExisted = os.path.exists(path)
            if not isExisted:
                pf.printf(path)
                pf.printf('上面列出的路径不存在，请设置正确路径！')
                return
            else:
                pf.printf('目录[' + path + ']存在,正在读取...')
            files = os.listdir(path)  # 获取当前文档下的文件
            files_cut = sorted(files, key=lambda x: int(x[:-4]))
            list_125 = []
            list_250 = []
            list_375 = []
            list_500 = []
            # print(files_cut)
            list_different_force = []
            for file_traversal_times in range(39):
                list_different_angle = []
                for index in range(file_traversal_times, len(files_cut), 39):
                    file_content = open(path + os.path.basename(files_cut[index]), 'rt')
                    first_line = file_content.read()
                    list_different_angle.append(float(first_line.strip()))
                    file_content.close()
                list_different_force.append(list_different_angle)
                # list_selected_train_data_force.append(list_selected_train_data_angle)
            list_selected_train_data_angle = []
            files_train = []
            for file in files_cut:
                which_angle = file[:-4].split('_')[0]
                which_force = file[:-4].split('_')[1]
                force_arr = ["1", "14", "26", "39"]
                angle_arr = ["1", "22", "43", "65"]
                if which_angle in angle_arr and which_force in force_arr:
                    files_train.append(file)
            files = sorted(files_train, key=lambda x: int(x[:-4].split('_')[1]))
            for file in files:
                file_content = open(path + os.path.basename(file), 'rt')
                first_line = file_content.read()
                list_selected_train_data_angle.append(float(first_line.strip()))
                file_content.close()

            # print(len(list_selected_train_data_force))
            return list_different_force, np.asarray(list_selected_train_data_angle).reshape(-1, 4)
            # for file in files_cut:
            #     if int(file[:-4].split('_')[1]) == 1:
            #         file_content = open(path + os.path.basename(file), 'rt')
            #         first_line = file_content.read()
            #         list_125.append(float(first_line.strip()))
            #         file_content.close()
            #     elif int(file[:-4].split('_')[1]) == 2:
            #         file_content = open(path + os.path.basename(file), 'rt')
            #         first_line = file_content.read()
            #         list_250.append(float(first_line.strip()))
            #         file_content.close()
            #     elif int(file[:-4].split('_')[1]) == 3:
            #         file_content = open(path + os.path.basename(file), 'rt')
            #         first_line = file_content.read()
            #         list_375.append(float(first_line.strip()))
            #         file_content.close()
            #     else:
            #         file_content = open(path + os.path.basename(file), 'rt')
            #         first_line = file_content.read()
            #         list_500.append(float(first_line.strip()))
            #         file_content.close()
            # return np.asarray(list_125), np.asarray(list_250), np.asarray(list_375), np.asarray(list_500)

        # list_train_stress_125, list_train_stress_250, \
        # list_train_stress_375, list_train_stress_500 = read_data(self.path_read)
        #
        # list_real_stress_125, list_real_stress_250, \
        # list_real_stress_375, list_real_stress_500 = read_data(path_real_data)
        # list_train_data, list_a = Read_Data(self.path_read)
        # print(list_train_data)
        list_real_data, list_train_data = Read_Data(path_real_data)

        def Which_Surrogate_Model(x_pre, func):
            list_predict_results = []
            for train_data in list_train_data:
                if func.__name__ == 'GPR':
                    s_model = func()
                    s_model.fit(v_fd.reshape(-1, 1), np.asarray(train_data).reshape(-1, 1))
                    list_predict_results.append(s_model.predict(x_pre.reshape(-1, 1)))
                else:
                    s_model = func()
                    s_model.fit(v_fd, train_data)
                    list_predict_results.append(s_model.predict(x_pre))
            return list_predict_results

        # RBF
        # rbfnet_125 = RBF(rbf_type)
        # rbfnet_250 = RBF(rbf_type)
        # rbfnet_375 = RBF(rbf_type)
        # rbfnet_500 = RBF(rbf_type)
        #
        # rbfnet_125.fit(v_fd, list_train_stress_125)
        # rbfnet_250.fit(v_fd, list_train_stress_250)
        # rbfnet_375.fit(v_fd, list_train_stress_375)
        # rbfnet_500.fit(v_fd, list_train_stress_500)
        # PRS
        # rbfnet_125 = PRS(rbf_type, m=2)
        # rbfnet_250 = PRS(rbf_type, m=2)
        # rbfnet_375 = PRS(rbf_type, m=2)
        # rbfnet_500 = PRS(rbf_type, m=3)

        # rbfnet_125.fit(v_fd, list_train_stress_125)
        # rbfnet_250.fit(v_fd, list_train_stress_250)
        # rbfnet_375.fit(v_fd, list_train_stress_375)
        # rbfnet_500.fit(v_fd, list_train_stress_500)
        # GPR
        # rbfnet_125 = GPR(optimize=True)
        # rbfnet_250 = GPR(optimize=True)
        # rbfnet_375 = GPR(optimize=True)
        # rbfnet_500 = GPR(optimize=True)
        #
        # rbfnet_125.fit(v_fd, list_train_stress_125.reshape(-1, 1))
        # rbfnet_250.fit(v_fd, list_train_stress_250.reshape(-1, 1))
        # rbfnet_375.fit(v_fd, list_train_stress_375.reshape(-1, 1))
        # rbfnet_500.fit(v_fd, list_train_stress_500.reshape(-1, 1))

        # stds_125 = str(rbfnet_125.std)
        # stds_250 = str(rbfnet_250.std)
        # stds_375 = str(rbfnet_375.std)
        # stds_500 = str(rbfnet_500.std)

        # GPR
        # x_GPR = np.arange(0, 65, 1).reshape(-1, 1)
        # other
        x_pre = np.arange(0, 65, 1)
        y_pre = Which_Surrogate_Model(x_pre, PRS)
        print(list_real_data[0])
        # print(y_pre[0])
        plt.plot(x_pre, y_pre[0], label="predict")
        plt.plot(x_pre, list_real_data[0], label="train")
        plt.scatter(v_fd, list_train_data[0], label="train", c="red", marker="x")
        # plt.show()

    def dataToPostFile_Kriging(self, fd, which_part):
        """
        :param fd: 输入的训练自变量
        :return:
        """
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
        list_w_stress = []
        list_w_dSum = []
        cycle_index = len(list_stress)
        for i in range(cycle_index):
            # for i in [19137]:
            stress_real = np.asarray(list_stress[i]).reshape(-1, 1)
            # dSum_real = np.asarray(list_disp_sum[i]).reshape(-1, 1)
            kriging_stress = KrigingSurrogate()
            # kriging_dSum = KrigingSurrogate()
            kriging_stress.train(fd, stress_real)
            # kriging_dSum.train(fd, dSum_real)
            _forceArr = np.linspace(50, 500, 20)
            _degreeArr = np.linspace(0, 72, 20)
            """
            画三维图一定不能忘了meshgrid
            """
            _X, _Y = np.meshgrid(_forceArr, _degreeArr)
            # print(_X.shape, _Y.shape)
            # print(_X)
            """
            2018.12.18 训练点的X,Y，可以通过打印X,Y得到X的排布，在根据这个排布去决定Z轴的排布。
            """
            forceArr = [50, 200, 350, 500]
            degreeArr = [0, 24, 48, 72]
            X, Y = np.meshgrid(forceArr, degreeArr)
            """
            2020.12.17 两个combine最终组成的数据因为顺序不一样，导致预测出来的stress顺序不同，
            而最终的三维图像只是简单地进行了一个reshape，很容易因为没有对应上而出错
            """
            # combine = []
            # for _iForce in range(_forceArr.shape[0]):
            #     for _iDegree in range(_degreeArr.shape[0]):
            #         combine.append((_forceArr[_iForce], _degreeArr[_iDegree]))
            # _fd = np.array(combine)
            combine = []
            for _i in range(_X.shape[0]):
                for _j in range(_X.shape[1]):
                    combine.append((_X[_i, _j], _Y[_i, _j]))
            _fd1 = np.array(combine)
            # list_w_stress.append(kriging_stress)
            _y_stress = kriging_stress.predict(_fd1).reshape(_X.shape)
            # print(stress_real)
            # _y_stress = kriging_stress.predict(_fd[0])
            # print(kriging_stress.predict(np.asarray([[500., 0.], [500, 72], [50, 0], [50, 72]])))
            # print(_y_stress)
            # print(_fd[0])
            # _y_d = kriging_dSum.predict(_fd)
            # list_w_dSum.append(w_dSum)
            fig = plt.figure()
            ax = Axes3D(fig)
            # ax = fig.add_subplot(111, projection='3d')
            # rstride:行之间的跨度  cstride:列之间的跨度，只能为正整数，默认是1，
            # 就是和linspace分割的块数一致，数字越大，图形的块数越少
            # rcount:设置间隔个数，默认50个，ccount:列的间隔个数  不能与上面两个参数同时出现
            ax.plot_surface(
                _X,
                _Y,
                _y_stress,
                rstride=1,
                cstride=1,
                cmap=plt.get_cmap('rainbow')  # coolwarm
            )
            """
            2020.12.18 因为应力是按照：力为第一维，角度为第二维，但是X是力的广播，Y是角度的广播。
            所以要对应力的数值进行转置。
            """
            ax.scatter(
                X,
                Y,
                stress_real.reshape(4, 4).T,
                c='k',
            )
            # 绘制从3D曲面到底部的投影,zdir 可选 'z'|'x'|'y'| 分别表示投影到z,x,y平面
            # zdir = 'z', offset = -2 表示投影到z = -2上
            # ax.contour(_degreeArr, _forceArr, _y_stress, zdir='z', offset=-2, cmap=plt.get_cmap('rainbow'))
            # 设置z轴的维度，x,y类似
            # ax.set_zlim(-2, 2)
            plt.savefig(r"C:\Users\asus\Desktop\pics_high\\" + str(i) + '.png')
            """
            2020.12.19 避免画图内存泄露
            """
            plt.close('all')  # 避免内存泄漏
            print("\r" + kriging_stress.__class__.__name__ + "程序当前已完成：" + str(
                round(i / len(list_stress) * 10000) / 100) + '%', end="")
        # plt.show()
        stepAndMin = which_part + '_others'
        ele = which_part + '_ele'
        dSum_w = which_part + '_dSum_w'
        stress_w = which_part + '_stress_w'
        coord = which_part + '_coord'
        #
        # if v_fd.ndim == 1:
        #     x_train = ','.join(map(str, v_fd.tolist()))
        # elif v_fd.ndim == 2:
        #     x_train = ','.join(map(lambda x: ','.join(map(str, x)), v_fd.tolist()))
        # else:
        #     x_train = "null"
        # pathisExists = os.path.exists(self.path_write)
        # if not pathisExists:
        #     os.makedirs(self.path_write)  # 不存在创建目录
        #     pf.printf('文件夹[' + self.path_write + ']创建成功,正在写入文件...')
        # # 步数和最小值，方差，输入值
        # tfc.text_Create(self.path_write, stepAndMin,
        #                 txt_DstepandMin + ',' + txt_SstepandMin + '\n' + stds + '\n' + x_train)
        # # 索引文件
        # tfc.text_Create(self.path_write, ele, txt_ele)
        # # 总位移文件
        # tfc.text_Create(self.path_write, dSum_w, '\n'.join(list_w_dSum) + '\n' + rbf_type)
        # # 应力文件
        # tfc.text_Create(self.path_write, stress_w, '\n'.join(list_w_stress) + '\n' + rbf_type)
        # # # 坐标文件【坐标一般需要变换一下，就不直接输出了】
        # tfc.text_Create(self.path_write, coord, txt_coord)

    def dataSaveToJson_RBF(self, v_fd, rbf_type='lin_a', which_part='truss'):
        """
        和上一版本的区别是，位移数据和坐标数据分开导出
        :param v_fd: 输入的训练自变量
        :param rbf_type: 使用的rbf类型
        :param which_part: 存储的数据是哪个零件的
        :return:
        """
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
        list_w_stress = []
        list_w_dSum = []
        cycle_index = len(list_stress)
        for i in range(cycle_index):
            stress_real = list_stress[i]
            dSum_real = list_dopSum[i]
            rbfnet_stress = RBF(rbf_type)
            rbfnet_dSum = RBF(rbf_type)
            w_stress = rbfnet_stress.fit(v_fd, stress_real)
            w_dSum = rbfnet_dSum.fit(v_fd, dSum_real)
            stds = str(rbfnet_stress.std)
            list_w_stress.append(w_stress)
            list_w_dSum.append(w_dSum)
            print("\r" + rbfnet_stress.__class__.__name__ + "程序当前已完成：" + str(
                round(i / len(list_stress) * 10000) / 100) + '%', end="")
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
        pathisExists = os.path.exists(self.path_write)
        if not pathisExists:
            os.makedirs(self.path_write)  # 不存在创建目录
            pf.printf('文件夹[' + self.path_write + ']创建成功,正在写入文件...')

        dict_rbf_model = {}
        dict_rbf_model["D_step_Min"] = txt_DstepandMin
        dict_rbf_model["S_step_Min"] = txt_SstepandMin
        dict_rbf_model["stds"] = stds
        dict_rbf_model["x_train"] = x_train
        dict_rbf_model["D_step_Min"] = txt_DstepandMin
        dict_rbf_model["S_step_Min"] = txt_SstepandMin
        dict_rbf_model["stds"] = stds
        dict_rbf_model["ele"] = txt_ele
        dict_rbf_model["dSum_w"] = dSum_w
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
