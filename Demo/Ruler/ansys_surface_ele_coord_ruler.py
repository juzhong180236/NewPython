# 【程序介绍】点的索引值和坐标值数据清洗
# 缩小点的索引值数据所在文件的大小，前一道程序先用javascript写的，后期改到python中
import os
import itertools

path_switch = "has_dut_35"
# 读取路径@@@@@@@@@@@@@@@@@@@@@(读pre)
path_four = "C:/Users/asus/Desktop/DT_DEMO/new_models/" + path_switch + "/pre/"
# '''四面体ELIST.lis路径'''
path_ele_four = "C:/Users/asus/Desktop/DT_DEMO/new_models/" + path_switch + "/pre/ele/ELIST.lis"

# 读取路径@@@@@@@@@@@@@@@@@@@@@(读pre)
# path_four = r"C:\Users\asus\Desktop\History\History_codes\DT_Origin_Demo\APP_A_CantileverBeam\APP_models\list_new\pre\\"
# '''四面体ELIST.lis路径'''
# path_ele_four = r"C:\Users\asus\Desktop\History\History_codes\DT_Origin_Demo\APP_A_CantileverBeam\APP_models\list_new\pre\ele\ELIST.lis"

path_hex = "C:/Users/asus/Desktop/DT_DEMO/new_models/" + path_switch + "/pre/"
'''六面体ELIST.lis路径'''
path_ele_hex = "C:/Users/asus/Desktop/DT_DEMO/new_models/" + path_switch + "/pre/ele/ELIST.lis"


# 【输入str，str】：生成的文件名，需要写入txt的文本数据
# 【功能】：创建一个txt文件
def Text_Create(name, msg, hexOrfour):
    # 存储路径@@@@@@@@@@@@@@@@@@@@@@@(存mid)
    save_path = "C:/Users/asus/Desktop/DT_DEMO/new_models/"
    # save_path = path_four
    if hexOrfour == 'four':
        # 存储路径@@@@@@@@@@@@@@@@@@@@@@@(存mid)
        save_path += path_switch + '/mid/'
        # save_path = path_four
    elif hexOrfour == 'hex':
        # save_path += 'new_utils/post/'
        save_path += path_switch + '/mid/'
    full_path = save_path + name + '.txt'  # 也可以创建一个.doc的word文档
    # 创建写入的文档
    file = open(full_path, 'w')
    file.write(msg)
    file.close()


def colorStep(input, pressureStep, i):
    return input + pressureStep * i


