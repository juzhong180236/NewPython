import numpy as np


class ElementData(object):
    def __init__(self, mapdl_mesh_elem=None, element_type=None):
        self.element_type = element_type
        self.mapdl_mesh_elem = mapdl_mesh_elem

    # def all_int_list_original(self):
    #     return list(map(lambda x: x[-4:], self.mapdl_mesh_elem))

    def all_int_list(self):
        shell181 = 181  # 4-Node Structural Shell
        solid185 = 185  # 3-D 8-Node Structural Solid.
        solid186 = 186  # 3-D 20-Node Structural Solid.
        solid187 = 187  # 3-D 10-Node Tetrahedral Solid.
        beam188 = 188  # 3-D 2-Node Beam.
        fluid29 = 29  # (not sure) 2-D Axisymmetric Harmonic Acoustic Fluid

        shell181_mesh = 1810  # mesh line

        # list_all_ele = self.all_int_list_original()
        list_all_ele = self.mapdl_mesh_elem
        list_result = []
        for each_ele in list_all_ele:
            if self.element_type in [solid185]:  # 4
                list_result.extend([each_ele[0], each_ele[2], each_ele[1],
                                    each_ele[1], each_ele[2], each_ele[4],
                                    each_ele[0], each_ele[4], each_ele[2],
                                    each_ele[0], each_ele[1], each_ele[4]])
            elif self.element_type in [solid186]:  # 8
                list_result.extend(
                    [each_ele[0], each_ele[1], each_ele[2],
                     each_ele[0], each_ele[2], each_ele[3],
                     each_ele[4], each_ele[5], each_ele[6],
                     each_ele[4], each_ele[6], each_ele[7],
                     each_ele[0], each_ele[3], each_ele[7],
                     each_ele[0], each_ele[4], each_ele[7],
                     each_ele[1], each_ele[5], each_ele[6],
                     each_ele[1], each_ele[2], each_ele[6],
                     each_ele[0], each_ele[4], each_ele[5],
                     each_ele[0], each_ele[1], each_ele[5],
                     each_ele[2], each_ele[6], each_ele[7],
                     each_ele[2], each_ele[6], each_ele[7]])
            elif self.element_type in [solid187]:  # 4
                list_result.extend([each_ele[0], each_ele[2], each_ele[1],
                                    each_ele[1], each_ele[2], each_ele[3],
                                    each_ele[0], each_ele[3], each_ele[2],
                                    each_ele[0], each_ele[1], each_ele[3]])
            elif self.element_type in [fluid29, shell181]:  # 4
                list_result.extend([each_ele[0], each_ele[1], each_ele[2],
                                    each_ele[2], each_ele[0], each_ele[3]])
            elif self.element_type in [beam188]:  # 2
                list_result.extend([each_ele[0], each_ele[1]])
            elif self.element_type in [shell181_mesh]:
                list_result.extend([each_ele[0], each_ele[1],
                                    each_ele[1], each_ele[2],
                                    each_ele[2], each_ele[3],
                                    each_ele[3], each_ele[0], ])
            else:
                print("This type of element has not been added in the data saving program.")
        return list_result

    def all_str(self):
        """
        :return:返回表面以及内部所有节点索引的str
        """
        return ','.join(map(str, self.all_int_list()))

    def all_int_list_threejs(self):
        return list(map(lambda x: int(x) - 1, self.all_int_list()))

    def surface_str(self):
        """
        【输出str】：删除模型除表面以外、内部点的索引，返回以【逗号】隔开，可绘制模型【表面】的排列好的索引值字符串(string)
        【功能】：每三个相连索引为一组，所有只出现一次（模型表面）的索引组所构成的字符串
        :return:
        """
        list_all_ele = self.all_int_list()
        if not list_all_ele:
            return
        # 将索引信息转为int类型后，每3个一组（称为【单面索引组】）进行排序，得到【顺序单面索引组】，再转为字符串，放入list_sort中。
        # 例如953转为'3,5,9'
        dict_real_sort = {}
        list_sort = []
        for i in range(0, len(list_all_ele), 3):
            list_temp = [list_all_ele[i], list_all_ele[i + 1], list_all_ele[i + 2]]
            list_temp_sorted = sorted(list_temp, key=lambda x: x)
            str_temp_sorted = str(list_temp_sorted[0]) + ',' + str(list_temp_sorted[1]) + ',' + str(list_temp_sorted[2])
            dict_real_sort[str_temp_sorted] = ','.join(map(str, list_temp))  # 三元素小数组中的顺序未变，画两次的索引只剩下画一次
            list_sort.append(str_temp_sorted)  # 排序后的字符串组成的list
        # 直接使用set对相同的顺序单面索引组只保留一个，即对画多次的表面只画一次
        # 这一步使内部面片不用画两次了，但是还是会画一次
        # set_sort=list(dic_sort.keys())
        set_sort = set(list_sort)
        # 每个【顺序单面索引组】的初始出现次数设置为0，使用dict类型保存
        # 例如{'3,5,8':0,'4,5,8':0,...}
        dict_sort = {}
        for ele in list_sort:
            dict_sort[ele] = 0
        # 利用set_sort对list_sort进行检测，list_sort中出现多次的【顺序单面索引组】就会被识别。
        for ele in list_sort:
            if ele in set_sort:
                dict_sort[ele] += 1  # 如果检测到【顺序单面索引组】一次，就加1
        # 最终得到只出现一次的【顺序单面索引组】组成的dict_sort，将它的key保存在list_sort中，
        list_real_sort = []
        for key, value in dict_sort.items():
            if value == 1:
                list_real_sort.append(dict_real_sort[key])
        # 返回逗号隔开的索引值字符串
        return ','.join(list_real_sort)

    def surface_str_list(self):
        return self.surface_str().split(',')

    def surface_int_list(self):
        return list(map(lambda x: int(x), self.surface_str_list()))

    def surface_int_set(self):
        return set(map(lambda x: int(x), set(self.surface_str_list())))

    def surface_int_list_threejs(self, coordinates_arr):
        """
        :param coordinates_arr: 坐标数据
        :return:
        """
        set_surface_ele = self.surface_int_set()
        list_surface_ele = self.surface_int_list()
        i_coord = 0  # 上述替换真实索引值(real_index_1、real_index_2...)的值
        # 存放所有坐标值的“从0开始的虚假索引”的字典
        # 结构为{real_index_1：[0,x,y,z],real_index_2:[1,x,y,z]...}
        # 其意图是用0,1...来替换real_index_1,real_index_2...
        dict_coord = {}
        for everyline in coordinates_arr:
            everyline_index = everyline[0]
            if everyline_index in set_surface_ele:  # 根据element_data中set_surfaceEle方法返回的信息，只需表面点的坐标
                dict_coord[everyline_index] = i_coord  # 将对应点的真实编号和要更新的iCoord一一对应起来
                i_coord += 1
        # print(list_surface_ele)
        for i_ele in range(len(list_surface_ele)):  # 将排序好的表面点的索引值替换成更新后的0,1,2...索引
            if int(list_surface_ele[i_ele]) in dict_coord.keys():  # 如果list_ele中的索引是表面的点的索引，进行替换
                list_surface_ele[i_ele] = dict_coord[list_surface_ele[i_ele]]  # 获取字典dict_coord中的第一值替换list_ele
        # print('替换后:' + str(list_surface_ele))
        # 将真实索引值（real_index_12...）更新为[0,1...]返回
        return list_surface_ele


