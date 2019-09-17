from functools import cmp_to_key


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


# 排序
def numeric_compare(x, y):
    return x - y


# 返回去除重复的字符串
def arrRemoveSameEle(array):
    arr_sort = []
    for i in range(0, len(array), 3):
        arr = [int(array[i]), int(array[i + 1]), int(array[i + 2])]
        arr.sort(key=cmp_to_key(numeric_compare))
        arr_sort.append(str(arr[0]) + ',' + str(arr[1]) + ',' + str(arr[2]))
    return ','.join(set(arr_sort))

    # print(arr_r)
    # for item in arr_sort:
    #     if item not in arr_sort:
    #         arr_result.append(item)
    #     i += 1
    #     print("\r" + str(round(i / len(arr_sort)*100)/10) + '%', end="") #进度


# 打开读取的文档
tf = open("C:/Users/asus/Desktop/DT_RopewayDemo/APP_A_CantileverBeam/APP_models/list_new/pre/ele/ele.txt", "r")
txt = tf.readline()
array_txt = txt.split(',')
print(len(array_txt))
result = arrRemoveSameEle(array_txt)
tf.close()
print(len(result.split(',')))
text_create('ele', result)