def defineColor(array_ele, list_min_ele, pressureStep):
    if array_ele < colorStep(list_min_ele, pressureStep, 1):
        colors = '0,0,1'
    elif colorStep(list_min_ele, pressureStep, 1) <= array_ele < colorStep(list_min_ele, pressureStep, 2):
        colors = '0,' + str(42 / 255) + ',1'
    elif colorStep(list_min_ele, pressureStep, 2) <= array_ele < colorStep(list_min_ele, pressureStep, 3):
        colors = '0,' + str(85 / 255) + ',1'
    elif colorStep(list_min_ele, pressureStep, 3) <= array_ele < colorStep(list_min_ele, pressureStep, 4):
        colors = '0,' + str(127 / 255) + ',1'
    elif colorStep(list_min_ele, pressureStep, 4) <= array_ele < colorStep(list_min_ele, pressureStep, 5):
        colors = '0,' + str(170 / 255) + ',1'
    elif colorStep(list_min_ele, pressureStep, 5) <= array_ele < colorStep(list_min_ele, pressureStep, 6):
        colors = '0,1,1'
    elif colorStep(list_min_ele, pressureStep, 6) <= array_ele < colorStep(list_min_ele, pressureStep, 7):
        colors = '0,1,' + str(170 / 255)
    elif colorStep(list_min_ele, pressureStep, 7) <= array_ele < colorStep(list_min_ele, pressureStep, 8):
        colors = '0,1,' + str(127 / 255)
    elif colorStep(list_min_ele, pressureStep, 8) <= array_ele < colorStep(list_min_ele, pressureStep, 9):
        colors = '0,1,' + str(85 / 255)
    elif colorStep(list_min_ele, pressureStep, 9) <= array_ele < colorStep(list_min_ele, pressureStep, 10):
        colors = '0,1,' + str(42 / 255)
    elif colorStep(list_min_ele, pressureStep, 10) <= array_ele < colorStep(list_min_ele, pressureStep, 11):
        colors = '0,1,0'
    elif colorStep(list_min_ele, pressureStep, 11) <= array_ele < colorStep(list_min_ele, pressureStep, 12):
        colors = str(42 / 255) + ',1,0'
    elif colorStep(list_min_ele, pressureStep, 12) <= array_ele < colorStep(list_min_ele, pressureStep, 13):
        colors = str(85 / 255) + ',1,0'
    elif colorStep(list_min_ele, pressureStep, 13) <= array_ele < colorStep(list_min_ele, pressureStep, 14):
        colors = str(127 / 255) + ',1,0'
    elif colorStep(list_min_ele, pressureStep, 14) <= array_ele < colorStep(list_min_ele, pressureStep, 15):
        colors = str(170 / 255) + ',1,0'
    elif colorStep(list_min_ele, pressureStep, 15) <= array_ele < colorStep(list_min_ele, pressureStep, 16):
        colors = '1,1,0'
    elif colorStep(list_min_ele, pressureStep, 16) <= array_ele < colorStep(list_min_ele, pressureStep, 17):
        colors = '1,' + str(170 / 255) + ',0'
    elif colorStep(list_min_ele, pressureStep, 17) <= array_ele < colorStep(list_min_ele, pressureStep, 18):
        colors = '1,' + str(127 / 255) + ',0'
    elif colorStep(list_min_ele, pressureStep, 18) <= array_ele < colorStep(list_min_ele, pressureStep, 19):
        colors = '1,' + str(85 / 255) + ',0'
    elif colorStep(list_min_ele, pressureStep, 19) <= array_ele < colorStep(list_min_ele, pressureStep, 20):
        colors = '1,' + str(42 / 255) + ',0'
    elif colorStep(list_min_ele, pressureStep, 20) <= array_ele <= colorStep(list_min_ele, pressureStep, 21):
        colors = '1,0,0'
    else:
        colors = '1,0,0'
    return colors


# 【输入list】：排列好的能画出四面体或六面体的索引的列表（list）
# 【输出str】：返回以逗号隔开的可绘制模型表面的排列好的索引值字符串(string)
# 【功能】：每三个相连索引为一组，所有只出现一次的索引组所构成的字符串
def Str_Remove_SameEle(list_input):
    list_sort = []
    for i in range(0, len(list_input), 3):
        list_temp = [int(list_input[i]), int(list_input[i + 1]), int(list_input[i + 2])]
        list_temp.sort(key=lambda x: x)
        list_sort.append(str(list_temp[0]) + ',' + str(list_temp[1]) + ',' + str(list_temp[2]))
    set_sort = set(list_sort)
    dict_sort = {}
    for arr_ele in list_sort:
        dict_sort[arr_ele] = 0
        # 列表list_sort中的某元素所重复的次数,初始次数为0
    for arr_ele in list_sort:
        if arr_ele in set_sort:
            dict_sort[arr_ele] += 1  # 如果检测到元素一次，就加1
    list_sort = []
    for key, value in dict_sort.items():
        if value == 1:
            list_sort.append(key)
    return ','.join(list_sort)


# 【输入str】：将ELIST.lis文件中每一行以多个空格隔开的一行字符串作为输入
# 【输出list】：将ELIST.lis中一行的元素转为list
# 【功能】：去除每行数据中多余的空格，返回只有元素的list
def Text_PerLine_ToList(str_input):
    list_str = str_input.strip().split(" ")
    list_temp = []
    for i in range(len(list_str)):
        if list_str[i] != "":
            list_temp.append(int(list_str[i]))
    return list_temp


