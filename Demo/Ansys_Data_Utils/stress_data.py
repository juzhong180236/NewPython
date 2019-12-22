import os
import itertools
import printf as pf
import color_data as colord


class StressData(object):
    def __init__(self, path_stress=None, ed=None):
        self.path_stress = path_stress
        self.ed = ed

    def surface_Stress_Scolor(self):
        isExisted = os.path.exists(self.path_stress)
        if not isExisted:
            pf.printf(self.path_stress)
            pf.printf('上面列出的路径不存在，请设置正确路径！')
            return
        else:
            pf.printf('目录[' + self.path_stress + ']存在,正在读取...')
        files_stress = os.listdir(self.path_stress)  # 获取当前文档下的文件
        # files_stress.sort(key=lambda x: int(x[:-4]))
        files_stress.sort(key=lambda x: int(x[:-4]))
        float_Scolor_step, float_Scolor_min = colord.color_Step(files_stress, self.path_stress, 's')  # 获取step

        set_surface_ele = self.ed.set_SurfaceEle()

        i_processing = 0
        str_Scolor_allFile = ''
        str_stress_allFile = ''
        for file in files_stress:  # 遍历文件夹
            list_Scolor = []
            if not os.path.isdir(file):  # 判断是否是文件夹，不是文件夹才打开
                filename = os.path.basename(file)  # 返回文件名
                fullpath = self.path_stress + filename  # 得到文件夹中每个文件的完整路径
                infile = open(fullpath, 'rt')  # 以文本形式读取文件
                i_line = 0
                for line in infile:
                    if i_line == 1:
                        line_index = int(line.split('\t')[0])
                        if line_index in set_surface_ele:

                            list_Scolor.append(line.split('\t')[1].rstrip('\n'))  # 将每一行以制表符分开后加入到list_Scolor序列中
                    i_line = 1
                infile.close()
            list_Scolor_result = map(colord.define_Color, map(float, list_Scolor),
                                     itertools.repeat(float_Scolor_min),
                                     itertools.repeat(float_Scolor_step))

            i_processing += 1
            print("\r程序当前已完成：" + str(round(i_processing / len(files_stress) * 100)) + '%', end="")
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
        files_stress = os.listdir(self.path_stress)  # 获取当前文档下的文件
        # files_stress.sort(key=lambda x: int(x[:-4]))
        files_stress.sort(key=lambda x: int(x[:-4]))
        float_Scolor_step, float_Scolor_min = colord.color_Step(files_stress, self.path_stress, 's')  # 获取step

        set_surface_ele = self.ed.set_SurfaceEle()

        i_processing = 0
        str_Scolor_allFile = ''
        str_stress_allFile = ''
        for file in files_stress:  # 遍历文件夹
            list_Scolor = []
            if not os.path.isdir(file):  # 判断是否是文件夹，不是文件夹才打开
                filename = os.path.basename(file)  # 返回文件名
                fullpath = self.path_stress + filename  # 得到文件夹中每个文件的完整路径
                infile = open(fullpath, 'rt')  # 以文本形式读取文件
                i_line = 0
                for line in infile:
                    if i_line == 1:
                        line_index = int(line.split('\t')[0])
                        if line_index in set_surface_ele:
                            list_Scolor.append(
                                [str(line_index), line.split('\t')[1].rstrip('\n')])  # 将每一行以制表符分开后加入到list_Scolor序列中
                    i_line = 1
                infile.close()

            list_Scolor = sorted(list_Scolor, key=lambda x: int(x[0]))
            length_Bysorted = len(list_Scolor)
            list_Scolor_Bysort = []
            for i in range(0, length_Bysorted):
                list_Scolor_Bysort.append(list_Scolor[i][1])
            list_Scolor_result = map(colord.define_Color, map(float, list_Scolor_Bysort),
                                     itertools.repeat(float_Scolor_min),
                                     itertools.repeat(float_Scolor_step))
            str_Scolor_allFile += ','.join(map(str, list_Scolor_result)) + '\n'  # 以逗号为分隔符来组成字符串,并在最后添加换行符,以换行符区分每个文件的信息
            str_stress_allFile += ','.join(list_Scolor_Bysort) + '\n'
            i_processing += 1
            print("\r程序当前已完成：" + str(round(i_processing / len(files_stress) * 100)) + '%', end="")

        str_Scolor_allFile += str(float_Scolor_step * 21 / 9)
        return str_stress_allFile.rstrip('\n'), str_Scolor_allFile, str(float_Scolor_step) + ',' + str(float_Scolor_min)