class CoordinateData(object):
    def __init__(self, ed=None, mapdl_mesh_nodes=None):
        self.ed = ed
        self.mapdl_mesh_nodes = mapdl_mesh_nodes

    def all_int_list_threejs(self, whichAxis='xyz'):
        coordinates_list = []
        for _i_c, each_ele in enumerate(self.mapdl_mesh_nodes):
            coordinates_list.append(np.hstack((_i_c + 1, each_ele)))
        list_coords = []
        for each_ele in coordinates_list:
            if whichAxis == 'x':
                list_coords.extend(each_ele[1])  # x
            elif whichAxis == 'y':
                list_coords.extend(each_ele[2])  # y
            elif whichAxis == 'z':
                list_coords.extend(each_ele[3])  # z
            else:
                list_coords.extend([each_ele[1], each_ele[2], each_ele[3]])  # xyz
        return list_coords

    def surface_int_list_threejs(self, whichAxis='xyz'):
        set_surface_ele = self.ed.surface_int_set()
        list_all_ele = self.all_int_list_threejs()
        list_coords = []
        for each_ele in list_all_ele:
            everyline_index = int(each_ele[0])
            if everyline_index in set_surface_ele:  # 根据element_data中set_surfaceEle方法返回的信息，只需表面点的坐标
                if whichAxis == 'x':
                    list_coords.extend(each_ele[1])  # x
                elif whichAxis == 'y':
                    list_coords.extend(each_ele[2])  # y
                elif whichAxis == 'z':
                    list_coords.extend(each_ele[3])  # z
                else:
                    list_coords.extend([each_ele[1], each_ele[2], each_ele[3]])  # xyz
        return list_coords


if __name__ == "__main__":
    pass
