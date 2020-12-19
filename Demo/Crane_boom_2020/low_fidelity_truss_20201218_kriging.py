import numpy as np
import dat_to_file as dtf
from ele_data import ElementData
from coords_data import CoordinateData
from disp_data import DispalcementData
from stre_data import StressData
from txt_file_create import text_Create
from openmdao.surrogate_models.kriging import KrigingSurrogate
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# R^2
def r2(data_real, data_predict):
    RSS = np.sum((data_predict - data_real) ** 2)
    TSS = np.sum((data_real - np.average(data_real)) ** 2)
    return 1 - RSS / TSS


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
# print(fd)
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
str_disp_xyz, str_disp_sum, str_disp_color, str_disp_step_min = dd.allDisplacement_To_Str_Beam188()
# 获得每个节点的应力数据，返回三个值【第一个】 374
str_stress_data, str_stress_color, str_stress_step_min = sd.allStress_To_Str_Beam188()
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
list_disp_sum, len_data_dopSum = dtf._getData(str_disp_sum_results.rstrip('\n'), 'stressOrdSum')

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

list_stress, len_data_stress = dtf._getData(str_stress_results.rstrip('\n'), 'stressOrdSum')

"""
-------------------------------【代理模型】-------------------------------------------
"""


def create_figure(_ax, _test_X, _test_Y, _predict_results, _train_X, _train_Y, _real_results,
                  color_map='rainbow', point_color='k'):
    _ax.plot_surface(
        _test_X,
        _test_Y,
        _predict_results,
        rstride=1,
        cstride=1,
        cmap=plt.get_cmap(color_map)  # coolwarm
    )
    _ax.scatter(
        _train_X,
        _train_Y,
        _real_results.reshape(_train_X.shape).T,
        c=point_color,
    )


