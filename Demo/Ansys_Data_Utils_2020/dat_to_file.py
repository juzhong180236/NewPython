import os
from surf_data_process import SurfaceData
from rbf_2020 import RBF
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

    def dataToPostFile_paper_result_pulley(self, v_fd, path_real_data, rbf_type='lin_a'):
        """
        :param v_fd: 输入的训练自变量
        :param path_real_data: 真实数据的路径
        :param rbf_type: 使用的rbf类型
        :return:
        """
        import numpy as np

        def read_data(path):
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
            for file in files_cut:
                if int(file[:-4].split('_')[1]) == 1:
                    file_content = open(self.path_read + os.path.basename(file), 'rt')
                    first_line = file_content.read()
                    list_125.append(float(first_line.strip()))
                    file_content.close()
                elif int(file[:-4].split('_')[1]) == 2:
                    file_content = open(self.path_read + os.path.basename(file), 'rt')
                    first_line = file_content.read()
                    list_250.append(float(first_line.strip()))
                    file_content.close()
                elif int(file[:-4].split('_')[1]) == 3:
                    file_content = open(self.path_read + os.path.basename(file), 'rt')
                    first_line = file_content.read()
                    list_375.append(float(first_line.strip()))
                    file_content.close()
                else:
                    file_content = open(self.path_read + os.path.basename(file), 'rt')
                    first_line = file_content.read()
                    list_500.append(float(first_line.strip()))
                    file_content.close()
            return np.asarray(list_125), np.asarray(list_250), np.asarray(list_375), np.asarray(list_500)

        # list_train_stress_125, list_train_stress_250, \
        # list_train_stress_375, list_train_stress_500 = read_data(self.path_read)

        list_real_stress_125, list_real_stress_250, \
        list_real_stress_375, list_real_stress_500 = read_data(path_real_data)

        rbfnet_125 = RBF(rbf_type)
        rbfnet_250 = RBF(rbf_type)
        rbfnet_375 = RBF(rbf_type)
        rbfnet_500 = RBF(rbf_type)

        # rbfnet_125.fit(v_fd, list_train_stress_125)
        # rbfnet_250.fit(v_fd, list_train_stress_250)
        # rbfnet_375.fit(v_fd, list_train_stress_375)
        # rbfnet_500.fit(v_fd, list_train_stress_500)

        stds_125 = str(rbfnet_125.std)
        stds_250 = str(rbfnet_250.std)
        stds_375 = str(rbfnet_375.std)
        stds_500 = str(rbfnet_500.std)

        # print("\r" + rbfnet_125.__class__.__name__ + "程序当前已完成：" + str(
        #     round(i / len(list_w_125) * 10000) / 100) + '%', end="")

        x = np.arange(0, 66, 1)

        # plt.plot(x, rbfnet_125.predict(x))
        # plt.plot(x, list_real_stress_125)
        # plt.show()
