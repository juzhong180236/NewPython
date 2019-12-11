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
file = open("C:/Users/asus/\Desktop/test/ele/ELIST.lis", "rt")
list_result = []
for everyline in file:
    if len(everyline) == 54:
        list_temp = Text_PerLine_ToList(everyline)
        ele(list_result, list_temp)
str_result = ','.join(map(str, list_result))

text_create('ele_reault', str_result)