def Surrogate_Model():
    list_w_stress = []
    list_w_dSum = []
    cycle_index = len(list_stress)
    list_r2 = []
    for i in range(cycle_index):
    # for i in [63, 217]:
        fig = plt.figure()
        ax = Axes3D(fig)
        stress_real = np.asarray(list_stress[i]).reshape(-1, 1)
        # dSum_real = np.asarray(list_disp_sum[i]).reshape(-1, 1)
        kriging_stress = KrigingSurrogate()
        kriging_dSum = KrigingSurrogate()
        kriging_stress.train(fd, stress_real)
        # kriging_dSum.train(fd, dSum_real)
        _forceArr = np.linspace(50, 500, 50)
        _degreeArr = np.linspace(0, 72, 50)
        """
        画三维图一定不能忘了meshgrid
        """
        _X, _Y = np.meshgrid(_forceArr, _degreeArr)
        """
        2018.12.18 训练点的X,Y，可以通过打印X,Y得到X的排布，在根据这个排布去决定Z轴的排布。
        """
        X, Y = np.meshgrid(forceArr, degreeArr)
        # print(_X.shape, _Y.shape)
        # print(_X)
        # print(X)
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

        # combine = []
        # for _i in range(X.shape[0]):
        #     for _j in range(X.shape[1]):
        #         combine.append((X[_i, _j], Y[_i, _j]))
        # _fd2 = np.array(combine)
        # print(_fd1)
        """
        2020.12.17 得到的结果数据，应该与X或Y的shape一样才能画出来三维图
        """
        _y_stress = kriging_stress.predict(_fd1).reshape(_X.shape)
        """
        2020.12.19 加入变形结果数据
        """
        _y_dsum = kriging_dSum.predict(_fd1).reshape(_X.shape)
        # print(kriging_stress.predict(np.asarray([[500., 0.], [480, 10], [500, 72], [50, 0], [50, 72]])))

        """
        标准化输出
        """
        # _y_stress = (_y_stress - kriging_stress.Y_mean) / kriging_stress.Y_std
        # _y_d = (_y_d - kriging_dSum.Y_mean) / kriging_dSum.Y_std

        # ax = fig.add_subplot(111, projection='3d')
        # rstride:行之间的跨度  cstride:列之间的跨度，只能为正整数，默认是1，
        # 就是和linspace分割的块数一致，数字越大，图形的块数越少
        # rcount:设置间隔个数，默认50个，ccount:列的间隔个数  不能与上面两个参数同时出现
        create_figure(ax, _X, _Y, _y_stress, X, Y, stress_real)
        # create_figure(ax, _X, _Y, _y_dsum, X, Y, dSum_real, "coolwarm")
        # ax.plot_surface(
        #     _X,
        #     _Y,
        #     _y_stress,
        #     rstride=1,
        #     cstride=1,
        #     cmap=plt.get_cmap('rainbow')  # coolwarm
        # )
        # list_r2.append(_y_stress)
        """
        2020.12.18 因为应力是按照：力为第一维，角度为第二维，但是X是力的广播，Y是角度的广播。
        所以要对应力的数值进行转置。
        """
        # ax.scatter(
        #     X,
        #     Y,
        #     stress_real.reshape(10, 10).T,
        #     c='k',
        # )
        # 绘制从3D曲面到底部的投影,zdir 可选 'z'|'x'|'y'| 分别表示投影到z,x,y平面
        # zdir = 'z', offset = -2 表示投影到z = -2上
        # ax.contour(_degreeArr, _forceArr, _y_stress, zdir='z', offset=-2, cmap=plt.get_cmap('rainbow'))
        # 设置z轴的维度，x,y类似
        # ax.set_zlim(-2, 2)

        # list_w_stress.append([
        #     kriging_stress.X,
        #     kriging_stress.X_mean,
        #     kriging_stress.X_std,
        #     kriging_stress.Y_mean,
        #     kriging_stress.Y_std,
        #     kriging_stress.thetas,
        #     kriging_stress.n_samples,
        #     kriging_stress.alpha
        # ])
        # list_w_dSum.append([
        #     kriging_dSum._X,
        #     kriging_dSum.X_mean,
        #     kriging_dSum.X_std,
        #     kriging_dSum.Y_mean,
        #     kriging_dSum.Y_std,
        #     kriging_dSum.thetas,
        #     kriging_dSum.n_samples,
        #     kriging_dSum.alpha
        # ])
        # plt.savefig(r"C:\Users\asus\Desktop\pics\\" + str(i) + '.png')
        """
        2020.12.19 避免画图内存泄露
        """
        plt.close('all')  # 避免内存泄漏
        print("\r" + kriging_stress.__class__.__name__ + "程序当前已完成：" + str(
            round(i / len(list_stress) * 10000) / 100) + '%',
              end="")
    #
    # stepAndMin = path_switch[4:-2] + '_others'
    # ele = path_switch[4:-2] + '_ele'
    # dSum_w = path_switch[4:-2] + '_dSum_w'
    # stress_w = path_switch[4:-2] + '_stress_w'
    # coord = path_switch[4:-2] + '_coord'
    # x_train = ','.join(map(lambda x: ','.join(map(str, x)), fd.tolist()))
    #
    # # 步数和最小值，方差，输入值
    # text_Create(path_four_write, stepAndMin,
    #             str_disp_step_min + ',' + str_stress_step_min + '\n' + stds + '\n' + x_train)
    # # 索引文件
    # text_Create(path_four_write, ele, ','.join(map(str, list_ele_data)))
    # # 坐标文件
    # text_Create(path_four_write, coord, ','.join(list_coord_results))
    # # 总位移文件
    # text_Create(path_four_write, dSum_w, '\n'.join(list_w_dSum) + '\n' + rbf_type)
    # # 应力文件
    # text_Create(path_four_write, stress_w, '\n'.join(list_w_stress) + '\n' + rbf_type)
    # print(r2(list_r2[0], list_r2[1]))
    # plt.show()


"""模型训练"""
Surrogate_Model()

"""测试用，直接输出颜色数据"""
# text_Create(path_four_write, "stress", str_stress_color)

# 下面两个是应力和位移的训练数据
# text_Create(path_four_write, "stress", str_stress_results.rstrip('\n'))
# text_Create(path_four_write, "disp", str_disp_sum_results.rstrip('\n'))


# dtf.dataToPostFile_v2_Bysorted(v_fd=fd, rbf_type='lin_a', which_part=path_switch[4:-2])
# dtf.dataToMidFile()
