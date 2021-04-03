import os
import Demo.Ansys_Data_Utils_2021.print_f as pf


class ElementData(object):
    def __init__(self, path_ele=None, geometry_type=None, data_list=None):
        if path_ele is not None:
            self.path_ele = path_ele + 'ELIST.lis'
        else:
            self.path_ele = None
        self.geometry_type = geometry_type
        self.data_list = data_list
        pass

    def all_Ele_To_List(self):
        return self.__allEle_To_List()

    def sort_Node_Index(self, list_temp):
        TETRAHEDRON_LINEAR = '3D4_L'
        TETRAHEDRON_PROGRAM_CONTROL = '3D4_P'
        HEXAHEDRON = '3D6'
        TETRAHEDRAL_SHEET = '2D4'
        """
               2020.12.13 增加BEAM188的解析
               """
        BEAM_188 = 'BEAM_188'
        list_result = []
        if len(list_temp) == 8:
            if TETRAHEDRON_LINEAR in self.geometry_type:
                """ 
                2020.12.12
                有时候单元序号是不连续的，但是单元类型是相同的。
                【变保真的会议论文中，桁架的单元序号出现了不连续209179直接跳到了209276】，
                但都是solid185单元。
                其实在apdl导出时，程序通常仅保留单个类型的单元，所以下面这一句判断可以不加，但也要看情况
                【查明原因】：因为有solid186单元没有导出，导致序号不连续。
                """
                # 1332  2391  1389  1389  1372  1372  1372  1372
                # 1594  1999  1617  1617  1616  1616  1616  1616
                # 所有的ele【前4位】排列为【四面体】的画图形式，得到这些值并存在list_result中
                list_result.extend([list_temp[0] - 1, list_temp[2] - 1, list_temp[1] - 1,  # outter
                                    list_temp[1] - 1, list_temp[2] - 1, list_temp[4] - 1,  # outter
                                    list_temp[0] - 1, list_temp[4] - 1, list_temp[2] - 1,  # outter
                                    list_temp[0] - 1, list_temp[1] - 1, list_temp[4] - 1])  # outter
            elif TETRAHEDRON_PROGRAM_CONTROL in self.geometry_type:
                # 190     919    1105     747
                # 88239   88800   88850   89126
                # 所有的ele【前4位】排列为【四面体】的画图形式，得到这些值并存在list_result中
                list_result.extend([list_temp[0] - 1, list_temp[2] - 1, list_temp[1] - 1,
                                    list_temp[1] - 1, list_temp[2] - 1, list_temp[3] - 1,
                                    list_temp[0] - 1, list_temp[3] - 1, list_temp[2] - 1,
                                    list_temp[0] - 1, list_temp[1] - 1, list_temp[3] - 1])
            elif HEXAHEDRON in self.geometry_type:
                # 所有的ele【前8位】排列为【六面体】的画图形式，得到这些值并存在list_result中
                list_result.extend(
                    [list_temp[0] - 1, list_temp[1] - 1, list_temp[2] - 1,
                     list_temp[0] - 1, list_temp[2] - 1, list_temp[3] - 1,
                     list_temp[4] - 1, list_temp[5] - 1, list_temp[6] - 1,
                     list_temp[4] - 1, list_temp[6] - 1, list_temp[7] - 1,
                     list_temp[0] - 1, list_temp[3] - 1, list_temp[7] - 1,
                     list_temp[0] - 1, list_temp[4] - 1, list_temp[7] - 1,
                     list_temp[1] - 1, list_temp[5] - 1, list_temp[6] - 1,
                     list_temp[1] - 1, list_temp[2] - 1, list_temp[6] - 1,
                     list_temp[0] - 1, list_temp[4] - 1, list_temp[5] - 1,
                     list_temp[0] - 1, list_temp[1] - 1, list_temp[5] - 1,
                     list_temp[2] - 1, list_temp[6] - 1, list_temp[7] - 1,
                     list_temp[2] - 1, list_temp[6] - 1, list_temp[7] - 1])
        elif len(list_temp) == 4:
            if TETRAHEDRAL_SHEET in self.geometry_type:
                list_result.extend([list_temp[0] - 1, list_temp[1] - 1,
                                    list_temp[2] - 1, list_temp[2] - 1,
                                    list_temp[0] - 1, list_temp[3] - 1])
        elif len(list_temp) == 3:
            if BEAM_188 in self.geometry_type:
                list_result.extend([list_temp[0] - 1, list_temp[1] - 1])
        return list_result

    # 【输入int,str】：ELIST.lis文件中是四面体节点输入4，六面体节点输入6，第二个参数为ELIST.lis的路径
    # 【输出str】：返回以逗号隔开的可绘制模型表面的排列好的索引值字符串(string)
    # 【功能】：对四面体或六面体的ELIST.lis进行简化，使其只有表面点的信息，极大减少数据量
    def __allEle_To_List(self):
        list_result = []
        if self.path_ele is not None:
            isExisted = os.path.exists(self.path_ele)
            if not isExisted:
                pf.printf(self.path_ele)
                pf.printf('上面列出的路径不存在，请设置正确路径！')
                return
            else:
                pf.printf('文件[' + self.path_ele[len(self.path_ele) - self.path_ele[::-1].index('\\'):] + ']存在,正在读取...')
            eleFile = open(self.path_ele, "rt")
            index_ele = 0
            for every_line in eleFile:
                list_everyline = every_line.split()
                list_cut = list_everyline[1:]
                list_temp = list(map(int, list_cut))
                if (int(list_everyline[0]) - index_ele) != 1:
                    break
                list_result.extend(self.sort_Node_Index(list_temp))
                index_ele += 1
            eleFile.close()
            pf.printf('文件[' + self.path_ele[len(self.path_ele) - self.path_ele[::-1].index('\\'):] + ']读取完成！')
        if self.data_list is not None:
            for every_component in self.data_list:
                index_ele = 0
                list_component = []
                # print(every_component)
                for every_line in every_component:
                    # if len(every_line) == 0:
                    #     print(every_line)
                    # if index_ele == 0:
                    #     print(every_line)
                    # print(every_line)
                    list_temp = every_line[1:]
                    list_component.extend(self.sort_Node_Index(list_temp))
                    # index_ele += 1
                list_result.append(list_component)
                # print(len(list_component)/12)
        return list_result

    def __sameEle_Remove(self, list_allEle):
        """
        【输入list】：经过排列后，能画出四面体或六面体的索引的列表（list）
        【输出str】：删除模型除表面以外、内部点的索引，返回以【逗号】隔开，可绘制模型【表面】的排列好的索引值字符串(string)
        【功能】：每三个相连索引为一组，所有只出现一次（模型表面）的索引组所构成的字符串
        :param list_input:
        :return:
        """
        if not list_allEle:
            return
        # 将索引信息转为int类型后，每3个一组（称为【单面索引组】）进行排序，得到【顺序单面索引组】，再转为字符串，放入list_sort中。
        # 例如953转为'3,5,9'
        dict_real_sort = {}
        list_sort = []
        for i in range(0, len(list_allEle), 3):
            list_temp = [list_allEle[i], list_allEle[i + 1], list_allEle[i + 2]]
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
        # list_sort = []
        # for i in range(0, len(list_allEle), 3):
        #     list_temp = [list_allEle[i], list_allEle[i + 1], list_allEle[i + 2]]
        #     list_temp.sort(key=lambda x: x)
        #     list_sort.append(str(list_temp[0]) + ',' + str(list_temp[1]) + ',' + str(list_temp[2]))
        # # 直接使用set对相同的顺序单面索引组只保留一个，即对画多次的表面只画一次
        # # 这一步使内部面片不用画两次了，但是还是会画一次
        # set_sort = set(list_sort)
        # # 每个【顺序单面索引组】的初始出现次数设置为0，使用dict类型保存
        # # 例如{'3,5,8':0,'4,5,8':0,...}
        # dict_sort = {}
        # for ele in list_sort:
        #     dict_sort[ele] = 0
        # # 利用set_sort对list_sort进行检测，list_sort中出现多次的【顺序单面索引组】就会被识别。
        # for ele in list_sort:
        #     if ele in set_sort:
        #         dict_sort[ele] += 1  # 如果检测到【顺序单面索引组】一次，就加1
        # # 最终得到只出现一次的【顺序单面索引组】组成的dict_sort，将它的key保存在list_sort中，
        # list_sort = []
        # for key, value in dict_sort.items():
        #     if value == 1:
        #         list_sort.append(key)
        # # 返回逗号隔开的索引值字符串
        # return ','.join(list_sort)

    def surfaceEle_Sequence_aerofoil(self):
        """
        :return:返回表面所有节点索引的str
        """
        list_result = []
        for _list in self.__allEle_To_List():
            list_result.append(self.__sameEle_Remove(_list))
        return list_result

    def surfaceEle_Sequence(self):
        """
        :return:返回表面所有节点索引的str
        """
        return self.__sameEle_Remove(self.__allEle_To_List())

    def allEle_Sequence(self):
        """
        :return:返回表面以及内部所有节点索引的str
        """
        return ','.join(map(str, self.__allEle_To_List()))

    def set_SurfaceEle(self):
        """
        :return:返回表面所有节点索引去重后的set
        """
        return set(map(lambda x: int(x) + 1, set(self.surfaceEle_Sequence().split(','))))

    def set_SurfaceEle_aerofoil(self):
        """
        :return:返回表面所有节点索引去重后的set
        """
        list_result = []
        for _str in self.surfaceEle_Sequence_aerofoil():
            list_result.append(set(map(lambda x: int(x) + 1, set(_str.split(',')))))
        return list_result

    def list_SurfaceEle(self):
        """
        :return:返回表面所有节点索引的list
        """
        return list(map(lambda x: int(x) + 1, self.surfaceEle_Sequence().split(',')))

    def list_SurfaceEle_aerofoil(self):
        """
        :return:返回表面所有节点索引去重后的set
        """
        list_result = []
        for _str in self.surfaceEle_Sequence_aerofoil():
            list_result.append(set(map(lambda x: int(x) + 1, set(_str.split(',')))))
        return list_result

    def surfaceEle_Real_Sequence(self, path_coord):
        """
        :param path_coord: 坐标数据文件
        :return:
        """
        set_surface_ele = self.set_SurfaceEle()
        list_surface_ele = self.list_SurfaceEle()
        coordfile = open(path_coord + 'NLIST.lis', 'rt')
        iCoord = 0  # 上述替换真实索引值(real_index_1、real_index_2...)的值
        # 存放所有坐标值的“从0开始的虚假索引”的字典
        # 结构为{real_index_1：[0,x,y,z],real_index_2:[1,x,y,z]...}
        # 其意图是用0,1...来替换real_index_1,real_index_2...
        dict_coord = {}
        for everyline in coordfile:
            list_everyline = everyline.split()
            everyline_index = int(list_everyline[0])
            if everyline_index in set_surface_ele:  # 根据element_data中set_surfaceEle方法返回的信息，只需表面点的坐标
                dict_coord[everyline_index] = iCoord  # 将对应点的真实编号和要更新的iCoord一一对应起来
                iCoord += 1
        # print(list_surface_ele)
        for i_ele in range(len(list_surface_ele)):  # 将排序好的表面点的索引值替换成更新后的0,1,2...索引
            if int(list_surface_ele[i_ele]) in dict_coord.keys():  # 如果list_ele中的索引是表面的点的索引，进行替换
                list_surface_ele[i_ele] = dict_coord[list_surface_ele[i_ele]]  # 获取字典dict_coord中的第一值替换list_ele
        # print('替换后:' + str(list_surface_ele))
        # 将真实索引值（real_index_12...）更新为[0,1...]返回
        coordfile.close()
        return list_surface_ele

    # def surfaceEle_Real_Sequence_aerofoil(self, path_coord):
    #     """
    #     :param path_coord: 坐标数据文件
    #     :return:
    #     """
    #     set_surface_ele_list = self.set_SurfaceEle_aerofoil()
    #     list_surface_ele_list = self.list_SurfaceEle_aerofoil()
    #
    #     coordfile = open(path_coord, 'rt')
    #     iCoord = 0  # 上述替换真实索引值(real_index_1、real_index_2...)的值
    #     # 存放所有坐标值的“从0开始的虚假索引”的字典
    #     # 结构为{real_index_1：[0,x,y,z],real_index_2:[1,x,y,z]...}
    #     # 其意图是用0,1...来替换real_index_1,real_index_2...
    #
    #     elements_str = coordfile.read()
    #     elements_list = elements_str.split("C")
    #     ele_result_list = []
    #     for ele_str in elements_list:
    #         ele_component_list = []
    #         temp_list = ele_str.strip().split("\n")
    #         for temp_list_child in temp_list:
    #             _list = temp_list_child.strip().split()
    #             ele_number = int(_list[0])
    #             node_1 = int(_list[1])
    #             node_2 = int(_list[2])
    #             node_3 = int(_list[3])
    #             node_4 = int(_list[4])
    #             node_5 = int(_list[5])
    #             node_6 = int(_list[6])
    #             node_7 = int(_list[7])
    #             node_8 = int(_list[8])
    #             ele_component_list.append(
    #                 [ele_number, node_1, node_2, node_3, node_4,
    #                  node_5, node_6, node_7, node_8])
    #         ele_result_list.append(ele_component_list)
    #
    #
    #     dict_coord = {}
    #     for everyline in coordfile:
    #         list_everyline = everyline.split()
    #         everyline_index = int(list_everyline[0])
    #         if everyline_index in set_surface_ele:  # 根据element_data中set_surfaceEle方法返回的信息，只需表面点的坐标
    #             dict_coord[everyline_index] = iCoord  # 将对应点的真实编号和要更新的iCoord一一对应起来
    #             iCoord += 1
    #     # print(list_surface_ele)
    #     for i_ele in range(len(list_surface_ele)):  # 将排序好的表面点的索引值替换成更新后的0,1,2...索引
    #         if int(list_surface_ele[i_ele]) in dict_coord.keys():  # 如果list_ele中的索引是表面的点的索引，进行替换
    #             list_surface_ele[i_ele] = dict_coord[list_surface_ele[i_ele]]  # 获取字典dict_coord中的第一值替换list_ele
    #     # print('替换后:' + str(list_surface_ele))
    #     # 将真实索引值（real_index_12...）更新为[0,1...]返回
    #     coordfile.close()
    #     return list_surface_ele


if __name__ == "__main__":
    # path_four_read = r"C:\Users\asus\Desktop\Demo_DT_Crane\APP_models\pulley\pre\ele\ELIST.lis"
    path_four_read = r"C:\Users\asus\Desktop\Demo_DT_Crane\APP_models\pulley\mid\element_surface_new.txt"
    ed = ElementData(path_four_read, ['2D4', '3D6'])
    # print(len(ed.allEle_Sequence()))
