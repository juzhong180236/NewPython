from Demo.Telescopic_boom_2021.libs.element_data import ElementData
import json
from Demo.Telescopic_boom_2021.libs.readexcel import read_excel

"""
将kriging模型转为json格式
"""
path_prefix = r"H:\Code\DT_Telescopic_Boom_v2.0\APP_models\\"
path_switch = r'pre_telescopic_boom_v1.0\Kriging Model\\'
# 读取路径(读pre)
path_read_jin = path_prefix + path_switch + r'jin\\'

jin_s = read_excel(path_read_jin + 'model_jin_S.xlsx')
jin_x_max = read_excel(path_read_jin + 'model_jin_X_MAX.xlsx').ravel().tolist()
jin_x_min = read_excel(path_read_jin + 'model_jin_X_MIN.xlsx').ravel().tolist()
jin_beta = read_excel(path_read_jin + 'model_jin_beta.xlsx').ravel().tolist()
jin_gamma = read_excel(path_read_jin + 'model_jin_gamma.xlsx').ravel().tolist()
jin_theta = read_excel(path_read_jin + 'model_jin_theta.xlsx').tolist()
jin_ysc = read_excel(path_read_jin + 'model_jin_Ysc.xlsx').ravel().tolist()
jin_m, jin_n = jin_s.shape

jin_krg = {
    "s": jin_s.tolist(),
    "x_max": jin_x_max,
    "x_min": jin_x_min,
    "beta": jin_beta,
    "gamma": jin_gamma,
    "theta": jin_theta,
    "ysc": jin_ysc,
    "m": jin_m,
    "n": jin_n,
}

path_read_hui = path_prefix + path_switch + r'hui\\'

hui_s = read_excel(path_read_hui + 'model_hui_S.xlsx')
hui_x_max = read_excel(path_read_hui + 'model_hui_X_MAX.xlsx').ravel().tolist()
hui_x_min = read_excel(path_read_hui + 'model_hui_X_MIN.xlsx').ravel().tolist()
hui_beta = read_excel(path_read_hui + 'model_hui_beta.xlsx').ravel().tolist()
hui_gamma = read_excel(path_read_hui + 'model_hui_gamma.xlsx').ravel().tolist()
hui_theta = read_excel(path_read_hui + 'model_hui_theta.xlsx').tolist()
hui_ysc = read_excel(path_read_hui + 'model_hui_Ysc.xlsx').ravel().tolist()
hui_m, hui_n = hui_s.shape

hui_krg = {
    "s": hui_s.tolist(),
    "x_max": hui_x_max,
    "x_min": hui_x_min,
    "beta": hui_beta,
    "gamma": hui_gamma,
    "theta": hui_theta,
    "ysc": hui_ysc,
    "m": hui_m,
    "n": hui_n,
}

dict_krg_model = {
    "jin_krg": jin_krg,
    "hui_krg": hui_krg,
}

json_rbf_model = json.dumps(dict_krg_model)
with open(path_prefix + r'pre_telescopic_boom_v3.0\krg\\' + path_switch[4:-21] + "_s_krg.json", "w") as f:
    json.dump(json_rbf_model, f)
