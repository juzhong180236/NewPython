import os
import itertools

'''程序输出：
1、三个静止面的节点索引和节点坐标
2、四个面的颜色信息
'''
# 读取路径
path = r"C:\Users\asus\Desktop\DT_Testbed\APP_models\points\v3_vp\\"


def Text_Create(name, msg):
    # 存储路径
    save_path = r"C:\Users\asus\Desktop\DT_Testbed\APP_models\post_points\v5\\"
    full_path = save_path + name + '.csv'
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


def ele(elelist, everyline):
    elelist.extend([everyline[0], everyline[1],
                    everyline[2], everyline[2],
                    everyline[0], everyline[3]])


def createcolor(origin, step, list_min):
    list_float = list(map(float, origin))
    # list_float_copy = list_float.copy()
    # list_float_copy.sort(key=lambda x: x)
    # step = (list_float_copy[-1] - list_float_copy[0]) / 21
    # list_min = list_float_copy[0]
    list_result = list(map(defineColor, list_float, itertools.repeat(list_min),
                           itertools.repeat(step)))
    return list_result


def Tuple(path_input):
    files = os.listdir(path_input)  # 获取当前文档下的文件
    str_allfile_color_1_v = ''
    str_allfile_color_2_v = ''
    str_allfile_color_3_v = ''
    str_allfile_color_4_v = ''
    str_allfile_color_1_p = ''
    str_allfile_color_2_p = ''
    str_allfile_color_3_p = ''
    str_allfile_color_4_p = ''
    str_allfile_coords = ''
    str_allfile_ele = ''
    i_processing = 0  # 遍历到第i个文件
    for file in files:  # 遍历文件夹
        if not os.path.isdir(file):
            filename = os.path.basename(file)  # 返回文件名
            fullpath_input = path_input + filename
            coordfile = open(fullpath_input, 'rt')

            if filename == 'export.csv':
                i_face = 0
                list_f1_coords = []
                list_f2_coords = []
                list_f3_coords = []
                list_f4_coords = []
                list_f1_index = []
                list_f2_index = []
                list_f3_index = []
                list_f4_index = []
                for everyline in coordfile:
                    if everyline.strip() == '[Data]':
                        i_face += 1
                    everyline = everyline.rstrip('\n')
                    list_everyline = everyline.split(', ')
                    if len(list_everyline) == 3 and list_everyline[0] != 'X [ mm ]':
                        if i_face == 1:
                            list_f1_coords.extend(list_everyline)
                        elif i_face == 2:
                            list_f2_coords.extend(list_everyline)
                        elif i_face == 3:
                            list_f3_coords.extend(list_everyline)
                        elif i_face == 4:
                            list_f4_coords.extend(list_everyline)
                    elif len(list_everyline) == 4:
                        if i_face == 1:
                            ele(list_f1_index, list_everyline)
                        elif i_face == 2:
                            ele(list_f2_index, list_everyline)
                        elif i_face == 3:
                            ele(list_f3_index, list_everyline)
                        elif i_face == 4:
                            ele(list_f4_index, list_everyline)
                    else:
                        continue
                        # ','.join(list_f2_coords) + '\n' + \
                        # ','.join(map(str, list_f2_index)) + '\n' + \
                str_allfile_coords = ','.join(list_f1_coords) + '\n' + \
                                     ','.join(list_f3_coords) + '\n' + \
                                     ','.join(list_f4_coords) + '\n'
                str_allfile_ele = ','.join(map(str, list_f1_index)) + '\n' + \
                                  ','.join(map(str, list_f3_index)) + '\n' + \
                                  ','.join(map(str, list_f4_index)) + '\n'
            else:
                i_face = 0
                list_f_v = []
                list_f1_v = []
                list_f2_v = []
                list_f3_v = []
                list_f4_v = []
                list_f_p = []
                list_f1_p = []
                list_f2_p = []
                list_f3_p = []
                list_f4_p = []
                for everyline in coordfile:
                    if everyline.strip() == '[Data]':
                        i_face += 1
                    everyline = everyline.rstrip('\n')
                    list_everyline = everyline.split(', ')
                    if len(list_everyline) == 2 and list_everyline[0] != 'Pressure [ MPa ]':
                        if i_face == 1:
                            list_f1_p.append(list_everyline[0])
                            list_f1_v.append(list_everyline[1])
                        elif i_face == 2:
                            list_f2_p.append(list_everyline[0])
                            list_f2_v.append(list_everyline[1])
                        elif i_face == 3:
                            list_f3_p.append(list_everyline[0])
                            list_f3_v.append(list_everyline[1])
                        elif i_face == 4:
                            list_f4_p.append(list_everyline[0])
                            list_f4_v.append(list_everyline[1])
                        list_f_p.append(list_everyline[0])
                        list_f_v.append(list_everyline[1])
                    else:
                        continue
                list_f_v = list(map(float, list_f_v))
                list_f_p = list(map(float, list_f_p))
                list_f_v.sort(key=lambda x: x)
                list_f_p.sort(key=lambda x: x)
                step_v = (list_f_v[-1] - list_f_v[0]) / 21
                step_p = (list_f_p[-1] - list_f_p[0]) / 21
                list_min_v = list_f_v[0]
                list_min_p = list_f_p[0]
                list_result1_v = createcolor(list_f1_v, step_v, list_min_v)
                list_result2_v = createcolor(list_f2_v, step_v, list_min_v)
                list_result3_v = createcolor(list_f3_v, step_v, list_min_v)
                list_result4_v = createcolor(list_f4_v, step_v, list_min_v)
                list_result1_p = createcolor(list_f1_p, step_p, list_min_p)
                list_result2_p = createcolor(list_f2_p, step_p, list_min_p)
                list_result3_p = createcolor(list_f3_p, step_p, list_min_p)
                list_result4_p = createcolor(list_f4_p, step_p, list_min_p)

                str_allfile_color_1_v += ','.join(map(str, list_result1_v)) + '\n'
                str_allfile_color_2_v += ','.join(map(str, list_result2_v)) + '\n'
                str_allfile_color_3_v += ','.join(map(str, list_result3_v)) + '\n'
                str_allfile_color_4_v += ','.join(map(str, list_result4_v)) + '\n'
                str_allfile_color_1_p += ','.join(map(str, list_result1_p)) + '\n'
                str_allfile_color_2_p += ','.join(map(str, list_result2_p)) + '\n'
                str_allfile_color_3_p += ','.join(map(str, list_result3_p)) + '\n'
                str_allfile_color_4_p += ','.join(map(str, list_result4_p)) + '\n'
        i_processing += 1
        print("\r程序当前已完成：" + str(round(i_processing / len(files) * 100)) + '%', end="")

    return str_allfile_color_1_v.rstrip('\n'), str_allfile_color_2_v.rstrip('\n'), \
           str_allfile_color_3_v.rstrip('\n'), str_allfile_color_4_v.rstrip('\n'), \
           str_allfile_color_1_p.rstrip('\n'), str_allfile_color_2_p.rstrip('\n'), \
           str_allfile_color_3_p.rstrip('\n'), str_allfile_color_4_p.rstrip('\n'), \
           str_allfile_coords, str_allfile_ele


file_velocity_coords = Tuple(path)
# print(file_velocity_coords[0])
Text_Create("color1_v", file_velocity_coords[0])
Text_Create("color2_v", file_velocity_coords[1])
Text_Create("color3_v", file_velocity_coords[2])
Text_Create("color4_v", file_velocity_coords[3])
Text_Create("color1_p", file_velocity_coords[4])
Text_Create("color2_p", file_velocity_coords[5])
Text_Create("color3_p", file_velocity_coords[6])
Text_Create("color4_p", file_velocity_coords[7])
Text_Create("coords", file_velocity_coords[8])
Text_Create("ele", file_velocity_coords[9])
