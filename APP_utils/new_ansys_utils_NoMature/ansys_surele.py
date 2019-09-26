import os


# 【程序介绍】变形
# 在一个文件夹下读取不同的位移文件数据，
# 然后将其添加到同一个txt文件中，每个位移文件的数据以换行符隔开
def textToList(string):
    list_str = string.strip().split(" ")
    list_temp = []
    for i in range(len(list_str)):
        if list_str[i] != "":
            list_temp.append(list_str[i])
    return list_temp


# 创建txt文件
def text_create(name, msg):
    desktop_path = "C:/Users/asus/Desktop/DT_RopewayDemo/APP_A_CantileverBeam/APP_models/list_new/new_utils/post/"
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
path = "C:/Users/asus/Desktop/DT_RopewayDemo/APP_A_CantileverBeam/APP_models/list_new/new_utils/pre/surele/"
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

set_surele = set()
for file in files:  # 遍历文件夹
    if not os.path.isdir(file):  # 判断是否是文件夹，不是文件夹才打开
        filename = os.path.basename(file)  # 返回文件名
        if filename == 'surele.txt':
            fullpath = path + filename  # 得到文件夹中每个文件的完整路径
            infile = open(fullpath, 'rt')  # 以文本形式读取文件
            list_surele = []
            for line in infile:
                list_surele.append(line.split('\t')[0])
            list_surele.pop(0)
            set_surele = set(list_surele)
print(len(set_surele))
list_result = []
file_content = ''
i = 1
for file in files:  # 遍历文件夹
    if not os.path.isdir(file):  # 判断是否是文件夹，不是文件夹才打开
        filename = os.path.basename(file)  # 返回文件名
        if filename == 'ELIST.lis':
            fullpath = path + filename  # 得到文件夹中每个文件的完整路径
            infile = open(fullpath, 'rt')  # 以文本形式读取文件
            for line in infile:
                if len(line) == 78:
                    list_temp = textToList(line)
                    if len(list_temp) != 8:
                        l_l = list(set(list_temp[6:]) & set_surele)
                        if len(l_l) == 3:  # 直接画 一个三角形
                            list_result.extend([l_l[0], l_l[1], l_l[2]])
                        elif len(l_l) == 4:  # 全画 四个三角形
                            list_result.extend([l_l[0], l_l[1], l_l[2],
                                                l_l[0], l_l[1], l_l[3],
                                                l_l[0], l_l[2], l_l[3],
                                                l_l[1], l_l[2], l_l[3]])
                        # elif len(l_l) == 5: #
                        #     print(list_temp[0] + ":" + str(l_l))
                        elif len(l_l) == 6:
                            # print(list_temp[0] + ":" + str(l_l))
                            list_result.extend([l_l[0], l_l[1], l_l[2], l_l[0], l_l[1], l_l[3],
                                                l_l[0], l_l[1], l_l[4], l_l[0], l_l[1], l_l[5],
                                                l_l[0], l_l[2], l_l[3], l_l[0], l_l[2], l_l[4],
                                                l_l[0], l_l[2], l_l[5], l_l[0], l_l[3], l_l[4],
                                                l_l[0], l_l[3], l_l[5], l_l[0], l_l[4], l_l[5],
                                                l_l[1], l_l[2], l_l[3], l_l[1], l_l[2], l_l[4],
                                                l_l[1], l_l[2], l_l[5], l_l[1], l_l[3], l_l[4],
                                                l_l[1], l_l[3], l_l[5], l_l[1], l_l[4], l_l[5],
                                                l_l[2], l_l[3], l_l[4], l_l[2], l_l[3], l_l[5],
                                                l_l[2], l_l[4], l_l[5], l_l[3], l_l[4], l_l[5]])
                        elif len(l_l) == 7:
                            print(list_temp[0] + ":" + str(l_l))
                            # pass
                        elif len(l_l) == 8:
                            print(list_temp[0] + ":" + str(l_l))
                        else:
                            pass
            # print(list_result)
            i += 1
            print("\r程序当前已完成：" + str(round(i / len(files) * 100)) + '%', end="")
    file_content = ','.join(list_result)  # 以逗号为分隔符来组成字符串,并在最后添加换行符,以换行符区分每个文件的信息
# text_create('surele', file_content)
