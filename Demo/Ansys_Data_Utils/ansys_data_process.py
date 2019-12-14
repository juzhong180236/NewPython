# 【程序介绍】点的索引值和坐标值数据清洗
# 缩小点的索引值数据所在文件的大小，前一道程序先用javascript写的，后期改到python中
import os
import itertools
import color_separate as cs
import text_file_create as tfc

path_switch = "/"
# 读取路径@@@@@@@@@@@@@@@@@@@@@(读pre)
path_four_read = "C:/Users/asus/Desktop/DT_Crane_Demo/APP_models" + path_switch + "pre/"
# '''四面体ELIST.lis路径'''
path_ele_four = "C:/Users/asus/Desktop/DT_Crane_Demo/APP_models" + path_switch + "pre/ele/ELIST.lis"
# 存储路径
path_four_write = "C:/Users/asus/Desktop/DT_Crane_Demo/APP_models" + path_switch + "mid/"

# 读取路径@@@@@@@@@@@@@@@@@@@@@(读pre)
# path_four = r"C:\Users\asus\Desktop\History\History_codes\DT_Origin_Demo\APP_A_CantileverBeam\APP_models\list_new\pre\\"
# '''四面体ELIST.lis路径'''
# path_ele_four = r"C:\Users\asus\Desktop\History\History_codes\DT_Origin_Demo\APP_A_CantileverBeam\APP_models\list_new\pre\ele\ELIST.lis"

path_hex = "C:/Users/asus/Desktop/DT_Crane_Demo/APP_models" + path_switch + "pre/"
'''六面体ELIST.lis路径'''
path_ele_hex = "C:/Users/asus/Desktop/DT_Crane_Demo/APP_models" + path_switch + "pre/ele/ELIST.lis"


class AnsysData(object):
    def __init__(self):
        pass





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
# def Str_Color_Step(path_input, min_or_max, stress_or_displacement):
def Str_Color_Step(path_input, stress_or_displacement):
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
    # if min_or_max == 'min':
    return list_color_ToStep_sorted[0], list_color_ToStep_sorted[-1]
    # elif min_or_max == 'max':
    # return list_color_ToStep_sorted[len(list_color_ToStep_sorted) - 1]
    # return list_color_ToStep_sorted[-1]
    # else:
    #     pass


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
    # files_cut = sorted(files[0:-1], key=lambda x: int(x[:-4]))
    files_cut = sorted(files[0:-1], key=lambda x: int(x))
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
    # str_coords_allFile = ','.join(list_coords) + '\n'  # 带初始坐标信息
    str_coords_allFile = ''  # 不带初始坐标信息
    # tfc.text_Create(path_hex, 'original_coords_x', ','.join(list_coords_x))
    tfc.text_Create(path_four_write, 'original_coords_x', ','.join(list_coords_x))
    # list_coords_allFile = []
    list_Dcolor_min = []
    list_Dcolor_max = []
    for file_cut in files_cut:
        Dcolor_min, Dcolor_max = Str_Color_Step(path_input + os.path.basename(file_cut), 'd')
        list_Dcolor_min.append(Dcolor_min)
        list_Dcolor_max.append(Dcolor_max)
    list_Dcolor_min.sort(key=lambda x: float(x))
    list_Dcolor_max.sort(key=lambda x: float(x))
    str_Dcolor_min = list_Dcolor_min[0]
    str_Dcolor_max = list_Dcolor_max[-1]
    # str_Dcolor_min = Str_Color_Step(path_input + os.path.basename(files_cut[0]), 'min', 'd')
    # str_Dcolor_max = Str_Color_Step(path_input + os.path.basename(files_cut[-1]), 'max', 'd')

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

        list_Dcolor_result = map(cs.define_Color, map(float, list_Dcolor), itertools.repeat(float(str_Dcolor_min)),
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
    # files_stress.sort(key=lambda x: int(x[:-4]))
    files_stress.sort(key=lambda x: int(x[:-4]))
    list_Scolor_min = []
    list_Scolor_max = []
    for file_stress in files_stress:
        Scolor_min, Scolor_max = Str_Color_Step(path_input + os.path.basename(file_stress), 's')
        list_Scolor_min.append(Scolor_min)
        list_Scolor_max.append(Scolor_max)
    list_Scolor_min.sort(key=lambda x: float(x))
    list_Scolor_max.sort(key=lambda x: float(x))
    str_Scolor_min = list_Scolor_min[0]
    str_Scolor_max = list_Scolor_max[-1]
    # str_Scolor_min = Str_Color_Step(path_input + os.path.basename(files_stress[0]), 'min', 's')
    # str_Scolor_max = Str_Color_Step(path_input + os.path.basename(files_stress[-1]), 'max', 's')
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

        list_Scolor_result = map(cs.define_Color, map(float, list_Scolor_eachfile),
                                 itertools.repeat(float(str_Scolor_min)),
                                 itertools.repeat(float_Scolor_step))

        i_processing += 1
        print("\r程序当前已完成：" + str(round(i_processing / len(files_stress) * 100)) + '%', end="")
        str_Scolor_allFile += ','.join(map(str, list_Scolor_result)) + '\n'  # 以逗号为分隔符来组成字符串,并在最后添加换行符,以换行符区分每个文件的信息
        str_stress_allFile += ','.join(list_Scolor_eachfile) + '\n'

    str_Scolor_allFile += str(float_Scolor_step * 21 / 9)
    return str_Scolor_allFile, str_stress_allFile.rstrip('\n'), str(float_Scolor_step) + ',' + str(str_Scolor_min)


'''四面体NLIST.lis路径和displacement路径'''

path_coords_four = path_four_read + "dopAndCoord/"
tuple_surface_coords_ele_Dcolor_four = Tuple_Surface_Coords_Ele_Dcolor(path_coords_four, str_surface_ele_four,
                                                                       set_surface_ele_four)
'''四面体stress路径'''
# path_stress_four = path_four + "stress/"
path_equivalent_stress_four = path_four_read + "equivalent_stress/"
# tuple_surface_stress_Scolor_four = Tuple_Surface_Scolor_Stress(path_stress_four, set_surface_ele_four)
tuple_surface_equivalent_stress_Scolor_four = Tuple_Surface_Scolor_Stress(path_equivalent_stress_four,
                                                                          set_surface_ele_four)

tfc.text_Create(path_four_write, 'displacement_coords_surface_new', tuple_surface_coords_ele_Dcolor_four[0])
tfc.text_Create(path_four_write, 'element_surface_new', ','.join(tuple_surface_coords_ele_Dcolor_four[1]))
tfc.text_Create(path_four_write, 'dSum_surface_new', tuple_surface_coords_ele_Dcolor_four[3])
tfc.text_Create(path_four_write, 'e_stress_surface_new', tuple_surface_equivalent_stress_Scolor_four[1])
tfc.text_Create(path_four_write, 'stress_dSum_step',
                tuple_surface_coords_ele_Dcolor_four[-1] + "," + tuple_surface_equivalent_stress_Scolor_four[-1])

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
