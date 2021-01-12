import numpy as np
import Demo.Ansys_Data_Utils_2021.model_save_to_file as mstf
from Demo.Ansys_Data_Utils_2021.element_data import ElementData
from Demo.Ansys_Data_Utils_2021.coordinate_data import CoordinateData
from Demo.Ansys_Data_Utils_2021.displacement_data import DispalcementData
from Demo.Ansys_Data_Utils_2021.stress_data import StressData
from Demo.Ansys_Data_Utils_2021.txt_file_create import text_Create
from Demo.Ansys_Data_Utils_2021.Surrogate_Models.RBF import RBF
import Demo.Ansys_Data_Utils_2021.print_f as pf
import os


def list_results_data(list_ele, list_input):
    list_results = []
    for i in list_ele:  # 单元中每个节点的编号
        list_results.extend(
            [list_input[i * 3],
             list_input[i * 3 + 1],
             list_input[i * 3 + 2]]
        )
    return list_results


"""
所谓low_fidelity，其实就是Beam188单元
"""
path_prefix = r"C:\Users\asus\Desktop\Code\DT_Crane_Boom_v1.0\APP_models\\"
# path_switch = 'rbf_correct_model'
path_switch = r'pre_low_fidelity_truss\\'
# 读取路径(读pre)
path_four_read = path_prefix + path_switch
# 写入路径(写在mid)
path_four_write = path_prefix + r"post_low_fidelity_truss\\"
# 网格类型
geometry_type = ['BEAM_188']
# 训练自变量
forceArr = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500]  # 50 100 150 200 250 300 350 400 450 500
degreeArr = [0, 8, 16, 24, 32, 40, 48, 56, 64, 72]  # 0 8 16 24 32 40 48 56 64 72
combine = []
for iForce in range(len(forceArr)):
    for iDegree in range(len(degreeArr)):
        combine.append((forceArr[iForce], degreeArr[iDegree]))
fd = np.array(combine)
fd_flat = fd.flatten()

# 单元对象
ed = ElementData(path_four_read + r"ele\\", geometry_type)
# 坐标对象
cd = CoordinateData(path_four_read + r"dopAndCoord\\")
# 位移对象
dd = DispalcementData(path_four_read + r"dopAndCoord\\")
# 应力对象
sd = StressData(path_four_read + r"equivalent_stress\\")

"""
1、单元对象包括每个单元的两个节点，共374个单元，每个单元两个节点，共748个节点。
2、坐标对象是每个节点的坐标值，共336个节点，故有336个不重复的坐标值。
3、位移对象是每个节点的位移值，共336个。
4、应力对象是每个单元的应力，共374个。
"""

# 获得单元中节点的排布数据 748
list_ele_data = ed.all_Ele_To_List()
# 获得每个节点的坐标数据 336
list_coord_data = cd.allCoord_To_List()
# 获取每个节点的位移数据，返回四个值【第二个】 336
str_disp_xyz, str_disp_sum, str_disp_color, d_step, d_min = dd.allDisplacement_To_Str_Beam188()
# 获得每个节点的应力数据，返回三个值【第一个】 374
str_stress_data, str_stress_color, s_step, s_min = sd.allStress_To_Str_Beam188()
# print(str_stress_color)
"""
-------------------------------【坐标】-------------------------------------------
因为坐标不能简单的排布，需要按照设定的顺序排布，所以在python中将坐标处理成按ele顺序排列的列表
共单元数748*3=2244个
"""
list_coord_results = list_results_data(list_ele_data, list_coord_data)

""" 
-------------------------------【位移】-------------------------------------------
与上述的代码一样，同样将位移数据按照ele排列，从336个扩充为748个。位移状态总共有100个。
"""
# 首先将读取到的每个节点（共336个节点，100个文件）的位移数据从str变为list
list_disp_sum = []
list_separateByNewline = str_disp_sum.split('\n')
for separateByNewline in list_separateByNewline:
    list_temp = separateByNewline.split(',')
    list_disp_sum.append(list_temp)
# 与坐标节点的转换一样，将位移数据按照ele排列，从336个扩充为748个
list_disp_sum_results = []
for disp_sum in list_disp_sum:
    _disp_sum = []
    for i in list_ele_data:  # 单元中每个节点的编号
        _disp_sum.append(disp_sum[i])
    list_disp_sum_results.append(_disp_sum)
