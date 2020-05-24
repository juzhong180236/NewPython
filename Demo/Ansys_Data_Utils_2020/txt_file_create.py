import os
import print_f as pf


# 【输入str，str】：生成的文件名，需要写入文档的文本数据
# 【功能】：创建一个文档
def text_Create(savepath, filename, msg, filesuffix='.txt'):
    isExisted = os.path.exists(savepath)
    if not isExisted:
        pf.printf(savepath)
        pf.printf('上面列出的目录或文件不存在，请设置正确路径！')
        return
    else:
        pf.printf('目录[' + savepath + ']存在,正在创建文件[' + filename + filesuffix + ']...')
    fullpath = savepath + filename + filesuffix
    # 创建写入的文档
    file = open(fullpath, 'w')
    file.write(msg)
    file.close()
    pf.printf('文件[' + filename + filesuffix + ']创建完成！')
