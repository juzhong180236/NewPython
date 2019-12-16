import os
from surface_data_process import SurfaceData
from rbf import RBF
import text_file_create as tfc
import printf as pf


def _getData(string, fileType):
    # 将多个文件（5个）合并过的变形、应力、坐标值数据等字符串以换行符分解为list
    list_separateByNewline = string.split('\n')
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
        return list_stress


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

    def dataToPostFile(self, variable, rbf_type='lin_a'):
        surfaced = SurfaceData(self.path_read, self.geometry_type)
        txt_ele = surfaced.get_Ele_Data()
        txt_coord_x = surfaced.get_Coord_Data('x')
        txt_dopCoord, txt_dopSum, txt_DstepandMin = surfaced.get_DopCoord_DopSum_DStepandMin()
        txt_stress, txt_SstepandMin = surfaced.get_Stress_SStepandMin()
        coordsFile = open(self.path_read + 'coord.txt', "rt")
        str_coords = coordsFile.read()
        coordsFile.close()

        stds = ''
        list_x, list_y, list_z = _getData(str_coords, 'coord')
        list_stress = _getData(txt_stress, 'stressOrdSum')
        list_dopSum = _getData(txt_dopSum, 'stressOrdSum')
        list_w_y = []
        list_w_z = []
        list_w_stress = []
        list_w_dSum = []
        cycle_index = len(list_x)
        for i in range(cycle_index):
            y_real = list_y[i]
            z_real = list_z[i]
            stress_real = list_stress[i]
            dSum_real = list_dopSum[i]
            rbfnet_y = RBF(rbf_type)
            rbfnet_z = RBF(rbf_type)
            rbfnet_stress = RBF(rbf_type)
            rbfnet_dSum = RBF(rbf_type)
            w_y = rbfnet_y.fit(variable, y_real)
            w_z = rbfnet_z.fit(variable, z_real)
            w_stress = rbfnet_stress.fit(variable, stress_real)
            w_dSum = rbfnet_dSum.fit(variable, dSum_real)
            stds = str(rbfnet_y.std)
            list_w_y.append(w_y)
            list_w_z.append(w_z)
            list_w_stress.append(w_stress)
            list_w_dSum.append(w_dSum)
            print("\r" + rbfnet_y.__class__.__name__ + "程序当前已完成：" + str(round(i / len(list_y) * 10000) / 100) + '%',
                  end="")

        ele = 'ele'
        coord_x = 'coord_x'
        stepAndMin = 'step_min'
        y_w = 'y_w'
        z_w = 'z_w'
        dSum_w = 'dSum_w'
        stress_w = 'stress_w'

        tfc.text_Create(self.path_write, ele, txt_ele)
        tfc.text_Create(self.path_write, coord_x, txt_coord_x)
        tfc.text_Create(self.path_write, stepAndMin, txt_DstepandMin + ',' + txt_SstepandMin)

        tfc.text_Create(self.path_write, y_w, '\n'.join(list_w_y) + '\n' + stds + '\n' + ','.join(
            map(lambda x: ','.join(map(str, x)), variable.tolist())) + '\n' + rbf_type)
        tfc.text_Create(self.path_write, z_w, '\n'.join(list_w_z) + '\n' + rbf_type)
        tfc.text_Create(self.path_write, dSum_w, '\n'.join(list_w_dSum) + '\n' + rbf_type)
        tfc.text_Create(self.path_write, stress_w, '\n'.join(list_w_stress) + '\n' + rbf_type)
