import numpy as np
import matplotlib.pyplot as plt
from ReadExcel import readExcel
import os
import printf as pf


def Read_TData(path, sheet):
    data_y, data_x = readExcel(path, sheet,
                               row_num=380,
                               y_column=1)
    return data_x, data_y


def Read_SData(path):
    isExisted = os.path.exists(path)
    if not isExisted:
        pf.printf(path)
        pf.printf('上面列出的路径不存在，请设置正确路径！')
        return
    else:
        pf.printf('目录[' + path + ']存在,正在读取...')

    list_different_angle = []

    file_content = open(path, 'rt')
    list_1 = []
    list_2 = []
    list_3 = []
    list_4 = []
    list_5 = []
    list_6 = []
    list_7 = []
    list_8 = []
    list_angle = []
    i = 0
    for line in file_content:
        i += 1
        if i % 16 == 1:
            list_1.append(np.abs(float(line)))
        elif i % 16 == 2:
            list_angle.append(float(line))
        elif i % 16 == 3:
            list_2.append(float(line))
        elif i % 16 == 5:
            list_3.append(float(line))
        elif i % 16 == 7:
            list_4.append(float(line))
        elif i % 16 == 9:
            list_5.append(float(line))
        elif i % 16 == 11:
            list_6.append(float(line))
        elif i % 16 == 13:
            list_7.append(float(line))
        elif i % 16 == 15:
            list_8.append(float(line))
        else:
            continue
    file_content.close()
    return list_1, list_2, list_3, list_4, list_5, list_6, list_7, list_8, list_angle


def mkdir(path_dir):
    import os
    path_dir = path_dir.strip()
    path_dir = path_dir.rstrip("\\")
    isExists = os.path.exists(path_dir)
    if not isExists:
        os.mkdir(path_dir)
        print(path_dir + ' 创建成功')
        return True
    else:
        print(path_dir + ' 目录已存在')
        return False


# path = r"C:\Users\asus\Desktop\stress data\\"
path = r"C:\Users\asus\Desktop\stress 20200704\\"
load = "20"
list_simulation_data = Read_SData(path + load + r".txt")
list_test_data = Read_TData(path + load + r".xlsx", load)
num = min(len(list_simulation_data[0]), len(list_test_data[1][0]))

# dict_1 = {}
# list_stress = []
# for angle in list_simulation_data[8]:
#     dict_1[angle] = []
#
# list1 = sorted(list(set(list_simulation_data[8])), key=lambda x: int(x))
# for angle, stress in zip(list_simulation_data[8][0:num], list_test_data[1][0][0:num]):
#     dict_1[angle].append(stress)
# print(dict_1)
# for value in sorted(dict_1):
#     list_stress.append(np.average(dict_1[value], axis=-1))
mkdir(path + load)

for i in range(8):
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    # ax2 = ax1.twinx()
    plt.title(load + 'kg Sample Point No.' + str(i + 1))
    plt.plot(list_test_data[0][0:num], list_simulation_data[i][0:num], label="Simulation Data")
    plt.plot(list_test_data[0][0:num], list_test_data[1][i][0:num], label="Experimental Data")

    # ax2.plot(list_test_data[0][0:num], list_simulation_data[8][0:num])

    plt.ylabel("Stress(Mpa)")
    plt.xlabel("time(s)")

    plt.legend()
    # plt.savefig(path + load + r"\\" + str(i + 1) + '.png')
    # plt.show()
