import os
import itertools
import Demo.Ansys_Data_Utils_2021.print_f as pf
import Demo.Ansys_Data_Utils_2021.color_data as colord


class StressData(object):
    def __init__(self, path_stress=None, ed=None):
        self.path_stress = path_stress
        self.ed = ed

    """
    2020.12.14 新增的Beam188单元的应力导出程序
    """

    def allStress_To_Str_Beam188(self):
        isExisted = os.path.exists(self.path_stress)
        if not isExisted:
            pf.printf(self.path_stress)
            pf.printf('上面列出的路径不存在，请设置正确路径！')
            return
        else:
            pf.printf('目录[' + self.path_stress + ']存在,正在读取...')
        """
        2020.12.19 从其他程序移植两个功能：
        1、自动删除"file0.page", "file1.page"
        2、对中间加了横杠的文件进行排序
        """
        files = os.listdir(self.path_stress)  # 获取当前文档下的文件
        abandon_files = ["file0.page", "file1.page"]
        for file in files:
            file_name = os.path.basename(file)
            if file_name in abandon_files:
                os.remove(self.path_stress + file_name)
        files_stress = os.listdir(self.path_stress)  # 获取当前文档下的文件
        # files_stress.sort(key=lambda x: int(x[:-4]))
        # 先按照文件名的第二个数字排列
        files_cut_sorted_1 = sorted(files_stress, key=lambda x: int(x[:-4].split('_')[1]))
        # 再按照文件名的第一个数字排列
        files_cut_sorted_2 = sorted(files_cut_sorted_1, key=lambda x: int(x[:-4].split('_')[0]))

        float_Scolor_step, float_Scolor_min = colord.color_Step(files_cut_sorted_2, self.path_stress, 's')  # 获取step

        i_processing = 0
        str_Scolor_allFile = ''
        str_stress_allFile = ''
        for file in files_cut_sorted_2:  # 遍历文件夹
            list_Scolor = []
            if not os.path.isdir(file):  # 判断是否是文件夹，不是文件夹才打开
                filename = os.path.basename(file)  # 返回文件名
                fullpath = self.path_stress + filename  # 得到文件夹中每个文件的完整路径
                infile = open(fullpath, 'rt')  # 以文本形式读取文件
                for line in infile:
                    list_everyline = line.split()
                    list_Scolor.append(list_everyline[1].strip())  # 将每一行以制表符分开后加入到list_Scolor序列中
                infile.close()
            list_Scolor_result = map(colord.define_Color, map(float, list_Scolor),
                                     itertools.repeat(float_Scolor_min),
                                     itertools.repeat(float_Scolor_step))

            i_processing += 1
            print("\r应力信息读取程序当前已完成：" + str(round(i_processing / len(files_cut_sorted_2) * 100)) + '%', end="")
            str_Scolor_allFile += ','.join(map(str, list_Scolor_result)) + '\n'  # 以逗号为分隔符来组成字符串,并在最后添加换行符,以换行符区分每个文件的信息
            str_stress_allFile += ','.join(list_Scolor) + '\n'

        str_Scolor_allFile += str(float_Scolor_step * 21 / 9)
        return str_stress_allFile.rstrip('\n'), str_Scolor_allFile, float_Scolor_step, float_Scolor_min

    def surface_Stress_Scolor(self):
        isExisted = os.path.exists(self.path_stress)
        if not isExisted:
            pf.printf(self.path_stress)
            pf.printf('上面列出的路径不存在，请设置正确路径！')
            return
        else:
            pf.printf('目录[' + self.path_stress + ']存在,正在读取...')
        """
        2020.12.19 从其他程序移植两个功能：
        1、自动删除"file0.page", "file1.page"
        2、对中间加了横杠的文件进行排序
        """
        files = os.listdir(self.path_stress)  # 获取当前文档下的文件
        abandon_files = ["file0.page", "file1.page"]
        for file in files:
            file_name = os.path.basename(file)
            if file_name in abandon_files:
                os.remove(self.path_stress + file_name)
        files_stress = os.listdir(self.path_stress)  # 获取当前文档下的文件
        # files_stress.sort(key=lambda x: int(x[:-4]))
        # 先按照文件名的第二个数字排列
        files_cut_sorted_1 = sorted(files_stress, key=lambda x: int(x[:-4].split('_')[1]))
        # 再按照文件名的第一个数字排列
        files_cut_sorted_2 = sorted(files_cut_sorted_1, key=lambda x: int(x[:-4].split('_')[0]))
        float_Scolor_step, float_Scolor_min = colord.color_Step(files_cut_sorted_2, self.path_stress, 's')  # 获取step

        set_surface_ele = self.ed.surface_int_set()

        i_processing = 0
        str_Scolor_allFile = ''
        str_stress_allFile = ''
        for file in files_cut_sorted_2:  # 遍历文件夹
            list_Scolor = []
            if not os.path.isdir(file):  # 判断是否是文件夹，不是文件夹才打开
                filename = os.path.basename(file)  # 返回文件名
                fullpath = self.path_stress + filename  # 得到文件夹中每个文件的完整路径
                infile = open(fullpath, 'rt')  # 以文本形式读取文件
                for line in infile:
                    list_everyline = line.split()
                    line_index = int(list_everyline[0])
                    if line_index in set_surface_ele:
                        list_Scolor.append(list_everyline[1].strip())  # 将每一行以制表符分开后加入到list_Scolor序列中

                infile.close()
            list_Scolor_result = map(colord.define_Color, map(float, list_Scolor),
                                     itertools.repeat(float_Scolor_min),
                                     itertools.repeat(float_Scolor_step))

            i_processing += 1
            print("\r应力信息读取程序当前已完成：" + str(round(i_processing / len(files_cut_sorted_2) * 100)) + '%', end="")
            str_Scolor_allFile += ','.join(map(str, list_Scolor_result)) + '\n'  # 以逗号为分隔符来组成字符串,并在最后添加换行符,以换行符区分每个文件的信息
            str_stress_allFile += ','.join(list_Scolor) + '\n'

        str_Scolor_allFile += str(float_Scolor_step * 21 / 9)
        return str_stress_allFile.rstrip('\n'), str_Scolor_allFile, str(float_Scolor_step) + ',' + str(float_Scolor_min)

    def surface_Stress_Scolor_Bysorted(self):
        isExisted = os.path.exists(self.path_stress)
        if not isExisted:
            pf.printf(self.path_stress)
            pf.printf('上面列出的路径不存在，请设置正确路径！')
            return
        else:
            pf.printf('目录[' + self.path_stress + ']存在,正在读取...')
        files = os.listdir(self.path_stress)  # 获取当前文档下的文件
        abandon_files = ["file0.page", "file1.page"]
        for file in files:
            file_name = os.path.basename(file)
            if file_name in abandon_files:
                os.remove(self.path_stress + file_name)
        files_stress = os.listdir(self.path_stress)  # 获取当前文档下的文件
        # files_stress.sort(key=lambda x: int(x[:-4]))
        # 先按照文件名的第二个数字排列
        files_cut_sorted_1 = sorted(files_stress, key=lambda x: int(x[:-4].split('_')[1]))
        # 再按照文件名的第一个数字排列
        files_cut_sorted_2 = sorted(files_cut_sorted_1, key=lambda x: int(x[:-4].split('_')[0]))
        float_Scolor_step, float_Scolor_min = colord.color_Step(files_cut_sorted_2, self.path_stress, 's')  # 获取step

        set_surface_ele = self.ed.surface_int_set()

        i_processing = 0
        str_Scolor_allFile = ''
        str_stress_allFile = ''
        for file in files_cut_sorted_2:  # 遍历文件夹
            list_Scolor = []
            if not os.path.isdir(file):  # 判断是否是文件夹，不是文件夹才打开
                filename = os.path.basename(file)  # 返回文件名
                fullpath = self.path_stress + filename  # 得到文件夹中每个文件的完整路径
                infile = open(fullpath, 'rt')  # 以文本形式读取文件
                for line in infile:
                    list_everyline = line.split()
                    line_index = int(list_everyline[0])
                    if line_index in set_surface_ele:
                        list_Scolor.append(
                            [str(line_index), list_everyline[1].strip()])  # 将每一行以制表符分开后加入到list_Scolor序列中

                infile.close()
            list_Scolor = sorted(list_Scolor, key=lambda x: int(x[0]))
            # print(list_Scolor)
            # 有重复的应力
            list_test = []
            for ele in list_Scolor[::-1]:
                if ele[0] in list_test:
                    list_Scolor.remove(ele)
                list_test.append(ele[0])
            length_Bysorted = len(list_Scolor)
            list_Scolor_Bysort = []
            for i in range(0, length_Bysorted):
                list_Scolor_Bysort.append(list_Scolor[i][1])
            # print(list_Scolor_Bysort)
            list_Scolor_result = map(colord.define_Color, map(float, list_Scolor_Bysort),
                                     itertools.repeat(float_Scolor_min),
                                     itertools.repeat(float_Scolor_step))
            str_Scolor_allFile += ','.join(map(str, list_Scolor_result)) + '\n'  # 以逗号为分隔符来组成字符串,并在最后添加换行符,以换行符区分每个文件的信息
            str_stress_allFile += ','.join(list_Scolor_Bysort) + '\n'
            i_processing += 1
            print("\r应力信息读取程序当前已完成：" + str(round(i_processing / len(files_cut_sorted_2) * 100)) + '%', end="")

        str_Scolor_allFile += str(float_Scolor_step * 21 / 9)
        return str_stress_allFile.rstrip('\n'), str_Scolor_allFile, float_Scolor_step, float_Scolor_min
