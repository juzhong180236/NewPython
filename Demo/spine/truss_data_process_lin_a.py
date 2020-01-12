import numpy as np
from data_to_file import DataToFile

path_prefix = r"C:\Users\asus\Desktop\DT_Crane_v2.0\APP_models\\"
# path_switch = 'rbf_correct_model'
path_switch = r'spine\\'
# 读取路径(读pre)
path_four_read = path_prefix + path_switch
# 写入路径(写在mid)
path_four_write = path_prefix + r"post\\"
# 网格类型
geometry_type = ['3D4_P']
# 训练自变量
degreeArr = [0, 1, 2, 3, 4, 5, 6]
# forceArr = [125, 250, 375, 500]
# combine = []
# for iDegree in range(len(degreeArr)):
#     for iForce in range(len(forceArr)):
#         combine.append((degreeArr[iDegree], forceArr[iForce]))
fd = np.array(degreeArr)
# fd_flat = fd.flatten()
# 训练模型
dtf = DataToFile(path_four_read, path_four_write, geometry_type)
# dtf.dataToPostFile_v2_Bysorted(v_fd=fd, rbf_type='lin_a', which_part=path_switch[4:-2])
dtf.dataToPostFile_v2_Bysorted(v_fd=fd, rbf_type='lin_a', which_part=path_switch[0:-2])
# dtf.dataToMidFile()