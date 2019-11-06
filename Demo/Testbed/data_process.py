import os

path = r"C:\Users\asus\Desktop\DT_Testbed\APP_models\points\\"


def Text_Create(name, msg):
    # 存储路径
    save_path = r"C:\Users\asus\Desktop\DT_Testbed\APP_models\points\\"
    full_path = save_path + name + '.csv'  # 也可以创建一个.doc的word文档
    # 创建写入的文档
    file = open(full_path, 'w')
    file.write(msg)
    file.close()


def Tuple(path_input):
    files = os.listdir(path_input)  # 获取当前文档下的文件
    str_all_file = ''
    i_processing = 0  # 遍历到第i个文件
    for file in files:  # 遍历文件夹
        if not os.path.isdir(file):
            filename = os.path.basename(file)  # 返回文件名
            # print(filename)
            fullpath_input = path_input + filename
            coordfile = open(fullpath_input, 'rt')
            list_eachfile_velocity = []
            list_eachfile_coords = []
            if i_processing == 0:
                for everyline in coordfile:
                    if len(everyline) in [63, 64, 65, 66]:
                        list_everyline = everyline.split(',')
                        list_everyline.pop()
                        list_eachfile_coords.extend(list_everyline)
            for everyline in coordfile:
                if len(everyline) in [63, 64, 65, 66]:
                    list_everyline = everyline.split(',')
                    list_eachfile_velocity.append(list_everyline.pop())
            print(len(list_eachfile_coords))
            print(len(list_eachfile_coords))
        i_processing += 1
        print("\r程序当前已完成：" + str(round(i_processing / len(files) * 100)) + '%', end="")

        # return ''.join(list_each_file)


# Text_Create("11", Tuple(path))
Tuple(path)
