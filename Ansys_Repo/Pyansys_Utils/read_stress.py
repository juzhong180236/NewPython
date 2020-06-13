import os

import sys
import math
import pyansys as py
import numpy as np
import text_file_create as tfc

# os.environ["CUDA_VISIBLE_DEVICES"] = "2"  # 指定使用编号为2的GPU
# os.environ["CUDA_VISIBLE_DEVICES"] = '1'

os.environ["CUDA_VISIBLE_DEVICES"] = "0,2,3"


def read_str(read_path, write_path, split_sign='\t'):
    result = py.read_binary(read_path)
    time_values_len = len(result.resultheader['time_values'])
    for i in range(1):
        # nnum, stress = result.nodal_stress(0)
        nnum, pstress_arr = result.principal_nodal_stress(rnum=i)
        str_stress_per_time = ''
        for j, ele in enumerate(pstress_arr):
            if str(ele[0]).isdigit():
                continue
            # print(ele)
            str_stress_per_time += str(nnum[j]) + split_sign + str(ele[-1]) + '\n'
        tfc.text_Create(write_path, str(i), str_stress_per_time)


def read_list(read_path, num=3):
    if num > 6:
        return
    num = math.floor(num)
    result = py.read_binary(read_path)
    time_values_len = len(result.resultheader['time_values'])
    print(result.solution_info)
    list_disp_entire_time = []
    for i in range(time_values_len):
        nnum, disp = result.nodal_stress(i)
        list_disp_per_time = []
        for j, ele in enumerate(disp):
            disp_sum = np.sqrt(np.sum(ele[0:4] ** 2))
            # list_disp_per_time.append(nnum[j])
            list_disp_per_time.extend(list(ele[0:num]))
            list_disp_per_time.append(disp_sum)
        list_disp_entire_time.append(list_disp_per_time)
    return list_disp_entire_time


if __name__ == '__main__':
    test_read_path = r'D:\Alai\ansys_Alai\Crane\Crane_Parts_v2.0\rod\20191223 wanggedi_files\dp0\SYS-3\MECH\file.rst'
    # test_read_path = r'D:\Alai\ansys_Alai\Crane_2019\Crane_Parts_v2.0\truss\20191220_files\dp0\SYS-3\MECH\file.rst'
    test_write_path = r'D:\Alai\2\\'
    read_str(test_read_path, test_write_path)
    # print(read_list(test_read_path))