# 将扩充完成后的数据从list转为str
str_disp_sum_results = ''
for disp_sum_results in list_disp_sum_results:
    str_disp_sum_results += ','.join(disp_sum_results) + '\n'
# 输入到_getData函数中，输入为100*748，输出为748*100
"""
这个函数的用处是将应力或者位移数据从一个第一维为M个状态，第二维为N个节点的列表
转换为一个第一维为N个节点，第二维为M个状态的列表。
例如，100个状态，力10个，角度10个，总共100个。节点数为336个。
则输入100*336的列表，输出336*100的列表。
"""
list_disp_sum, len_data_dopSum = mstf._getData(str_disp_sum_results.rstrip('\n'), 'stressOrdSum')

# print(len(list_disp_sum[0]))

""" 
-------------------------------【应力】-------------------------------------------
因为应力是按照单元输出的，apdl的输出的是等效应力只有一个值，但是一个单元两个节点，
直接复制，将应力数据由[1,2,3]变为[1,1,2,2,3,3]就可以
"""
# str转为list
list_stress_data = []
list_stress_per = str_stress_data.split('\n')
for separateByNewline in list_stress_per:
    # 将应力数据由[1,2,3]变为[1,1,2,2,3,3]就可以
    list_temp = [val for val in separateByNewline.split(',') for i in range(2)]
    list_stress_data.append(list_temp)

# 将扩充完成后的数据从list转为str
str_stress_results = ''
for stress_results in list_stress_data:
    str_stress_results += ','.join(stress_results) + '\n'

list_stress, len_data_stress = mstf._getData(str_stress_results.rstrip('\n'), 'stressOrdSum')

"""
-------------------------------【代理模型】-------------------------------------------
"""


def Surrogate_Model():
    rbf_type = 'lin_a'
    list_w_stress = []
    list_w_dSum = []
    # list_y_name = []
    stds = ''
    cycle_index = len(list_stress)
    for i in range(cycle_index):
        stress_real = list_stress[i]
        dSum_real = list_disp_sum[i]
        rbfnet_stress = RBF(rbf_type)
        rbfnet_dSum = RBF(rbf_type)
        w_stress = rbfnet_stress.fit(fd, stress_real)
        w_disp = rbfnet_dSum.fit(fd, dSum_real)
        stds = str(rbfnet_stress.std)
        list_w_stress.append(w_stress)
        list_w_dSum.append(w_disp)
        print("\r" + rbfnet_stress.__class__.__name__ + "程序当前已完成：" + str(round(i / cycle_index * 10000) / 100) + '%',
              end="")

    stepAndMin = path_switch[4:-2] + '_others'
    ele = path_switch[4:-2] + '_ele'
    dSum_w = path_switch[4:-2] + '_dSum_w'
    stress_w = path_switch[4:-2] + '_stress_w'
    coord = path_switch[4:-2] + '_coord'
    x_train = ','.join(map(lambda x: ','.join(map(str, x)), fd.tolist()))

    pathisExists = os.path.exists(path_four_write)
    if not pathisExists:
        os.makedirs(path_four_write)  # 不存在创建目录
        pf.printf('文件夹[' + path_four_write + ']创建成功,正在写入文件...')
    # 步数和最小值，方差，输入值
    text_Create(path_four_write, stepAndMin,
                d_step + ',' + d_min + ',' + s_step + ',' + s_min + '\n' + stds + '\n' + x_train)
    # 索引文件
    text_Create(path_four_write, ele, ','.join(map(str, list_ele_data)))
    # 坐标文件
    text_Create(path_four_write, coord, ','.join(list_coord_results))
    # 总位移文件
    text_Create(path_four_write, dSum_w, '\n'.join(list_w_dSum) + '\n' + rbf_type)
    # 应力文件
    text_Create(path_four_write, stress_w, '\n'.join(list_w_stress) + '\n' + rbf_type)


"""模型训练"""
Surrogate_Model()

"""测试用，直接输出颜色数据"""
# text_Create(path_four_write, "stress", str_stress_color)

# 下面两个是应力和位移的训练数据
# text_Create(path_four_write, "stress", str_stress_results.rstrip('\n'))
# text_Create(path_four_write, "disp", str_disp_sum_results.rstrip('\n'))


# dtf.dataToPostFile_v2_Bysorted(v_fd=fd, rbf_type='lin_a', which_part=path_switch[4:-2])
# dtf.dataToMidFile()
