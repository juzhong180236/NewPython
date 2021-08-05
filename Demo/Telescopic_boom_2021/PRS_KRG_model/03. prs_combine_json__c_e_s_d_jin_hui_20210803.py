import json

"""
因为json字符串中对象种类过多，load第一次解析出来的是str，再loads一次才能是字典对象
"""
path_prefix = r"H:\Code\DT_Telescopic_Boom_v2.0\APP_models\\"

path_switch = r'pre_telescopic_boom_v3.0\\'
path_read = path_prefix + path_switch
# prs_type = 'simple_m'
prs_type = 'full'

with open(path_read + path_switch[4:-7] + "_ele_coord_prs.json",
          "r") as f:
    dict_c_e = json.loads(json.load(f))

with open(path_read + r"prs\\" + prs_type + r"\\" + path_switch[4:-7] + "_s_d_prs.json",
          "r") as f:
    dict_s_d = json.loads(json.load(f))

for i in range(4):
    dict_result = {
        "coordinates": dict_c_e["coordinates"][i],
        "coordinates_negative": dict_c_e["coordinates_negative"][i],
        "elements_index": dict_c_e["elements_index"][i],
        "stress_w_jin": dict_s_d["stress_w_jin"][i],
        "deformation_w_jin": dict_s_d["deformation_w_jin"][i],
        "stress_w_hui": dict_s_d["stress_w_hui"][i],
        "deformation_w_hui": dict_s_d["deformation_w_hui"][i],
        "m": dict_s_d["m"],
        "x_train": dict_s_d["x_train"],
        "prs_type": dict_s_d["prs_type"],
    }
    with open(path_read + r"prs\\"
              + dict_s_d["prs_type"] + r"\\"
              + path_switch[4:-7] + "_component_" + str(i + 1) + "_prs.json", "w") as f:
        json.dump(dict_result, f)