# 【输入int,str】：ELIST.lis文件中是四面体节点输入4，六面体节点输入6，第二个参数为ELIST.lis的路径
# 【输出str】：返回以逗号隔开的可绘制模型表面的排列好的索引值字符串(string)
# 【功能】：对四面体或六面体的ELIST.lis进行简化，使其只有表面点的信息，极大减少数据量
def Str_SurfaceEle(geometry_faceNumber, path_input):
    eleFile = open(path_input, "rt")
    list_result = []
    for everyline in eleFile:
        if len(everyline) >= 78:
            list_temp = Text_PerLine_ToList(everyline)
            if len(list_temp) == 14:
                if geometry_faceNumber == 4:
                    if list_temp[1] == 1:
                        # 所有的ele【前4位】排列为【四面体】的画图形式，得到这些值并存在list_result中
                        list_result.extend([list_temp[6] - 1, list_temp[7] - 1, list_temp[8] - 1,
                                            list_temp[7] - 1, list_temp[8] - 1, list_temp[9] - 1,
                                            list_temp[6] - 1, list_temp[8] - 1, list_temp[9] - 1,
                                            list_temp[6] - 1, list_temp[7] - 1, list_temp[9] - 1])
                elif geometry_faceNumber == 6:
                    if list_temp[1] == 1:
                        # 所有的ele【前8位】排列为【六面体】的画图形式，得到这些值并存在list_result中
                        list_result.extend(
                            [list_temp[6] - 1, list_temp[7] - 1, list_temp[8] - 1,
                             list_temp[6] - 1, list_temp[8] - 1, list_temp[9] - 1,
                             list_temp[10] - 1, list_temp[11] - 1, list_temp[12] - 1,
                             list_temp[10] - 1, list_temp[12] - 1, list_temp[13] - 1,
                             list_temp[6] - 1, list_temp[9] - 1, list_temp[13] - 1,
                             list_temp[6] - 1, list_temp[10] - 1, list_temp[13] - 1,
                             list_temp[7] - 1, list_temp[11] - 1, list_temp[12] - 1,
                             list_temp[7] - 1, list_temp[8] - 1, list_temp[12] - 1,
                             list_temp[6] - 1, list_temp[10] - 1, list_temp[11] - 1,
                             list_temp[6] - 1, list_temp[7] - 1, list_temp[11] - 1,
                             list_temp[8] - 1, list_temp[9] - 1, list_temp[13] - 1,
                             list_temp[8] - 1, list_temp[12] - 1, list_temp[13] - 1])
    result = Str_Remove_SameEle(list_result)
    eleFile.close()
    return result


# 541 516 214 261 845 856 762 324 348 763 738 786 六面体索引顺序

# text_create('ele_surface_new', result)

str_surface_ele_four = Str_SurfaceEle(4, path_ele_four)

str_surface_ele_hex = Str_SurfaceEle(6, path_ele_hex)


def addOne(x):
    return int(x) + 1


set_surface_ele_four = set(map(addOne, set(str_surface_ele_four.split(','))))

set_surface_ele_hex = set(map(addOne, set(str_surface_ele_hex.split(','))))


# 【输入str,str】：displacement或stress所在的文件夹路径；取最小值还是最大值，min，max
# 【输出float】：返回最小值或最大值
# 【功能】：将displacement或stress中最小的和最大的输出
def Str_Color_Step(path_input, min_or_max, stress_or_displacement):
    list_color_ToStep = []
    file = open(path_input, 'rt')
    for line in file:
        if stress_or_displacement == 's':
            list_color_ToStep.append(line.split('\t')[1])
        elif stress_or_displacement == 'd':
            if len(line) == 62:
                list_color_ToStep.append(line[49:61].strip())
    if stress_or_displacement == 's':
        list_color_ToStep.pop(0)
    list_color_ToStep_sorted = sorted(list_color_ToStep, key=lambda x: float(x))
    if min_or_max == 'min':
        return list_color_ToStep_sorted[0]
    elif min_or_max == 'max':
        # return list_color_ToStep_sorted[len(list_color_ToStep_sorted) - 1]
        return list_color_ToStep_sorted[-1]
    else:
        pass


