import os
import itertools
import printf as pf
import color_data as colord


class DispalcementData(object):
    def __init__(self, path_displacement=None, ed=None, cd=None):
        self.path_displacement = path_displacement
        self.ed = ed
        self.cd = cd

    #  ele,coords,dcolor
    # 【输入str,str,set】：NLIST.lis和displacement所在的文件夹；surface上排序好的索引值的str；经过set取唯一值的surface索引的set
    # 【输出tuple】：返回tuple的第一个元素是所有姿态的坐标值str，第二个元素是更新为0,1,2...后的索引值，第三个元素是根据位移值得到的颜色值字符串
    # 【功能】：根据排序好的surface上的索引值，提取出对应在displacement和NLIST.lis中的各姿态坐标值，以及将索引更新为Three.js识别的从0开始的索引，
    def surface_DopCoords_DopSum_Dcolor(self):
        isExisted = os.path.exists(self.path_displacement)
        if not isExisted:
            pf.printf(self.path_displacement)
            pf.printf('上面列出的路径不存在，请设置正确路径！')
            return
        else:
            pf.printf('目录[' + self.path_displacement + ']存在,正在读取...')
        files = os.listdir(self.path_displacement)  # 获取当前文档下的文件
        # files_cut = sorted(files[0:-1], key=lambda x: int(x[:-4]))
        files_cut = sorted(files[0:-1], key=lambda x: int(x))
        float_Dcolor_step, float_Dcolor_min = colord.color_Step(files_cut, self.path_displacement, 'd')  # 获取step

        list_coords = self.cd.surfaceCoord_To_List()  # 获取xyz坐标信息
        set_surface_ele = self.ed.set_SurfaceEle()

        i_processing = 1  # 遍历到第i个文件
        str_coords_allFile = ''  # 不带初始坐标信息
        str_Dcolor_allFile = ''
        str_displacementSum_allFile = ''
        for file in files_cut:  # 遍历文件夹
            list_sort = []  # 存放加上位移后的所有坐标值的list
            list_Dcolor = []
            if not os.path.isdir(file):  # 判断是否是文件夹，不是文件夹才打开
                filename = os.path.basename(file)  # 返回文件名
                fullpath_input = self.path_displacement + filename  # 得到文件夹中每个文件的完整路径
                infile = open(fullpath_input, 'rt')  # 以文本形式读取文件
                iCount = 0  # 上述初始的坐标值的list_coords中的索引，每3个一组
                for line in infile:
                    if len(line) == 62:
                        line_index = int(line[0:9].strip())  # 获取节点编号
                        if line_index in set_surface_ele:  # 如果该点是表面点和位移运算得到点的最终坐标
                            list_sort.append(str(float(line[9:22].strip()) + float(list_coords[iCount])))
                            list_sort.append(str(float(line[22:35].strip()) + float(list_coords[iCount + 1])))
                            list_sort.append(str(float(line[35:48].strip()) + float(list_coords[iCount + 2])))
                            list_Dcolor.append(line[49:61].strip())  # 将位移之和的值传入数组
                            iCount += 3
                infile.close()
            list_Dcolor_result = map(colord.define_Color, map(float, list_Dcolor),
                                     itertools.repeat(float_Dcolor_min),
                                     itertools.repeat(float_Dcolor_step))
            str_Dcolor_allFile += ','.join(map(str, list_Dcolor_result)) + '\n'

            str_displacementSum_allFile += ','.join(list_Dcolor) + '\n'

            str_coords_allFile += ','.join(list_sort) + '\n'  # 以逗号为分隔符来组成字符串,并在最后添加换行符,以换行符区分每个文件的信息
            print("\r位移信息读取程序当前已完成：" + str(round(i_processing / len(files_cut) * 100)) + '%', end="")
            i_processing += 1
        str_Dcolor_allFile += str(float_Dcolor_step * 21 / 9)
        # print(str_coords_allFile.rstrip('\n'))
        return str_coords_allFile.rstrip('\n'), str_displacementSum_allFile.rstrip('\n'), str_Dcolor_allFile, str(
            float_Dcolor_step) + ',' + str(float_Dcolor_min)

    def surface_Displacement_DopSum_Dcolor(self):
        isExisted = os.path.exists(self.path_displacement)
        if not isExisted:
            pf.printf(self.path_displacement)
            pf.printf('上面列出的路径不存在，请设置正确路径！')
            return
        else:
            pf.printf('目录[' + self.path_displacement + ']存在,正在读取...')
        files = os.listdir(self.path_displacement)  # 获取当前文档下的文件
        # files_cut = sorted(files[0:-1], key=lambda x: int(x[:-4]))
        files_cut = sorted(files[0:-1], key=lambda x: int(x))
        float_Dcolor_step, float_Dcolor_min = colord.color_Step(files_cut, self.path_displacement, 'd')  # 获取step

        set_surface_ele = self.ed.set_SurfaceEle()

        i_processing = 1  # 遍历到第i个文件
        str_displacementXYZ_allFile = ''  # 不带初始坐标信息
        str_Dcolor_allFile = ''
        str_displacementSum_allFile = ''
        for file in files_cut:  # 遍历文件夹
            list_sort = []  # 存放加上位移后的所有坐标值的list
            list_Dcolor = []
            if not os.path.isdir(file):  # 判断是否是文件夹，不是文件夹才打开
                filename = os.path.basename(file)  # 返回文件名
                fullpath_input = self.path_displacement + filename  # 得到文件夹中每个文件的完整路径
                infile = open(fullpath_input, 'rt')  # 以文本形式读取文件
                iCount = 0  # 上述初始的坐标值的list_coords中的索引，每3个一组
                for line in infile:
                    if len(line) == 62:
                        line_index = int(line[0:9].strip())  # 获取节点编号
                        if line_index in set_surface_ele:  # 如果该点是表面点和位移运算得到点的最终坐标
                            list_sort.extend([line[9:22].strip(),line[22:35].strip(),line[35:48].strip()])
                            list_Dcolor.append(line[49:61].strip())  # 将位移之和的值传入数组
                            iCount += 3
                infile.close()
            list_Dcolor_result = map(colord.define_Color, map(float, list_Dcolor),
                                     itertools.repeat(float_Dcolor_min),
                                     itertools.repeat(float_Dcolor_step))
            str_Dcolor_allFile += ','.join(map(str, list_Dcolor_result)) + '\n'

            str_displacementSum_allFile += ','.join(list_Dcolor) + '\n'
            str_displacementXYZ_allFile += ','.join(list_sort) + '\n'  # 以逗号为分隔符来组成字符串,并在最后添加换行符,以换行符区分每个文件的信息
            print("\r位移信息读取程序当前已完成：" + str(round(i_processing / len(files_cut) * 100)) + '%', end="")
            i_processing += 1
        str_Dcolor_allFile += str(float_Dcolor_step * 21 / 9)
        # print(str_coords_allFile.rstrip('\n'))
        return str_displacementXYZ_allFile.rstrip('\n'), str_displacementSum_allFile.rstrip('\n'), str_Dcolor_allFile, str(
            float_Dcolor_step) + ',' + str(float_Dcolor_min)
