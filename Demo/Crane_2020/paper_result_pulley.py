import numpy as np
from dat_to_file import DataToFile

path_prefix = r"C:\Users\asus\Desktop\papre_result_pulley\\"
# path_switch = 'rbf_correct_model'
path_real_stress = r'equivalent_stress_point\\'
# path_train_stress = r'stress_train\\'
# 读取路径(读pre)
# path_read_train_stress = path_prefix + path_train_stress
path_read_real_stress = path_prefix + path_real_stress
# 写入路径(写在mid)
# path_four_write = path_prefix + r"\\"
# 网格类型
geometry_type = ['3D4_L']
# 训练自变量
degreeArr = [0, 21, 42, 64]
forceArr = [125, 250, 375, 500]
combine = []
for iDegree in range(len(degreeArr)):
    for iForce in range(len(forceArr)):
        combine.append((degreeArr[iDegree], forceArr[iForce]))
fd = np.array(combine)
fd_flat = fd.flatten()
fd_train = np.asarray([0, 21, 42, 64])
# 训练模型
dtf = DataToFile(path_read_real_stress, None, geometry_type)
dtf.dataToPostFile_paper_result_pulley(fd_train, path_real_data=path_read_real_stress)
# dtf.dataToMidFile()
