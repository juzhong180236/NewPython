import os

# 读取路径
path = r"C:\Users\asus\Desktop\DT_Testbed\APP_models\points\\"


def Text_Create(name, msg):
    # 存储路径
    save_path = r"C:\Users\asus\Desktop\DT_Testbed\APP_models\post_points\\"
    full_path = save_path + name + '.csv'
    # 创建写入的文档
    file = open(full_path, 'w')
    file.write(msg)
    file.close()


def Tuple(path_input):
    files = os.listdir(path_input)  # 获取当前文档下的文件
    str_allfile_velocity_color = ''
    str_allfile_coords = ''
    i_processing = 0  # 遍历到第i个文件
    for file in files:  # 遍历文件夹
        if not os.path.isdir(file):
            filename = os.path.basename(file)  # 返回文件名
            # print(filename)
            fullpath_input = path_input + filename
            coordfile = open(fullpath_input, 'rt')
            list_eachfile_velocity = []
            list_eachfile_coords = []
            i_line = 0  # 记录行数
            for everyline in coordfile:
                # print(i_line % 3)
                # if len(everyline) in [63, 64, 65, 66] and i_line % 1.5 == 0:
                if len(everyline) in [63, 64, 65, 66]:
                    list_everyline = everyline.split(',')
                    list_eachfile_velocity.append(list_everyline.pop()[1:-1])
                    list_eachfile_coords.extend(map(lambda x: x.lstrip(' '), list_everyline))
                # i_line += 1
            # str_allfile_velocity += ','.join(list_eachfile_velocity) + '\n'
            list_float_velocity = list(map(float, list_eachfile_velocity))
            list_float_velocity_copy = list_float_velocity.copy()
            list_float_velocity_copy.sort(key=lambda x: x)
            velocity_step = (list_float_velocity_copy[-1] - list_float_velocity_copy[0]) / 21
            list_min_velocity = list_float_velocity_copy[0]

            def colorStep(input, i):
                return input + velocity_step * i

            def defineColor(array_ele):
                if array_ele < colorStep(list_min_velocity, 1):
                    colors = '0,0,1'
                elif colorStep(list_min_velocity, 1) <= array_ele < colorStep(list_min_velocity, 2):
                    colors = '0,' + str(42 / 255) + ',1'
                elif colorStep(list_min_velocity, 2) <= array_ele < colorStep(list_min_velocity, 3):
                    colors = '0,' + str(85 / 255) + ',1'
                elif colorStep(list_min_velocity, 3) <= array_ele < colorStep(list_min_velocity, 4):
                    colors = '0,' + str(127 / 255) + ',1'
                elif colorStep(list_min_velocity, 4) <= array_ele < colorStep(list_min_velocity, 5):
                    colors = '0,' + str(170 / 255) + ',1'
                elif colorStep(list_min_velocity, 5) <= array_ele < colorStep(list_min_velocity, 6):
                    colors = '0,1,1'
                elif colorStep(list_min_velocity, 6) <= array_ele < colorStep(list_min_velocity, 7):
                    colors = '0,1,' + str(170 / 255)
                elif colorStep(list_min_velocity, 7) <= array_ele < colorStep(list_min_velocity, 8):
                    colors = '0,1,' + str(127 / 255)
                elif colorStep(list_min_velocity, 8) <= array_ele < colorStep(list_min_velocity, 9):
                    colors = '0,1,' + str(85 / 255)
                elif colorStep(list_min_velocity, 9) <= array_ele < colorStep(list_min_velocity, 10):
                    colors = '0,1,' + str(42 / 255)
                elif colorStep(list_min_velocity, 10) <= array_ele < colorStep(list_min_velocity, 11):
                    colors = '0,1,0'
                elif colorStep(list_min_velocity, 11) <= array_ele < colorStep(list_min_velocity, 12):
                    colors = str(42 / 255) + ',1,0'
                elif colorStep(list_min_velocity, 12) <= array_ele < colorStep(list_min_velocity, 13):
                    colors = str(85 / 255) + ',1,0'
                elif colorStep(list_min_velocity, 13) <= array_ele < colorStep(list_min_velocity, 14):
                    colors = str(127 / 255) + ',1,0'
                elif colorStep(list_min_velocity, 14) <= array_ele < colorStep(list_min_velocity, 15):
                    colors = str(170 / 255) + ',1,0'
                elif colorStep(list_min_velocity, 15) <= array_ele < colorStep(list_min_velocity, 16):
                    colors = '1,1,0'
                elif colorStep(list_min_velocity, 16) <= array_ele < colorStep(list_min_velocity, 17):
                    colors = '1,' + str(170 / 255) + ',0'
                elif colorStep(list_min_velocity, 17) <= array_ele < colorStep(list_min_velocity, 18):
                    colors = '1,' + str(127 / 255) + ',0'
                elif colorStep(list_min_velocity, 18) <= array_ele < colorStep(list_min_velocity, 19):
                    colors = '1,' + str(85 / 255) + ',0'
                elif colorStep(list_min_velocity, 19) <= array_ele < colorStep(list_min_velocity, 20):
                    colors = '1,' + str(42 / 255) + ',0'
                elif colorStep(list_min_velocity, 20) <= array_ele <= colorStep(list_min_velocity, 21):
                    colors = '1,0,0'
                else:
                    colors = '1,0,0'
                return colors

            list_result = map(defineColor, list_float_velocity)
            str_allfile_coords += ','.join(list_eachfile_coords) + '\n'
            str_allfile_velocity_color += ','.join(map(str, list_result)) + '\n'
        i_processing += 1
        print("\r程序当前已完成：" + str(round(i_processing / len(files) * 100)) + '%', end="")

    return str_allfile_velocity_color.rstrip('\n'), str_allfile_coords.rstrip('\n')


file_velocity_coords = Tuple(path)
# print(file_velocity_coords[0])
Text_Create("velocity", file_velocity_coords[0])
Text_Create("coords", file_velocity_coords[1])
