# 【输入str，str】：生成的文件名，需要写入文档的文本数据
# 【功能】：创建一个文档
def text_Create(savepath, filename, msg, filesuffix='.txt'):
    fullpath = savepath + filename + filesuffix
    # 创建写入的文档
    file = open(fullpath, 'w')
    file.write(msg)
    file.close()
