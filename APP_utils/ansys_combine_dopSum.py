import os


# 【程序介绍】变形
# 在一个文件夹下读取不同的位移文件数据，
# 然后将其添加到同一个txt文件中，每个位移文件的数据以换行符隔开

# 创建txt文件
def text_create(name, msg):
    desktop_path = "C:/Users/asus/Desktop/DT_RopewayDemo/APP_A_CantileverBeam/APP_models/list_new/post/"
    pathisExists = os.path.exists(desktop_path)
    # 判断结果
    if not pathisExists:
        # 如果不存在则创建目录
        os.makedirs(desktop_path)  # 创建目录操作函数
        print(desktop_path + ' 创建成功')
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(desktop_path + ' 目录已存在')
    full_path = desktop_path + name + '.txt'  # 也可以创建一个.doc的word文档
    # 创建写入的文档
    file = open(full_path, 'w')
    file.write(msg)
    file.close()


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

# arr_coord = []okim ,,,,,,,,,,,,,,,,,,,
# coordfile = open(path + "coord", 'rt')\'

# for everyline in coordfile:
#     if len(everyline) == 76:
#         arr_coord.append(everyline[9:31].strip())  # 按照字符的数量截取字符串
#         arr_coord.append(everyline[31:53].strip())  #
#         arr_coord.append(everyline[53:75].strip())  #
# print(arr_coord)
# file_content = ','.join(arr_coord) + '\n'
file_content = ''
i = 1
for file in files_cut:  # 遍历文件夹
    arr_sort = []
    if not os.path.isdir(file):  # 判断是否是文件夹，不是文件夹才打开
        filename = os.path.basename(file)  # 返回文件名

        # print(filename)
        fullpath = path + filename  # 得到文件夹中每个文件的完整路径

        infile = open(fullpath, 'rt')  # 以文本形式读取文件
        iCount = 0
        for line in infile:
            if len(line) == 62 and filename != 'coord':
                # arr_sort.append(str(float(line[9:22].strip()) + float(arr_coord[iCount])))
                # arr_sort.append(str(float(line[22:35].strip()) + float(arr_coord[iCount + 1])))
                # arr_sort.append(str(float(line[35:48].strip()) + float(arr_coord[iCount + 2])))
                arr_sort.append(line[49:61].strip())
                # iCount += 3
    # print(','.join(arr_sort))
    i += 1
    print("\r程序当前已完成：" + str(round(i / len(files) * 100)) + '%', end="")
    file_content += ','.join(arr_sort) + '\n'  # 以逗号为分隔符来组成字符串,并在最后添加换行符,以换行符区分每个文件的信息
# print(file_content)
# text_create('dop_Sum', file_content.rstrip('\n'))
