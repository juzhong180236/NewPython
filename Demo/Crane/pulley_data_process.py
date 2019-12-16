import numpy as np
from data_to_file import DataToFile

path_switch = 'test_new_code'
# 读取路径(读pre)
path_four_read = r"C:\Users\asus\Desktop\Demo_DT_Crane\APP_models\\" + path_switch + r"\pre\\"
# 写入路径(写在mid)
path_four_write = r"C:\Users\asus\Desktop\Demo_DT_Crane\APP_models\\" + path_switch + r"\post\\"
# 网格类型
geometry_type = ['3D4']
# 训练自变量
forceArr = [125, 250, 375, 500]
degreeArr = [0, 21, 42, 63]
combine = []
for iForce in range(len(forceArr)):
    for iDegree in range(len(degreeArr)):
        combine.append((forceArr[iForce], degreeArr[iDegree]))
d = np.array(combine)
# 训练模型
dtf = DataToFile(path_four_read, path_four_write, geometry_type)
dtf.dataToPostFile(d)
