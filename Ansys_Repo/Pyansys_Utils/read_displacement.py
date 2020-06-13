import os
import sys
import math
import pyansys as py
import numpy as np
import text_file_create as tfc


def read_str(read_path, write_path, split_sign='\t', num=3):
    def to_sci_num(origin_num):
        return '{:e}'.format(origin_num)

    if num > 6:
        return
    num = math.floor(num)
    result = py.read_binary(read_path)
    time_values_len = len(result.resultheader['time_values'])
    print(time_values_len)
    for i in range(time_values_len):
        nnum, disp = result.nodal_solution(i)
        str_disp_per_time = ''
        for j, ele in enumerate(disp):
            disp_sum = to_sci_num(np.sqrt(np.sum(ele[0:4] ** 2)))
            str_disp_per_time += str(nnum[j]) + split_sign + split_sign.join(
                map(to_sci_num, ele[0:num])) + split_sign + disp_sum + '\n'
        tfc.text_Create(write_path, str(i), str_disp_per_time)


def read_list(read_path, num=3):
    if num > 6:
        return
    num = math.floor(num)
    result = py.read_binary(read_path)
    time_values_len = len(result.resultheader['time_values'])
    print(result.solution_info)
    list_disp_entire_time = []
    for i in range(time_values_len):
        nnum, disp = result.nodal_solution(i)
        str_disp_per_time = []
        for j, ele in enumerate(disp):
            disp_sum = np.sqrt(np.sum(ele[0:4] ** 2))
            # list_disp_per_time.append(nnum[j])
            str_disp_per_time.extend(list(ele[0:num]))
            str_disp_per_time.append(disp_sum)
        list_disp_entire_time.append(str_disp_per_time)
    return list_disp_entire_time


if __name__ == '__main__':
    # test_read_path = r'D:\Alai\ansys_Alai\Crane_2019\Crane_Parts_v2.0\rod\20191223 wanggedi_files\dp0\SYS-3\MECH\file.rst'
    test_read_path = r'D:\Alai\ansys_Alai\Crane\Crane_Parts_v2.0\truss\20191220_files\dp0\SYS-3\MECH\file.rst'

    # test_read_path = r'D:\Alai\ansys_Alai\2020.1.10\peristaltic pump1231_14_0.5r\pristaltic_pump1231_files\dp0\SYS\MECH\file.rst'
    test_write_path = r'D:\Alai\1\\'
    read_str(test_read_path, test_write_path)
    # print(read_list(test_read_path))