#  ele,coords,dcolor
# 【输入str,str,set】：NLIST.lis和displacement所在的文件夹；surface上排序好的索引值的str；经过set取唯一值的surface索引的set
# 【输出tuple】：返回tuple的第一个元素是所有姿态的坐标值str，第二个元素是更新为0,1,2...后的索引值，第三个元素是根据位移值得到的颜色值字符串
# 【功能】：根据排序好的surface上的索引值，提取出对应在displacement和NLIST.lis中的各姿态坐标值，以及将索引更新为Three.js识别的从0开始的索引，
def Tuple_Surface_Coords_Ele_Dcolor(path_input, str_surface_ele, set_surface_ele):
    isExisted = os.path.exists(path_input)  # 打开读取的文档
    if not isExisted:
        os.makedirs(path_input)  # 如果不存在则创建目录
        print(path_input + ' 创建成功')
    else:
        print(path_input + ' 目录已存在')  # 如果目录存在则不创建，并提示目录已存在
    files = os.listdir(path_input)  # 获取当前文档下的文件
    files_cut = sorted(files[0:-1], key=lambda x: int(x[:-4]))
    list_coords = []  # 获取该文件夹下面的节点初始的坐标数据
    list_coords_x = []  # RBF的Coords中的x坐标
    coordfile = open(path_input + "NLIST.lis", 'rt')
    for everyline in coordfile:
        if len(everyline) == 76:
            everyline_index = int(everyline[0:9].strip())
            if everyline_index in set_surface_ele:
                list_coords.append(everyline[9:31].strip())  # 按照字符的数量截取字符串
                list_coords.append(everyline[31:53].strip())
                list_coords.append(everyline[53:75].strip())
                list_coords_x.append(everyline[9:31].strip())
    str_coords_allFile = ','.join(list_coords) + '\n'  # 带初始坐标信息
    # Text_Create('original_coords_x', ','.join(list_coords_x), 'hex')
    Text_Create('original_coords_x', ','.join(list_coords_x), 'four')
    # list_coords_allFile = []

    str_Dcolor_min = Str_Color_Step(path_input + os.path.basename(files_cut[0]), 'min', 'd')
    str_Dcolor_max = Str_Color_Step(path_input + os.path.basename(files_cut[-1]), 'max', 'd')

    float_Dcolor_step = (float(str_Dcolor_max) - float(str_Dcolor_min)) / 21
    # file_content = ''  # 不带初始坐标信息
    i_processing = 1  # 遍历到第i个文件
    # 将可以组成表面信息的排序好的节点都加1存到list_ele中，因为前面存的都是减过1的
    list_ele = list(map(addOne, str_surface_ele.split(',')))

    str_Dcolor_allFile = ''
    str_displacementSum_allFile = ''
    for file in files_cut:  # 遍历文件夹
        list_sort = []  # 存放加上位移后的所有坐标值的list
        list_Dcolor = []
        # 存放所有坐标值的“从0开始的虚假索引”的字典
        # 结构为{real_index_1：[0,x,y,z],real_index_2:[1,x,y,z]...}
        # 其意图是用0,1...来替换real_index_1,real_index_2...
        dict_coord = {}
        if not os.path.isdir(file):  # 判断是否是文件夹，不是文件夹才打开
            filename = os.path.basename(file)  # 返回文件名
            fullpath_input = path_input + filename  # 得到文件夹中每个文件的完整路径
            infile = open(fullpath_input, 'rt')  # 以文本形式读取文件
            iCount = 0  # 上述初始的坐标值的list_coords中的索引，每3个一组
            iCoord = 0  # 上述替换真实索引值(real_index_12...)的值
            for line in infile:
                list_temp = []  # 存放NLIST.lis中每行三个坐标的list
                if len(line) == 62:
                    line_index = int(line[0:9].strip())  # 获取节点编号
                    if line_index in set_surface_ele:  # 如果该点是表面点和位移运算得到点的最终坐标
                        list_sort.append(str(float(line[9:22].strip()) + float(list_coords[iCount])))
                        list_sort.append(str(float(line[22:35].strip()) + float(list_coords[iCount + 1])))
                        list_sort.append(str(float(line[35:48].strip()) + float(list_coords[iCount + 2])))
                        list_Dcolor.append(line[49:61].strip())  # 将位移之和的值传入数组
                        if i_processing == 1:  # 如果是第一个文件，执行这段代码，因为每个文件表面点的编号都一样
                            list_temp.append(str(float(line[9:22].strip()) + float(list_coords[iCount])))
                            list_temp.append(str(float(line[22:35].strip()) + float(list_coords[iCount + 1])))
                            list_temp.append(str(float(line[35:48].strip()) + float(list_coords[iCount + 2])))
                            dict_coord[line_index] = [iCoord, list_temp[0:4]]  # 将对应点的真实编号和要更新的iCoord一一对应起来
                            iCoord += 1
                        iCount += 3
        if i_processing == 1:
            for i_ele in range(len(list_ele)):  # 将排序好的表面点的索引值替换成更新后的0,1,2...索引
                if int(list_ele[i_ele]) in dict_coord.keys():  # 如果list_ele中的索引是表面的点的索引，进行替换
                    # print(list_ele[iEle])
                    list_ele[i_ele] = str(dict_coord[int(list_ele[i_ele])][0])  # 获取字典dict_coord中的第一值替换list_ele
                    # print('替换后:' + list_ele[iEle])

        list_Dcolor_result = map(defineColor, map(float, list_Dcolor), itertools.repeat(float(str_Dcolor_min)),
                                 itertools.repeat(float_Dcolor_step))
        str_Dcolor_allFile += ','.join(map(str, list_Dcolor_result)) + '\n'
        str_displacementSum_allFile += ','.join(list_Dcolor) + '\n'
        # print(','.join(list_sort))
        i_processing += 1
        print("\r程序当前已完成：" + str(round(i_processing / len(files) * 100)) + '%', end="")
        str_coords_allFile += ','.join(list_sort) + '\n'  # 以逗号为分隔符来组成字符串,并在最后添加换行符,以换行符区分每个文件的信息
    str_Dcolor_allFile += str(float_Dcolor_step * 21 / 9)
    # 将所有加了位移信息的坐标值和将真实索引值（real_index_12...）更新为[0,1...]的list_ele返回
    return str_coords_allFile.rstrip('\n'), list_ele, str_Dcolor_allFile, str_displacementSum_allFile.rstrip(
        '\n'), str(float_Dcolor_step) + ',' + str(str_Dcolor_min)


