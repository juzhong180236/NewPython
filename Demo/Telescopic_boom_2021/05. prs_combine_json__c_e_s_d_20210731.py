import json

"""
因为json字符串中对象种类过多，load第一次解析出来的是str，再loads一次才能是字典对象
"""
path_prefix = r"H:\Code\DT_Telescopic_Boom_v1.0\APP_models\\"

path_switch = r'pre_telescopic_boom\\'

with open(path_prefix + r"sort_sequence\1_1_" + path_switch[4:-2] + "_rbf.json",
          "r") as f:
    dict_c_e = json.loads(json.load(f))

with open(path_prefix + path_switch[4:-2] + "_s_d_prs.json",
          "r") as f:
    dict_s_d = json.loads(json.load(f))

for i in range(4):
    dict_result = {
        "coordinates": dict_c_e["coordinates"][i],
        "coordinates_negative": dict_c_e["coordinates_negative"][i],
        "elements_index": dict_c_e["elements_index"][i],
        "stress_w": dict_s_d["stress_w"][i],
        "deformation_w": dict_s_d["deformation_w"][i],
        "m": dict_s_d["m"],
        "x_train": dict_s_d["x_train"],
        "prs_type": dict_s_d["prs_type"],
    }
    with open(path_prefix + r"prs\\" + dict_s_d["prs_type"] + r"\\" + path_switch[4:-2] + "_component_" + str(
            i + 1) + "_prs.json", "w") as f:
        json.dump(dict_result, f)
