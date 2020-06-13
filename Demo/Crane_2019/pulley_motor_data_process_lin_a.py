import numpy as np
from data_to_file import DataToFile

path_prefix = r"C:\Users\asus\Desktop\DT_Crane_v2.0\APP_models\no_displacement_1\\"
# path_switch = 'rbf_correct_model'
# path_switch = r'pre_pulley_motor\\'
path_switch = r'pre_pulley_motor_360\\'
# 读取路径(读pre)
path_four_read = path_prefix + path_switch
# 写入路径(写在mid)
# path_four_write = path_prefix + r"post_more\\"
path_four_write = path_prefix + r"post_360\\"
# 网格类型
geometry_type = ['3D4_L']
# 训练自变量
degreeArr = [0, 90, 180, 270, 360]
forceArr = [125, 250, 375, 500]
combine = []
for iDegree in range(len(degreeArr)):
    for iForce in range(len(forceArr)):
        combine.append((degreeArr[iDegree], forceArr[iForce]))
fd = np.array(combine)
fd_flat = fd.flatten()
# 训练模型
dtf = DataToFile(path_four_read, path_four_write, geometry_type)
dtf.dataToPostFile_v2_Bysorted(v_fd=fd, rbf_type='lin_a', which_part=path_switch[4:-2])
# dtf.dataToMidFile()
