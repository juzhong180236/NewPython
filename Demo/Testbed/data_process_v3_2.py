import os
import itertools

# 读取路径
path = r"C:\Users\asus\Desktop\DT_Testbed\APP_models\points\v4\\"


def Text_Create(name, msg):
    # 存储路径
    save_path = r"C:\Users\asus\Desktop\DT_Testbed\APP_models\post_points\v4\\"
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


def createcolor(origin):
    list_float = list(map(float, origin))
    list_float_copy = list_float.copy()
    list_float_copy.sort(key=lambda x: x)
    step = (list_float_copy[-1] - list_float_copy[0]) / 21
    list_min = list_float_copy[0]
    list_result = list(map(defineColor, list_float, itertools.repeat(list_min),
                           itertools.repeat(step)))
    return list_result


def Tuple(path_input):
    files = os.listdir(path_input)  # 获取当前文档下的文件
    str_allfile_coords = ''
    str_allfile_ele = ''
    i_processing = 0  # 遍历到第i个文件
    for file in files:  # 遍历文件夹
        if not os.path.isdir(file):
            filename = os.path.basename(file)  # 返回文件名
            fullpath_input = path_input + filename
            coordfile = open(fullpath_input, 'rt')
            list_coords = []
            list_index = []
            for everyline in coordfile:
                everyline = everyline.rstrip('\n')
                list_everyline = everyline.split(', ')
                if len(list_everyline) == 5:
                    list_coords.extend(list_everyline[1:-1])
                elif len(list_everyline) == 4:
                    ele(list_index, list_everyline)
                else:
                    continue
            str_allfile_coords += ','.join(list_coords) + '\n'
            str_allfile_ele += ','.join(map(str, list_index)) + '\n'
        i_processing += 1
        print("\r程序当前已完成：" + str(round(i_processing / len(files) * 100)) + '%', end="")

    return str_allfile_coords.rstrip('\n'), str_allfile_ele.rstrip('\n')


file_velocity_coords = Tuple(path)
Text_Create("coords_dynamic", file_velocity_coords[0])
Text_Create("ele_dynamic", file_velocity_coords[1])
