import numpy as np
from data_to_file import DataToFile

path_switch = 'rbf_correct_model'
# 读取路径(读pre)
path_four_read = r"C:\Users\asus\Desktop\Demo_DT_Crane\APP_models\\" + path_switch + r"\pre\\"
# 写入路径(写在mid)
path_four_write = r"C:\Users\asus\Desktop\Demo_DT_Crane\APP_models\\" + path_switch + r"\post_lin_a\\"
# 网格类型
geometry_type = ['3D4']
# 训练自变量
forceArr = [125, 250, 375, 500]
degreeArr = [0, 21, 42, 63]
combine = []
for iForce in range(len(forceArr)):
    for iDegree in range(len(degreeArr)):
        combine.append((forceArr[iForce], degreeArr[iDegree]))
fd = np.array(combine)
d = np.array(degreeArr).repeat(4)
# 训练模型
dtf = DataToFile(path_four_read, path_four_write, geometry_type)
dtf.dataToPostFile(v_fd=fd, v_d=d, rbf_type='lin_a')
# dtf.dataToMidFile()
