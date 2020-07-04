import numpy as np
from dat_to_file import DataToFile

path_prefix = r"C:\Users\asus\Desktop\\"

path_switch = r'sheft\\'
name = r'pre_truss\\'
# 读取路径(读pre)
path_four_read = path_prefix + path_switch
# 写入路径
path_four_write = path_prefix + r"post\\"
# 网格类型
geometry_type = ['3D4_P']
# 训练自变量
degreeArr = [0, 30, 60, 90, 120, 150]
forceArr = [10, 20, 30, 40, 50]
combine = []

for iDegree in range(len(degreeArr)):
    for iForce in range(len(forceArr)):
        combine.append((degreeArr[iDegree], forceArr[iForce]))
fd = np.array(combine)

dtf = DataToFile(path_four_read, path_four_write, geometry_type)
dtf.dataToPostFile_v2_Bysorted(v_fd=fd, rbf_type='lin_a', which_part=name[4:-2])
