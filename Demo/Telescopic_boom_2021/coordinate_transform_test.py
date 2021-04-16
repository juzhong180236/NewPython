import Demo.Telescopic_boom_2021.coordinate_transform.coordinate_transform as ct
from Demo.Telescopic_boom_2021.libs.element_data import ElementData
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


def create_figure(_ax, _array, point_color='k'):
    for arr_child in _array:
        _ax.scatter(
            arr_child[0],
            arr_child[1],
            arr_child[2],
            c=point_color,
        )


def ax_fun(_ax):
    BIGGER_SIZE = 16
    MIDDLE_SIZE = 12
    _ax.set_xlabel("x", fontsize=BIGGER_SIZE)
    _ax.set_ylabel("y", fontsize=BIGGER_SIZE)
    _ax.set_zlabel('z', fontsize=BIGGER_SIZE)
    plt.tick_params(labelsize=MIDDLE_SIZE)  # fontsize of the tick labels


# path_prefix = r"C:\Users\asus\Desktop\Code\DT_Telescopic_Boom_v1.0\APP_models\\"
# # path_switch = 'rbf_correct_model'
# path_switch = r'pre_telescopic_boom\\'
# # 读取路径(读pre)
# path_four_read = path_prefix + path_switch
#
# """
# 以1_1的网格作为最终的网格排布形态，读取节点索引数据
# """
# elements = open(path_four_read + r'elements_sort\1_1.txt', 'rt')
# elements_str = elements.read()
# elements_list = elements_str.split("C")
# ele_result_list = []
# for ele_str in elements_list:
#     ele_component_list = []
#     temp_list = ele_str.strip().split("\n")
#     for temp_list_child in temp_list:
#         _list = temp_list_child.split()
#         ele_number = int(_list[0])
#         node_1 = int(_list[1])
#         node_2 = int(_list[2])
#         node_3 = int(_list[3])
#         node_4 = int(_list[4])
#         node_5 = int(_list[5])
#         node_6 = int(_list[6])
#         node_7 = int(_list[7])
#         node_8 = int(_list[8])
#         ele_component_list.append(
#             [ele_number, node_1, node_2, node_3, node_4,
#              node_5, node_6, node_7, node_8])
#     ele_result_list.append(ele_component_list)
# elements.close()
#
# ele_data = ElementData(geometry_type=['3D4_P'], data_list=ele_result_list)
# set_ele_surface_list_1_1 = ele_data.set_SurfaceEle_aerofoil()
# # # 在Three.js中可用的索引数据
# # ele_data_save = ele_data.surfaceEle_Real_Sequence_aerofoil(path_four_read + r'coordinates\1_1.txt')
# print("The element data in the file '1_1' has been loaded！")
#
# """
# 以1_1的网格作为最终的网格排布形态，所有后续的网格训练出的模型用1_1作为输入进行预测
# """
# coordinates_benchmark = open(path_four_read + r'coordinates_sort\1_1.txt', 'rt')
# coordinates_benchmark_str = coordinates_benchmark.read()
# coordinates_benchmark_list = coordinates_benchmark_str.split("C")
#
# cd_benchmark_result_list = []
# # 命名为C_1到C_4的Component，共4个Components，即4次循环
# for i_list, _ in enumerate(coordinates_benchmark_list):
#     cd_benchmark_component_list = []
#     cd_temp_list = coordinates_benchmark_list[i_list].strip().split("\n")
#     # 每个Component中的坐标个数。根据Component的不同循环次数不同
#     for i_list_child, _ in enumerate(cd_temp_list):
#         cd_list_child = cd_temp_list[i_list_child].split()
#         cd_index = int(cd_list_child[0])
#         if cd_index in set_ele_surface_list_1_1[i_list]:
#             cd_benchmark_component_list.append([float(cd_list_child[1]),
#                                                 float(cd_list_child[2]),
#                                                 float(cd_list_child[3])])
#     cd_benchmark_result_list.append(cd_benchmark_component_list)  # 这个得到的数据因为是4个不同的component，所以长度不同
# coordinates_benchmark.close()
#
# print("The coordinates & stress & displacement data in the file '1_1' has been loaded！")

# point = np.array(cd_benchmark_result_list[0]).reshape(-1, 3)
# rotated_coordinate = np.array(ct.rotateX(point[0], 30)).reshape(-1, 3)
# # ct.translate()
# print(point[0])
# print(rotated_coordinate)
# fig = plt.figure(figsize=(10, 8))
# ax = Axes3D(fig)
# create_figure(ax, point[0].reshape(-1, 3))
# create_figure(ax, rotated_coordinate, "r")
# ax_fun(ax)
point = []
_y = np.linspace(0, np.pi / 2, 10)
_z = np.sin(_y)
_x = np.array([0] * _y.shape[0])
for i in range(_x.shape[0]):
    rotated_coordinate = np.array(ct.rotateX([_x[i], _y[i], _z[i]], -10))
    plt.scatter(_y[i], _z[i], color='#0000ff', label='point', marker='s')
    plt.scatter(rotated_coordinate[1], rotated_coordinate[2], color='r', label='point', marker='s')

# translate_coordinate = np.array(ct.translate(point, 30, 0, 0))
# plt.scatter(translate_coordinate[0], translate_coordinate[1], color='#0000ff', label='point', marker='s')
plt.show()
