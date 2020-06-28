import numpy as np
from dat_to_file import DataToFile

path_prefix = r"C:\Users\asus\Desktop\DT_Crane_v3.0\APP_models_gyration_v2.0\\"

path_switch = r'pre_pedestal_gyration\\'
name = r'pre_pedestal_gyration_v2\\'
# 读取路径(读pre)
path_four_read = path_prefix + path_switch
# 写入路径
path_four_write = path_prefix + r"post_360\\"
# 网格类型
geometry_type = ['3D4_P']
# 训练自变量
degreeArr = [0, 21, 42, 64]
forceArr = [125, 250, 375, 500]
gyrationArr = [0, 22.5, 45]
combine = []

for iDegree in range(len(degreeArr)):
    for iForce in range(len(forceArr)):
        for iGyration in range(len(gyrationArr)):
            # combine.append((degreeArr[iDegree], forceArr[iForce]))
            combine.append((degreeArr[iDegree], forceArr[iForce], gyrationArr[iGyration]))
fd = np.array(combine)
# print(fd)
dtf = DataToFile(path_four_read, path_four_write, geometry_type)
dtf.dataToPostFile_v2_Bysorted(v_fd=fd, rbf_type='lin_a', which_part=name[4:-2])
