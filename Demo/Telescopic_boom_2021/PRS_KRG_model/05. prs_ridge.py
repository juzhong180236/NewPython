from Demo.Telescopic_boom_2021.libs.element_data import ElementData
from APP_utils.Algorithm.Surrogate_Model.PRS.bp_complicated_PRS import PRS
import Demo.Telescopic_boom_2021.coordinate_transform.coordinate_transform as ct
import json
import numpy as np
from scipy.interpolate import griddata
import pandas as pd

"""
3.3度的伸缩臂
"""
path_prefix = r"H:\Code\DT_Telescopic_Boom_v2.0\APP_models\\"
path_switch = r'pre_telescopic_boom_v1.0\Ridge\\'

# 读取路径(读pre)
path_read = path_prefix + path_switch
"""
预测的输入
"""
data_train = pd.read_csv(path_read + 'Bianfu_shuju.txt', sep='\t', names=['载荷', '角度', '位移', '油压'])
x_train = data_train.values[:, 0:3]
y_train = data_train.values[:, 3]
print("The model is building...")
prs_type = 'full'
prs_force = PRS(m=3)
m = prs_force.m
gram_matrix = prs_force.calc_gram_matrix(x_train)
prs_force.gram_matrix = gram_matrix
w_force = prs_force.fit(y_train)

dict_prs_model = {
    "force_w": w_force,
}
json_prs_model = json.dumps(dict_prs_model)
with open(path_prefix + r"pre_telescopic_boom_v3.0\prs\\" + prs_type + r"\\" + path_switch[4:-13] + "_f_prs.json", "w") as f:
    json.dump(json_prs_model, f)