def Tuple_Surface_Scolor_Stress(path_input, set_surface_ele):
    isExists = os.path.exists(path_input)
    if not isExists:
        os.makedirs(path_input)
        print(path_input + ' 创建成功')
    else:
        print(path_input + ' 目录已存在')
    files_stress = os.listdir(path_input)
    files_stress.sort(key=lambda x: int(x[:-4]))
    str_Scolor_min = Str_Color_Step(path_input + os.path.basename(files_stress[0]), 'min', 's')
    str_Scolor_max = Str_Color_Step(path_input + os.path.basename(files_stress[-1]), 'max', 's')
    float_Scolor_step = (float(str_Scolor_max) - float(str_Scolor_min)) / 21

    i_processing = 0
    str_Scolor_allFile = ''
    str_stress_allFile = ''
    for file in files_stress:  # 遍历文件夹
        list_Scolor = []
        if not os.path.isdir(file):  # 判断是否是文件夹，不是文件夹才打开
            filename = os.path.basename(file)  # 返回文件名
            fullpath = path_input + filename  # 得到文件夹中每个文件的完整路径
            infile = open(fullpath, 'rt')  # 以文本形式读取文件
            i_line = 0
            for line in infile:
                if i_line == 1:
                    line_index = int(line.split('\t')[0])
                    if line_index in set_surface_ele:
                        list_Scolor.append(line.split('\t')[1])  # 将每一行以制表符分开后加入到list_Scolor序列中
                i_line = 1
        # list_Scolor.pop(0)  # 去掉list_Scolor序列的第一个元素，是一串字母，不是数字
        list_Scolor_eachfile = ''.join(list_Scolor).split('\n')  # 以空字符将list_Scolor连接为字符串，再以换行符转为list
        list_Scolor_eachfile.pop()  # 去掉最后一个换行符

        list_Scolor_result = map(defineColor, map(float, list_Scolor_eachfile), itertools.repeat(float(str_Scolor_min)),
                                 itertools.repeat(float_Scolor_step))

        i_processing += 1
        print("\r程序当前已完成：" + str(round(i_processing / len(files_stress) * 100)) + '%', end="")
        str_Scolor_allFile += ','.join(map(str, list_Scolor_result)) + '\n'  # 以逗号为分隔符来组成字符串,并在最后添加换行符,以换行符区分每个文件的信息
        str_stress_allFile += ','.join(list_Scolor_eachfile) + '\n'

    str_Scolor_allFile += str(float_Scolor_step * 21 / 9)
    return str_Scolor_allFile, str_stress_allFile.rstrip('\n'), str(float_Scolor_step) + ',' + str(str_Scolor_min)


