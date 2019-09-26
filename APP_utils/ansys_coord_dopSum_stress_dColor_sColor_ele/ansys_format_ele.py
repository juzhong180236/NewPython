# 【程序介绍】点的索引值
# 缩小点的索引值数据所在文件的大小，前一道程序先用javascript写的，后期改到python中

# 创建txt文件
def text_create(name, msg):
    # desktop_path = "C:\\Users\\asus\\Desktop\\"  # 新创建的txt文件的存放路径
    desktop_path = "C:/Users/asus/Desktop/DT_RopewayDemo/APP_A_CantileverBeam/APP_models/list_new/post/"
    full_path = desktop_path + name + '.txt'  # 也可以创建一个.doc的word文档
    # 创建写入的文档
    file = open(full_path, 'w')
    file.write(msg)
    file.close()


# 返回去除重复的字符串
def arrRemoveSameEle(array):
    arr_sort = []
    for i in range(0, len(array), 3):
        arr = [int(array[i]), int(array[i + 1]), int(array[i + 2])]
        arr.sort(key=lambda x: x)
        arr_sort.append(str(arr[0]) + ',' + str(arr[1]) + ',' + str(arr[2]))
    set_sort = set(arr_sort)
    # print(len(set_sort))
    dict_sort = {}
    for arr_ele in arr_sort:
        dict_sort[arr_ele] = 0
        # 列表arr_sort中的某元素所重复的次数,初始次数为1
    for arr_ele in arr_sort:
        if arr_ele in set_sort:
            dict_sort[arr_ele] += 1  # 如果检测到元素一次，iCount就加1
    # print(dict_sort)
    list_sort = []
    for key, value in dict_sort.items():
        if value == 1:
            list_sort.append(key)
    # print(list_sort)
    return ','.join(list_sort)


# 打开读取的文档
tf = open("C:/Users/asus/Desktoansys_format_ele.pyp/DT_RopewayDemo/APP_A_CantileverBeam/APP_models/list_new/pre/ele/ELIST.lis", "r")
txt = tf.readline()
array_txt = txt.split(',')
# print(len(array_txt))
result = arrRemoveSameEle(array_txt)
tf.close()
# print(len(result.split(',')))
# print(result)
text_create('ele_surface', result)
