import numpy as np
import Demo.Ansys_Data_Utils_2021.model_save_to_file as mstf
from Demo.Ansys_Data_Utils_2021.element_data import ElementData
from Demo.Ansys_Data_Utils_2021.coordinate_data import CoordinateData
from Demo.Ansys_Data_Utils_2021.displacement_data import DispalcementData
from Demo.Ansys_Data_Utils_2021.stress_data import StressData
from openmdao.surrogate_models.kriging import KrigingSurrogate
from smt.surrogate_models import KRG
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import json


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
path_prefix = r"H:\Code\DT_Crane_Boom_v1.0\APP_models\\"
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
# 与坐标节点的转换一样，将位移数据按照ele排列，从336个扩充为748个
list_disp_sum_temp = []
list_separateByNewline = str_disp_sum.split('\n')
for separateByNewline in list_separateByNewline:
    list_temp = separateByNewline.split(',')
    _disp_sum = []
    for i in list_ele_data:  # 一个单元两个节点，总共748个节点的编号，按照顺序找到变形数据
        _disp_sum.append(float(list_temp[i]))  # 所以_disp_sum是一个748长度列表
    list_disp_sum_temp.append(_disp_sum)  # 100*748
# 转置一下 748*100
list_disp_sum = np.asarray(list_disp_sum_temp).T.tolist()

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
    list_thetas_stress = []
    list_alpha_stress = []
    list_Y_mean_stress = []
    list_Y_std_stress = []

    list_thetas_deformation = []
    list_alpha_deformation = []
    list_Y_mean_deformation = []
    list_Y_std_deformation = []

    list_X_mean = []
    list_X_std = []
    n_samples = 0
    list_X = []
    print(list_disp_sum[75])
    print(list_disp_sum[74])

    cycle_index = len(list_stress)
    for i in range(cycle_index):
        # for i in [63, 217]:
        fig = plt.figure()
        ax = Axes3D(fig)
        stress_real = np.asarray(list_stress[i]).reshape(-1, 1)
        dSum_real = np.asarray(list_disp_sum[i]).reshape(-1, 1)
        kriging_stress = KrigingSurrogate()
        kriging_deformation = KrigingSurrogate()
        kriging_stress.train(fd, stress_real)
        kriging_deformation.train(fd, dSum_real)
        # stress模型存储
        list_thetas_stress.append(kriging_stress.thetas.tolist())
        list_alpha_stress.append(kriging_stress.alpha.tolist())
        list_Y_mean_stress.append(kriging_stress.Y_mean.tolist())
        list_Y_std_stress.append(kriging_stress.Y_std.tolist())
        # deformation模型存储
        list_thetas_deformation.append(kriging_deformation.thetas.tolist())
        list_alpha_deformation.append(kriging_deformation.alpha.tolist())
        list_Y_mean_deformation.append(kriging_deformation.Y_mean.tolist())
        list_Y_std_deformation.append(kriging_deformation.Y_std.tolist())

        if i == 0:
            list_X_mean = kriging_stress.X_mean.tolist()
            list_X_std = kriging_stress.X_std.tolist()
            n_samples = kriging_stress.n_samples
            list_X = kriging_stress.X.tolist()

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
        _y_dsum = kriging_deformation.predict(_fd1).reshape(_X.shape)
        # print(kriging_stress.predict(np.asarray([[500., 0.], [480, 10], [500, 72], [50, 0], [50, 72]])))

        """
        标准化输出
        """
        # _y_stress = (_y_stress - kriging_stress.Y_mean) / kriging_stress.Y_std
        # _y_d = (_y_d - kriging_deformation.Y_mean) / kriging_deformation.Y_std

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

        # plt.savefig(r"C:\Users\asus\Desktop\pics\\" + str(i) + '.png')
        """
        2020.12.19 避免画图内存泄露
        """
        plt.close('all')  # 避免内存泄漏
        print("\r" + kriging_stress.__class__.__name__ + "程序当前已完成：" + str(
            round(i / len(list_stress) * 10000) / 100) + '%',
              end="")
    dict_kriging_model = {
        "thetas":
            {
                "deformation": list_thetas_deformation,
                "stress": list_thetas_stress,
            },
        "alpha":
            {
                "deformation": list_alpha_deformation,
                "stress": list_alpha_stress,
            },
        "Y_mean":
            {
                "deformation": list_Y_mean_deformation,
                "stress": list_Y_mean_stress,
            },
        "Y_std":
            {
                "deformation": list_Y_std_deformation,
                "stress": list_Y_std_stress,
            },
        # 以下的四个参数stress和deformation的相同
        "X_mean": list_X_mean,
        "X_std": list_X_std,
        "n_samples": n_samples,
        "X": list_X,
    }
    # dict_kriging_dSum_model = {
    #     "thetas": kriging_deformation.thetas.tolist(),  # x
    #     "X_mean": kriging_deformation.X_mean.tolist(),  #
    #     "X_std": kriging_deformation.X_std.tolist(),  #
    #     "n_samples": kriging_deformation.n_samples,  #
    #     "X": kriging_deformation.X.tolist(),  #
    #     "alpha": kriging_deformation.alpha.tolist(),  # x
    #     "Y_mean": kriging_deformation.Y_mean.tolist(),  # x
    #     "Y_std": kriging_deformation.Y_std.tolist(),  # x
    # }
    # print(dict_kriging_model)
    # plt.show()

    json_rbf_model = json.dumps(dict_kriging_model)
    with open("C:/Users/asus/Desktop/" + path_switch[4:-2] + ".json", "w") as f:
        json.dump(json_rbf_model, f)


"""模型训练"""
Surrogate_Model()

"""测试用，直接输出颜色数据"""
# text_Create(path_four_write, "stress", str_stress_color)

# 下面两个是应力和位移的训练数据
# text_Create(path_four_write, "stress", str_stress_results.rstrip('\n'))
# text_Create(path_four_write, "disp", str_disp_sum_results.rstrip('\n'))
