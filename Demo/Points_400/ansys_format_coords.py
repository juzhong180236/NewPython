# 【程序介绍】点的索引值
# 缩小点的索引值数据所在文件的大小，前一道程序先用javascript写的，后期改到python中

# 创建txt文件
def text_create(name, msg):
    # desktop_path = "C:\\Users\\asus\\Desktop\\"  # 新创建的txt文件的存放路径
    desktop_path = "C:/Users/asus/\Desktop/test/"
    full_path = desktop_path + name + '.txt'  # 也可以创建一个.doc的word文档
    # 创建写入的文档
    file = open(full_path, 'w')
    file.write(msg)
    file.close()


def ele(elelist, everyline):
    elelist.extend([everyline[6] - 1, everyline[7] - 1,
                    everyline[8] - 1, everyline[8] - 1,
                    everyline[6] - 1, everyline[9] - 1])


def Text_PerLine_ToList(str_input):
    list_str = str_input.strip().split(" ")
    list_temp = []
    for i in range(len(list_str)):
        if list_str[i] != "":
            list_temp.append(int(list_str[i]))
    return list_temp


# 打开读取的文档
file = open("C:/Users/asus/\Desktop/test/dopAndCoord/NLIST.lis", "rt")
list_coords = []  # 获取该文件夹下面的节点初始的坐标数据
for everyline in file:
    if len(everyline) == 76:
        list_coords.append(everyline[9:31].strip())  # 按照字符的数量截取字符串
        list_coords.append(everyline[31:53].strip())
        list_coords.append(everyline[53:75].strip())
str_coords_File = ','.join(list_coords)
text_create('coords_reault', str_coords_File)
