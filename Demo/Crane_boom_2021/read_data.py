import os
import sklearn.gaussian_process.kernels as kns
from sklearn.gaussian_process.kernels import ConstantKernel
import Demo.Ansys_Data_Utils_2021.txt_file_create as tfc
import Demo.Ansys_Data_Utils_2021.print_f as pf
import numpy as np


class Read_Data(object):
    def __init__(self):
        pass

    def read_stress(self, path, mode="h"):

        """
        :param path: 多个static structural数据路径
        :return:
        """
        isExisted = os.path.exists(path)
        if not isExisted:
            pf.printf(path)
            pf.printf('上面列出的路径不存在，请设置正确路径！')
            return
        else:
            pf.printf('目录[' + path + ']存在,正在读取...')
        files = os.listdir(path)  # 获取当前文档下的文件
        abandon_files = ["file0.page", "file1.page"]
        for file in files:
            file_name = os.path.basename(file)
            if file_name in abandon_files:
                os.remove(path + file_name)
        files = os.listdir(path)  # 获取当前文档下的文件
        # 先按照文件名的第二个数字排列
        files_cut_sorted_1 = sorted(files, key=lambda x: int(x[:-4].split('_')[1]))
        # 再按照文件名的第一个数字排列
        files_cut_sorted_2 = sorted(files_cut_sorted_1, key=lambda x: int(x[:-4].split('_')[0]))

        list_stress = []
        for file in files_cut_sorted_2:
            file_content = open(path + os.path.basename(file), 'rt')
            if mode == 'h':
                first_line = file_content.read()
                each_point_stress = first_line.split()
                list_stress.append(list(map(float, each_point_stress)))
            elif mode == 'v':
                list_everyfile = []
                for line in file_content:
                    list_everyline = line.split()
                    list_everyfile.append(float(list_everyline[1]))
                list_stress.append(list_everyfile)
            else:
                pass
            file_content.close()
        return list_stress
