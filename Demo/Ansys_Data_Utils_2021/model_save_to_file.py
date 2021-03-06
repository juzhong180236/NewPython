import os
import numpy as np
from .surface_data_process import SurfaceData
from Demo.Ansys_Data_Utils_2021.Surrogate_Models.RBF import RBF
from Demo.Ansys_Data_Utils_2021.Surrogate_Models.PRS import PRS
import Demo.Ansys_Data_Utils_2021.txt_file_create as tfc
import Demo.Ansys_Data_Utils_2021.print_f as pf
from openmdao.surrogate_models.kriging import KrigingSurrogate
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import json

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


class ModelSaveToFile(object):
    def __init__(self, path_read=None, path_write=None, geometry_type=None):
        self.path_read = path_read
        self.path_write = path_write
        self.geometry_type = geometry_type

    def dataSaveToTXT_RBF(self, v_fd, rbf_type='lin_a', which_part='truss'):
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
        list_ele = surfaced.get_Ele_Data()
        # print(len(set(sorted(map(int, txt_ele.split(',')), key=lambda x: x))))
        list_coords = surfaced.get_Coord_Data()
        # 位移
        txt_displacement, txt_dopSum, d_step, d_min = surfaced.get_Displacement_DopSum_Dcolor_Bysorted()
        # 应力
        txt_stress, s_step, s_min = surfaced.get_Stress_SStepandMin_Bysorted()
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
            list_w_stress.append(','.join(map(str, w_stress)))
            list_w_dSum.append(','.join(map(str, w_dSum)))
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
                        str(d_step) + ',' + str(d_min) + ',' + str(s_step) + ',' + str(s_min)
                        + '\n' + stds + '\n' + x_train)
        # 索引文件
        tfc.text_Create(self.path_write, ele, ','.join(map(str, list_ele)))
        # 总位移文件
        tfc.text_Create(self.path_write, dSum_w, '\n'.join(list_w_dSum) + '\n' + rbf_type)
        # 应力文件
        tfc.text_Create(self.path_write, stress_w, '\n'.join(list_w_stress) + '\n' + rbf_type)
        # # 坐标文件【坐标一般需要变换一下，就不直接输出了】
        tfc.text_Create(self.path_write, coord, ','.join(map(str, list_coords)))

    def dataSaveToJSON_Kriging(self, fd, which_part):
        """
        :param fd: 输入的训练自变量
        :return:
        """
        surfaced = SurfaceData(self.path_read, self.geometry_type)
        """以下为节点数据"""
        # 索引
        list_ele = surfaced.get_Ele_Data()
        # print(len(set(sorted(map(int, list_ele.split(',')), key=lambda x: x))))
        list_coords = surfaced.get_Coord_Data()
        # 位移
        txt_displacement, txt_dopSum, d_step, d_min = surfaced.get_Displacement_DopSum_Dcolor_Bysorted()
        # 应力
        txt_stress, s_step, s_min = surfaced.get_Stress_SStepandMin_Bysorted()
        # print(len(list_coords.split('\n')[0].split(',')))
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
            dSum_real = np.asarray(list_dopSum[i]).reshape(-1, 1)
            kriging_stress = KrigingSurrogate()
            kriging_dSum = KrigingSurrogate()
            kriging_stress.train(fd, stress_real)
            kriging_dSum.train(fd, dSum_real)

            dict_kriging_model = {}
            dict_kriging_model["thetas"] = kriging_stress.thetas.tolist()
            dict_kriging_model["X_mean"] = kriging_stress.X_mean.tolist()
            dict_kriging_model["X_std"] = kriging_stress.X_std.tolist()
            dict_kriging_model["n_samples"] = kriging_stress.n_samples
            dict_kriging_model["X"] = kriging_stress.X.tolist()
            dict_kriging_model["alpha"] = kriging_stress.alpha.tolist()
            dict_kriging_model["Y_mean"] = kriging_stress.Y_mean.tolist()
            dict_kriging_model["Y_std"] = kriging_stress.Y_std.tolist()

            print("\r" + kriging_stress.__class__.__name__ + "程序当前已完成：" + str(
                round(i / len(list_stress) * 10000) / 100) + '%', end="")

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

    def dataSaveToJSON_RBF(self, v_fd, rbf_type='lin_a', which_part='truss'):
        """

        :param v_fd: 输入的训练自变量
        :param rbf_type: 使用的rbf类型
        :param which_part: 存储的数据是哪个零件的
        :return:
        """
        surfaced = SurfaceData(self.path_read, self.geometry_type)
        """以下为节点数据"""
        # 索引
        list_ele = surfaced.get_Ele_Data()
        # print(len(set(sorted(map(int, list_ele.split(',')), key=lambda x: x))))
        list_coords = surfaced.get_Coord_Data()
        # 位移
        txt_displacement, txt_dopSum, d_step, d_min = surfaced.get_Displacement_DopSum_Dcolor_Bysorted()
        # 应力
        txt_stress, s_step, s_min = surfaced.get_Stress_SStepandMin_Bysorted()
        # print(len(list_coords.split('\n')[0].split(',')))
        stds = None
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
            stds = rbfnet_stress.std
            list_w_stress.append(w_stress)
            list_w_dSum.append(w_dSum)
            print("\r" + rbfnet_stress.__class__.__name__ + "程序当前已完成：" + str(
                round(i / len(list_stress) * 10000) / 100) + '%', end="")
        if v_fd.ndim == 1:
            x_train = v_fd.flatten().tolist()
        elif v_fd.ndim == 2:
            x_train = v_fd.flatten().tolist()
        else:
            x_train = None
        pathisExists = os.path.exists(self.path_write)
        if not pathisExists:
            os.makedirs(self.path_write)  # 不存在创建目录
            pf.printf('文件夹[' + self.path_write + ']创建成功,正在写入文件...')

        dict_rbf_model = {
            "coordinates": list_coords,
            "elements_index": list_ele,

            "stress_w": list_w_stress,
            "stress_step": s_step,
            "stress_min": s_min,

            "deformation_w": list_w_dSum,
            "deformation_step": d_step,
            "deformation_min": d_min,

            "x_train": x_train,
            "stds": stds,
            "rbf_type": rbf_type,
        }
        # print(type(list_coords))
        # print(type(list_coords[0]))
        # print(type(list_ele))
        # print(type(list_ele[0]))
        # print(type(list_w_stress))
        # print(type(list_w_stress[0]))
        # print(type(s_step))
        # print(type(x_train))
        # print(type(rbf_type))
        # print(type(stds))

        json_rbf_model = json.dumps(dict_rbf_model)
        with open("C:/Users/asus/Desktop/" + which_part + ".json", "w") as f:
            json.dump(json_rbf_model, f)
