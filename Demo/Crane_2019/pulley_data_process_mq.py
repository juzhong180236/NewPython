import numpy as np
from data_to_file import DataToFile

path_switch = 'rbf_correct_model'
# 读取路径(读pre)
path_four_read = r"C:\Users\asus\Desktop\Demo_DT_Crane\APP_models\\" + path_switch + r"\pre\\"
# 写入路径(写在mid)
path_four_write = r"C:\Users\asus\Desktop\Demo_DT_Crane\APP_models\\" + path_switch + r"\post_mq_coord_dop\\"
# 网格类型
geometry_type = ['3D4']
# 训练自变量
degreeArr = [0, 21, 42, 63]
forceArr = [125, 250, 375, 500]
combine = []
for iDegree in range(len(degreeArr)):
    for iForce in range(len(forceArr)):
        combine.append((degreeArr[iDegree], forceArr[iForce]))
fd = np.array(combine)
fd_flat = fd.flatten()
# 训练模型
dtf = DataToFile(path_four_read, path_four_write, geometry_type)
dtf.dataToPostFile(v_fd=fd, rbf_type='mq')
# dtf.dataToMidFile()
