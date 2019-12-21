import os
import printf as pf


class ElementData(object):
    def __init__(self, path_ele=None, geometry_type=None):
        self.path_ele = path_ele + 'ELIST.lis'
        self.geometry_type = geometry_type
        pass

    def aa(self):
        return self.__allEle_To_List()

    # 【输入int,str】：ELIST.lis文件中是四面体节点输入4，六面体节点输入6，第二个参数为ELIST.lis的路径
    # 【输出str】：返回以逗号隔开的可绘制模型表面的排列好的索引值字符串(string)
    # 【功能】：对四面体或六面体的ELIST.lis进行简化，使其只有表面点的信息，极大减少数据量
    def __allEle_To_List(self):
        TETRAHEDRON = '3D4'
        HEXAHEDRON = '3D6'
        TETRAHEDRAL_SHEET = '2D4'
        isExisted = os.path.exists(self.path_ele)
        if not isExisted:
            pf.printf(self.path_ele)
            pf.printf('上面列出的路径不存在，请设置正确路径！')
            return
        else:
            pf.printf('文件[' + self.path_ele[len(self.path_ele) - self.path_ele[::-1].index('\\'):] + ']存在,正在读取...')
        eleFile = open(self.path_ele, "rt")
        list_result = []

        for everyline in eleFile:
            list_everyline = everyline.split()
            if list_everyline and list_everyline[0].isdigit():
                # 只type为1的元素索引，在都为四面体的网格中起作用
                if len(self.geometry_type) == 1 and TETRAHEDRON in self.geometry_type and not list_everyline[1] == '1':
                    continue
                # 取每一行第6个到最后一个的元素
                list_cut = list_everyline[6:]
                # list_cut为空或者首个字符不是纯数字构成的字符串,直接跳过该行
                # if not list_cut or not list_cut[0].isdigit() or list_cut.count('0') > 1:
                #     print(list_cut)
                if not list_cut or not list_cut[0].isdigit():
                    # if not list_cut:
                    continue
                for ele in list_cut[::-1]:  # 反序遍历
                    if not ele.isdigit() or ele == '0':
                        list_cut.remove(ele)
                list_temp = list(map(int, list_cut))
                # if list_everyline[0] == '1':
                #     print(list_temp)
                if len(list_temp) == 8:
                    if TETRAHEDRON in self.geometry_type:
                        # 所有的ele【前4位】排列为【四面体】的画图形式，得到这些值并存在list_result中
                        list_result.extend([list_temp[0] - 1, list_temp[1] - 1, list_temp[2] - 1,
                                            list_temp[1] - 1, list_temp[2] - 1, list_temp[3] - 1,
                                            list_temp[0] - 1, list_temp[2] - 1, list_temp[3] - 1,
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
        eleFile.close()
        pf.printf('文件[' + self.path_ele[len(self.path_ele) - self.path_ele[::-1].index('\\'):] + ']读取完成！')
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
        list_sort = []
        for i in range(0, len(list_allEle), 3):
            list_temp = [list_allEle[i], list_allEle[i + 1], list_allEle[i + 2]]
            list_temp.sort(key=lambda x: x)
            list_sort.append(str(list_temp[0]) + ',' + str(list_temp[1]) + ',' + str(list_temp[2]))
        # 直接使用set对相同的顺序单面索引组只保留一个，即对画多次的表面只画一次
        # 这一步使内部面片不用画两次了，但是还是会画一次
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
        list_sort = []
        for key, value in dict_sort.items():
            if value == 1:
                list_sort.append(key)
        # 返回逗号隔开的索引值字符串
        return ','.join(list_sort)

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

    def list_SurfaceEle(self):
        """
        :return:返回表面所有节点索引的list
        """
        return list(map(lambda x: int(x) + 1, self.surfaceEle_Sequence().split(',')))

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
            if len(everyline) == 76:
                everyline_index = int(everyline[0:9].strip())
                if everyline_index in set_surface_ele:  # 根据element_data中set_surfaceEle方法返回的信息，只需表面点的坐标
                    dict_coord[everyline_index] = iCoord  # 将对应点的真实编号和要更新的iCoord一一对应起来
                    iCoord += 1
        for i_ele in range(len(list_surface_ele)):  # 将排序好的表面点的索引值替换成更新后的0,1,2...索引
            if int(list_surface_ele[i_ele]) in dict_coord.keys():  # 如果list_ele中的索引是表面的点的索引，进行替换
                # print(list_ele[iEle])
                list_surface_ele[i_ele] = dict_coord[list_surface_ele[i_ele]]  # 获取字典dict_coord中的第一值替换list_ele
                # print('替换后:' + list_ele[iEle])
        # 将真实索引值（real_index_12...）更新为[0,1...]返回
        coordfile.close()
        return ','.join(map(str, list_surface_ele))


if __name__ == "__main__":
    # path_four_read = r"C:\Users\asus\Desktop\Demo_DT_Crane\APP_models\pulley\pre\ele\ELIST.lis"
    path_four_read = r"C:\Users\asus\Desktop\Demo_DT_Crane\APP_models\pulley\mid\element_surface_new.txt"
    ed = ElementData(path_four_read, ['2D4', '3D6'])
    # print(len(ed.allEle_Sequence()))
