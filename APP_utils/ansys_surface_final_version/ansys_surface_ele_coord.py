# 【程序介绍】点的索引值和坐标值数据清洗
# 缩小点的索引值数据所在文件的大小，前一道程序先用javascript写的，后期改到python中
import os


# 将以多个空格隔开的一行字符串转为list
def textToList(string):
    list_str = string.strip().split(" ")
    list_temp = []
    for i in range(len(list_str)):
        if list_str[i] != "":
            list_temp.append(int(list_str[i]))
    return list_temp


# 创建txt文件
def text_create(name, msg):
    desktop_path = "C:/Users/asus/Desktop/DT_RopewayDemo/APP_A_CantileverBeam/APP_models/list_new/post/"
    full_path = desktop_path + name + '.txt'  # 也可以创建一个.doc的word文档
    # 创建写入的文档
    file = open(full_path, 'w')
    file.write(msg)
    file.close()


# 对排列好的画出四面体的索引，提取只出现一次的索引，返回提取好的索引字符串，以逗号隔开
def arrRemoveSameEle(array):
    arr_sort = []
    for i in range(0, len(array), 3):
        arr = [int(array[i]), int(array[i + 1]), int(array[i + 2])]
        arr.sort(key=lambda x: x)
        arr_sort.append(str(arr[0]) + ',' + str(arr[1]) + ',' + str(arr[2]))
    set_sort = set(arr_sort)
    dict_sort = {}
    for arr_ele in arr_sort:
        dict_sort[arr_ele] = 0
        # 列表arr_sort中的某元素所重复的次数,初始次数为0
    for arr_ele in arr_sort:
        if arr_ele in set_sort:
            dict_sort[arr_ele] += 1  # 如果检测到元素一次，就加1
    list_sort = []
    for key, value in dict_sort.items():
        if value == 1:
            list_sort.append(key)
    return ','.join(list_sort)


# 所有的ele前4位排列为四面体的画图形式
eleFile = open(
    "C:/Users/asus/Desktop/DT_RopewayDemo/APP_A_CantileverBeam/APP_models/list_new/pre/ele/ELIST.lis",
    "rt")
list_result = []
for everyline in eleFile:
    if len(everyline) == 78:
        list_temp = textToList(everyline)
        if len(list_temp) == 14:
            list_result.extend([list_temp[6] - 1, list_temp[7] - 1, list_temp[8] - 1,
                                list_temp[7] - 1, list_temp[8] - 1, list_temp[9] - 1,
                                list_temp[6] - 1, list_temp[8] - 1, list_temp[9] - 1,
                                list_temp[6] - 1, list_temp[7] - 1, list_temp[9] - 1])
result = arrRemoveSameEle(list_result)
eleFile.close()


# text_create('ele_surface_new', result)


def addOne(x):
    return int(x) + 1


set_surface_coord_ele = set(map(addOne, set(result.split(','))))

# 打开读取的文档
path = "C:/Users/asus/Desktop/DT_RopewayDemo/APP_A_CantileverBeam/APP_models/list_new/pre/dopAndCoord/"
isExisted = os.path.exists(path)
# 判断结果
if not isExisted:
    # 如果不存在则创建目录
    os.makedirs(path)  # 创建目录操作函数
    print(path + ' 创建成功')
else:
    # 如果目录存在则不创建，并提示目录已存在
    print(path + ' 目录已存在')
# 获取当前文档下的文件
files = os.listdir(path)
files_cut = sorted(files[0:-1], key=lambda x: int(x[:-4]))

arr_coord = []
coordfile = open(path + "coord", 'rt')
for everyline in coordfile:
    if len(everyline) == 76:
        arr_coord.append(everyline[9:31].strip())  # 按照字符的数量截取字符串
        arr_coord.append(everyline[31:53].strip())  #
        arr_coord.append(everyline[53:75].strip())  #
# print(arr_coord)
file_content = ','.join(arr_coord) + '\n'  # 带初始坐标信息
# file_content = ''  # 不带初始坐标信息
i = 1

list_ele = list(map(addOne, result.split(',')))

for file in files_cut:  # 遍历文件夹
    arr_sort = []
    dict_coord = {}
    if not os.path.isdir(file):  # 判断是否是文件夹，不是文件夹才打开
        filename = os.path.basename(file)  # 返回文件名
        # print(filename)
        fullpath = path + filename  # 得到文件夹中每个文件的完整路径

        infile = open(fullpath, 'rt')  # 以文本形式读取文件
        iCount = 0
        iCoord = 0
        for line in infile:
            arr_temp = []
            if len(line) == 62:
                line_index = int(line[0:9].strip())
                if line_index in set_surface_coord_ele:
                    arr_sort.append(str(float(line[9:22].strip()) + float(arr_coord[iCount])))
                    arr_sort.append(str(float(line[22:35].strip()) + float(arr_coord[iCount + 1])))
                    arr_sort.append(str(float(line[35:48].strip()) + float(arr_coord[iCount + 2])))
                    if i == 1:
                        arr_temp.append(str(float(line[9:22].strip()) + float(arr_coord[iCount])))
                        arr_temp.append(str(float(line[22:35].strip()) + float(arr_coord[iCount + 1])))
                        arr_temp.append(str(float(line[35:48].strip()) + float(arr_coord[iCount + 2])))
                        dict_coord[line_index] = [iCoord, arr_temp[0:4]]
                        iCoord += 1
                    iCount += 3
    if i == 1:
        # print(dict_coord)
        iEle = 0
        for iEle in range(len(list_ele)):
            if int(list_ele[iEle]) in dict_coord.keys():
                # print(list_ele[iEle])
                list_ele[iEle] = str(dict_coord[int(list_ele[iEle])][0])
                # print('替换后:' + list_ele[iEle])
    # print(','.join(arr_sort))
    i += 1
    print("\r程序当前已完成：" + str(round(i / len(files) * 100)) + '%', end="")
    file_content += ','.join(arr_sort) + '\n'  # 以逗号为分隔符来组成字符串,并在最后添加换行符,以换行符区分每个文件的信息
# print(file_content)
# print(list_ele)

iEle = 0
for iEle in range(len(list_ele)):
    if int(list_ele[iEle]) in dict_coord.keys():
        list_ele[iEle] = str(dict_coord[int(list_ele[iEle])][0])

text_create('dop_Coord_surface', file_content.rstrip('\n'))
text_create('ele_surface_new', ','.join(list_ele))
