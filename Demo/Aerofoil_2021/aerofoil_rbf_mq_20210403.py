import numpy as np
from Demo.Ansys_Data_Utils_2021.model_save_to_file import ModelSaveToFile

"""2021.04.03

# """
path_prefix = r"C:\Users\asus\Desktop\Code\DT_Airplane_v2.0\APP_models\\"
# path_switch = 'rbf_correct_model'
path_switch = r'pre_aerofoil\\'
# 读取路径(读pre)
path_four_read = path_prefix + path_switch
# 写入路径(写在mid)
path_four_write = path_prefix + r"post_aerofoil\\"
# 网格类型
geometry_type = ['3D4_P']
# 训练自变量
displacement_arr = [0, 0.05, 3, 8.5, 15, 20, 25.5, 30]
fd = np.asarray(displacement_arr)
# print(fd)
# 存储模型
mstf = ModelSaveToFile(path_four_read, path_four_write, geometry_type)
mstf.dataSaveToJSON_RBF_Aerofoil(v_fd=fd, rbf_type='lin_a', which_part=path_switch[4:-2])