'''四面体NLIST.lis路径和displacement路径'''

path_coords_four = path_four + "dopAndCoord/"
tuple_surface_coords_ele_Dcolor_four = Tuple_Surface_Coords_Ele_Dcolor(path_coords_four, str_surface_ele_four,
                                                                       set_surface_ele_four)
'''四面体stress路径'''
# path_stress_four = path_four + "stress/"
path_equivalent_stress_four = path_four + "equivalent_stress/"
# tuple_surface_stress_Scolor_four = Tuple_Surface_Scolor_Stress(path_stress_four, set_surface_ele_four)
tuple_surface_equivalent_stress_Scolor_four = Tuple_Surface_Scolor_Stress(path_equivalent_stress_four,
                                                                          set_surface_ele_four)

Text_Create('displacement_coords_surface_new', tuple_surface_coords_ele_Dcolor_four[0], 'four')
Text_Create('element_surface_new', ','.join(tuple_surface_coords_ele_Dcolor_four[1]), 'four')
Text_Create('dSum_surface_new', tuple_surface_coords_ele_Dcolor_four[3], 'four')
Text_Create('e_stress_surface_new', tuple_surface_equivalent_stress_Scolor_four[1], 'four')
Text_Create('stress_dSum_step',
            tuple_surface_coords_ele_Dcolor_four[-1] + "," + tuple_surface_equivalent_stress_Scolor_four[-1],
            'four')

# Text_Create('sColor_surface_new', tuple_surface_stress_Scolor_four[0], 'four')
# Text_Create('stress_surface_new', tuple_surface_stress_Scolor_four[1], 'four')
# Text_Create('dColor_surface_new', tuple_surface_coords_ele_Dcolor_four[2], 'four')

'''六面体NLIST.lis路径和displacement路径'''
# path_hex = "C:/Users/asus/Desktop/DT_RopewayDemo/APP_A_CantileverBeam/APP_models/list_new/new_utils/pre/"

path_coords_hex = path_hex + "dopAndCoord/"
tuple_surface_coords_ele_Dcolor_hex = Tuple_Surface_Coords_Ele_Dcolor(path_coords_hex, str_surface_ele_hex,
                                                                      set_surface_ele_hex)
'''六面体stress路径'''
# path_stress_hex = path_hex + "stress/"
path_equivalent_stress_hex = path_hex + "equivalent_stress/"
# tuple_surface_stress_Scolor_hex = Tuple_Surface_Scolor_Stress(path_stress_hex, set_surface_ele_hex)
tuple_surface_equivalent_stress_Scolor_hex = Tuple_Surface_Scolor_Stress(path_equivalent_stress_hex,
                                                                         set_surface_ele_hex)
#
# Text_Create('displacement_coords_surface_new', tuple_surface_coords_ele_Dcolor_hex[0], 'hex')
# Text_Create('element_surface_new', ','.join(tuple_surface_coords_ele_Dcolor_hex[1]), 'hex')
# Text_Create('dSum_surface_new', tuple_surface_coords_ele_Dcolor_hex[3], 'hex')
# Text_Create('e_stress_surface_new', tuple_surface_equivalent_stress_Scolor_hex[1], 'hex')
# Text_Create('stress_dSum_step',
#             str(tuple_surface_coords_ele_Dcolor_hex[-1]) + "," + str(tuple_surface_equivalent_stress_Scolor_hex[-1]),
#             'hex')

# Text_Create('sColor_surface_new', tuple_surface_stress_Scolor_hex[0], 'hex')
# Text_Create('stress_surface_new', tuple_surface_stress_Scolor_hex[1], 'hex')
# Text_Create('e_sColor_surface_new', tuple_surface_equivalent_stress_Scolor_hex[0], 'hex')
# Text_Create('dColor_surface_new', tuple_surface_coords_ele_Dcolor_hex[2], 'hex')
