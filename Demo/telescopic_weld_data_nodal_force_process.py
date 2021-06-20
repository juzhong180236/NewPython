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
    def __init__(self, path_read=None, ed=None):
        self.path_read = path_read

    def surfaceCoord_To_List(self, i_file, whichAxis='xyz'):
        list_data = []  # 获取该文件夹下面的节点初始的坐标数据
        coordfile = open(self.path_read + "NFORCE" + str(i_file), 'rt')
        for everyline in coordfile:
            # print(len(everyline))
            if len(everyline) == 82:
                list_everyline = everyline.split()

                list_data.append(
                    " ".join([list_everyline[0].strip(), list_everyline[1].strip(), list_everyline[2].strip(),
                              list_everyline[3].strip()]))
        coordfile.close()
        return "\n".join(list_data)


if __name__ == "__main__":
    path_read = r"C:\Users\asus\Desktop\\"
    path_write = r"C:\Users\asus\Desktop\\"
    read_data = ReadData(path_read=path_read)
    text_create(path_write, "1", read_data.surfaceCoord_To_List(1))
