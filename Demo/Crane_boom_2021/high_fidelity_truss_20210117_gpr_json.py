import numpy as np
from Demo.Ansys_Data_Utils_2021.model_save_to_file import ModelSaveToFile

path_prefix = r"H:\Code\DT_Crane_Boom_v1.0\APP_models\\"
# path_switch = 'rbf_correct_model'
path_switch = r'pre_high_fidelity_truss\\'
# 读取路径(读pre)
path_four_read = path_prefix + path_switch
# 写入路径(写在mid)
path_four_write = path_prefix + r"post_truss\\"
# 网格类型
geometry_type = ['3D4_L']
# 训练自变量
forceArr = [50, 200, 350, 500]
degreeArr = [0, 24, 48, 72]
combine = []
for iForce in range(len(forceArr)):
    for iDegree in range(len(degreeArr)):
        combine.append((forceArr[iForce], degreeArr[iDegree]))
fd = np.array(combine)
# 训练模型
mstf = ModelSaveToFile(path_four_read, path_four_write, geometry_type)
mstf.dataSaveToJSON_GPR(fd, which_part=path_switch[4:-2])
