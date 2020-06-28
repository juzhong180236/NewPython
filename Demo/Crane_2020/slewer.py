from ele_data import ElementData
from coords_data import CoordinateData
from disp_data import DispalcementData
from stre_data import StressData
from surf_data_process import SurfaceData
import txt_file_create as tfc
import numpy as np
from dat_to_file import DataToFile

path_prefix = r"C:\Users\asus\Desktop\DT_Crane_v3.0\APP_models_gyration_v2.0\\"

path_switch = r'pre_slewer\\'

# 读取路径(读pre)
path_four_read = path_prefix + path_switch

# 写入路径
path_four_write = path_prefix + r"post_360\\"

# 网格类型
geometry_type = ['3D4_P']
# 训练自变量
degreeArr = [0, 21, 42, 64]
forceArr = [125, 250, 375, 500]
combine = []
for iDegree in range(len(degreeArr)):
    for iForce in range(len(forceArr)):
        combine.append((degreeArr[iDegree], forceArr[iForce]))
fd = np.array(combine)

dtf = DataToFile(path_four_read, path_four_write, geometry_type)
dtf.dataToPostFile_v2_Bysorted(v_fd=fd, rbf_type='lin_a', which_part=path_switch[4:-2])
