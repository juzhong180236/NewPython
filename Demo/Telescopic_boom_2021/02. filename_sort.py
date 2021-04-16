import shutil
import os


def objFileName():
    '''
    生成文件名列表
    :return:
    '''
    local_file_name_list = r'C:\Users\asus\Desktop\coordinates'
    # 指定名单
    obj_name_list = []
    for filename in os.listdir(local_file_name_list):
        obj_name_list.append(filename)
    return obj_name_list


def copy_file(_read_path, _write_path, _readfile_name, _writefile_name):
    '''
    复制、重命名、粘贴文件
    :return:
    '''
    is_read_existed = os.path.exists(_read_path)
    if not is_read_existed:
        print(_read_path + " 路径不存在，请设置正确路径！")
    else:
        is_write_existed = os.path.exists(_write_path)
        if not is_write_existed:
            os.mkdir(_write_path)
        shutil.copy(_read_path + '/' + _readfile_name, _write_path + '/' + _writefile_name)


if __name__ == '__main__':

    def excute(which_type):
        read_path = path_ + which_type
        write_path = path_ + which_type + "_sort"
        for i in range(1, 17):
            if i in [1, 2, 3, 7, 14, 15, 16]:
                copy_file(read_path, write_path, str(i) + '_1.txt', str(i) + '_1.txt')
            elif i in [4, 5, 8]:
                copy_file(read_path, write_path, str(i) + '_1.txt', str(i + 1) + '_1.txt')
            elif i in [6]:
                copy_file(read_path, write_path, str(i) + '_1.txt', str(i - 2) + '_1.txt')
            elif i in [9, 11, 12, 13]:
                copy_file(read_path, write_path, str(i) + '_1.txt', str(i - 1) + '_1.txt')
            else:
                copy_file(read_path, write_path, str(i) + '_1.txt', str(i + 3) + '_1.txt')


    path_ = r'C:\Users\asus\Desktop\Code\DT_Telescopic_Boom_v1.0\APP_models\pre_telescopic_boom\\'
    # path_ = r'C:\Users\asus\Desktop\\'
    elements = "elements"
    coordinates = "coordinates"
    stresses = "stresses"
    displacement = "displacement"
    excute(elements)
    excute(coordinates)
    excute(stresses)
    excute(displacement)
