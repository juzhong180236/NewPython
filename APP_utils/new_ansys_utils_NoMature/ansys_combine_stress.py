import os


# 【程序介绍】应力
# 在一个文件夹下读取不同的应力文件数据，
# 然后将其添加到同一个txt文件中，每个应力文件的数据以换行符隔开

# 创建txt文件
def text_create(name, msg):
    # desktop_path = "C:\\Users\\asus\\Desktop\\"  # 新创建的txt文件的存放路径
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
path = "C:/Users/asus/Desktop/DT_RopewayDemo/APP_A_CantileverBeam/APP_models/list_new/new_utils/pre/stress/"
isExists = os.path.exists(path)
# 判断结果
if not isExists:
    # 如果不存在则创建目录
    os.makedirs(path)  # 创建目录操作函数
    print(path + ' 创建成功')
else:
    # 如果目录存在则不创建，并提示目录已存在
    print(path + ' 目录已存在')
# 获取当前文档下的文件
files = os.listdir(path)
file_content = ''
files.sort(key=lambda x: int(x[:-4]))
for file in files:  # 遍历文件夹
    arr_sort = []
    if not os.path.isdir(file):  # 判断是否是文件夹，不是文件夹才打开
        filename = os.path.basename(file)  # 返回文件名
        # print(filename)
        fullpath = path + filename  # 得到文件夹中每个文件的完整路径

        infile = open(fullpath, 'rt')  # 以文本形式读取文件
        for line in infile:
            arr_sort.append(line.split('\t')[1])  # 将每一行以制表符分开后加入到arr_sort序列中
    arr_sort.pop(0)  # 去掉arr_sort序列的第一个元素，是一串字母，不是数字
    # print(','.join(''.join(arr_sort).split('\n')))
    arr_each_file = ''.join(arr_sort).split('\n')  # 以换行符为分割将arr_sort连接为字符串，并以空字符又转为list
    arr_each_file.pop()  # 去掉最后一个换行符
    file_content += ','.join(arr_each_file) + '\n'  # 以逗号为分隔符来组成字符串,并在最后添加换行符,以换行符区分每个文件的信息
# print(file_content)
text_create('stress', file_content.rstrip('\n'))
