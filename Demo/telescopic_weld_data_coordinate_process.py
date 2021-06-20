import os


# 【输入str，str】：生成的文件名，需要写入文档的文本数据
# 【功能】：创建一个文档
def text_create(savepath, filename, msg, filesuffix='.txt'):
    isExisted = os.path.exists(savepath)
    if not isExisted:
        print(savepath)
        print('上面列出的目录或文件不存在，请设置正确路径！')
        return
    else:
        print('目录[' + savepath + ']存在,正在创建文件[' + filename + filesuffix + ']...')
    fullpath = savepath + filename + filesuffix
    # 创建写入的文档
    file = open(fullpath, 'w')
    file.write(msg)
    file.close()
    print('文件[' + filename + filesuffix + ']创建完成！')


class ReadData(object):
    def __init__(self, path_read=None):
        self.path_read = path_read

    def read_weld_coordinate(self, i_file):
        coordfile = open(self.path_read + str(i_file) + "_1.lis", 'rt')
        txt = coordfile.read()
        list_temp = txt.split("C")
        for i, temp in enumerate(list_temp):
            text_create(path_write, str(i_file) + "_" + str(i + 1), temp)


if __name__ == "__main__":
    path_read = r"C:\Users\asus\Desktop\weld_data\\"
    path_write = r"C:\Users\asus\Desktop\\"
    read_data = ReadData(path_read=path_read)
    read_data.read_weld_coordinate(1)
    # text_create(path_write, "1", read_data.surfaceCoord_To_List(1))
