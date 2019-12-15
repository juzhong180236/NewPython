import os


def color_Compare(array_ele, list_min_ele, color_step, i):
    if i == 0:
        return array_ele < list_min_ele + color_step * (i + 1)
    else:
        return list_min_ele + color_step * i <= array_ele < list_min_ele + color_step * (i + 1)


def define_Color(array_ele, list_min_ele, color_step):
    if color_Compare(array_ele, list_min_ele, color_step, 0):
        colors = '0,0,1'
    elif color_Compare(array_ele, list_min_ele, color_step, 1):
        colors = '0,' + str(42 / 255) + ',1'
    elif color_Compare(array_ele, list_min_ele, color_step, 2):
        colors = '0,' + str(85 / 255) + ',1'
    elif color_Compare(array_ele, list_min_ele, color_step, 3):
        colors = '0,' + str(127 / 255) + ',1'
    elif color_Compare(array_ele, list_min_ele, color_step, 4):
        colors = '0,' + str(170 / 255) + ',1'
    elif color_Compare(array_ele, list_min_ele, color_step, 5):
        colors = '0,1,1'
    elif color_Compare(array_ele, list_min_ele, color_step, 6):
        colors = '0,1,' + str(170 / 255)
    elif color_Compare(array_ele, list_min_ele, color_step, 7):
        colors = '0,1,' + str(127 / 255)
    elif color_Compare(array_ele, list_min_ele, color_step, 8):
        colors = '0,1,' + str(85 / 255)
    elif color_Compare(array_ele, list_min_ele, color_step, 9):
        colors = '0,1,' + str(42 / 255)
    elif color_Compare(array_ele, list_min_ele, color_step, 10):
        colors = '0,1,0'
    elif color_Compare(array_ele, list_min_ele, color_step, 11):
        colors = str(42 / 255) + ',1,0'
    elif color_Compare(array_ele, list_min_ele, color_step, 12):
        colors = str(85 / 255) + ',1,0'
    elif color_Compare(array_ele, list_min_ele, color_step, 13):
        colors = str(127 / 255) + ',1,0'
    elif color_Compare(array_ele, list_min_ele, color_step, 14):
        colors = str(170 / 255) + ',1,0'
    elif color_Compare(array_ele, list_min_ele, color_step, 15):
        colors = '1,1,0'
    elif color_Compare(array_ele, list_min_ele, color_step, 16):
        colors = '1,' + str(170 / 255) + ',0'
    elif color_Compare(array_ele, list_min_ele, color_step, 17):
        colors = '1,' + str(127 / 255) + ',0'
    elif color_Compare(array_ele, list_min_ele, color_step, 18):
        colors = '1,' + str(85 / 255) + ',0'
    elif color_Compare(array_ele, list_min_ele, color_step, 19):
        colors = '1,' + str(42 / 255) + ',0'
    elif color_Compare(array_ele, list_min_ele, color_step, 20):
        colors = '1,0,0'
    else:
        colors = '1,0,0'
    return colors


# 【输入str,str】：displacement或stress所在的文件夹路径；取最小值还是最大值，min，max
# 【输出float】：返回最小值或最大值
# 【功能】：将displacement或stress中最小的和最大的输出
# def Str_Color_Step(path_input, min_or_max, stress_or_displacement):
def max_Min(path_color, stress_or_displacement):
    list_color_ToStep = []
    file = open(path_color, 'rt')
    for line in file:
        if stress_or_displacement == 's':
            list_color_ToStep.append(line.split('\t')[1])
        elif stress_or_displacement == 'd':
            if len(line) == 62:
                list_color_ToStep.append(line[49:61].strip())
    if stress_or_displacement == 's':
        list_color_ToStep.pop(0)
    list_color_ToStep_sorted = sorted(list_color_ToStep, key=lambda x: float(x))
    file.close()
    return list_color_ToStep_sorted[-1], list_color_ToStep_sorted[0]


def color_Step(files_cut, path_color, stress_or_displacement):
    list_color_min = []
    list_color_max = []
    for file_cut in files_cut:
        if not os.path.isdir(file_cut):
            color_max, color_min = max_Min(path_color + os.path.basename(file_cut), stress_or_displacement)
            list_color_min.append(color_min)
            list_color_max.append(color_max)
    list_color_min.sort(key=lambda x: float(x))
    list_color_max.sort(key=lambda x: float(x))
    float_color_min = float(list_color_min[0])
    float_color_max = float(list_color_max[-1])
    float_Dcolor_step = (float_color_max - float_color_min) / 21
    return float_Dcolor_step, float_color_min
