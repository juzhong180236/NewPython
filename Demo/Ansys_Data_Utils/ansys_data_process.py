# 【程序介绍】点的索引值和坐标值数据清洗
# 缩小点的索引值数据所在文件的大小，前一道程序先用javascript写的，后期改到python中
import os
import itertools
import color_data as cs
import element_data as ed
import coordinate_data as cd
import text_file_create as tfc

path_switch = "/"
# 读取路径@@@@@@@@@@@@@@@@@@@@@(读pre)
path_four_read = "C:/Users/asus/Desktop/DT_Crane_Demo/APP_models" + path_switch + "pre/"
path_four_read_dopAndCoord = path_four_read + 'dopAndCoord/'
path_four_read_ele = path_four_read + 'ele/'
path_four_read_equivalentStress = path_four_read + 'equivalent_stress/'

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


list_coords_x = cd.surfaceCoord_To_List(path_four_read_dopAndCoord, ['3D4'], 'x')

txt_ele = ed.surfaceEle_Real_Sequence(path_four_read_ele, ['3D4'], path_four_read_dopAndCoord)

tfc.text_Create(path_four_write, 'original_coords_x', ','.join(list_coords_x))


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
