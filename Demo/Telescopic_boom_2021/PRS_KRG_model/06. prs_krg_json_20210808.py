import json

"""
因为json字符串中对象种类过多，load第一次解析出来的是str，再loads一次才能是字典对象
"""
path_prefix = r"H:\Code\SANY_TB_DT\DT_Telescopic_Boom_v2.0\APP_models\\"

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

with open(path_read + r"prs\\" + prs_type + r"\\" + path_switch[4:-7] + "_delta_s_prs.json",
          "r") as f:
    dict_delta_s = json.loads(json.load(f))

with open(path_read + r"prs\\" + prs_type + r"\\" + path_switch[4:-7] + "_f_prs.json",
          "r") as f:
    dict_f = json.loads(json.load(f))

with open(path_read + r"krg\\" + path_switch[4:-7] + "_s_krg.json",
          "r") as f:
    dict_s_krg = json.loads(json.load(f))

for i in range(4):
    if i == 0:
        dict_result = {
            "coordinates": dict_c_e["coordinates"][i],
            "coordinates_negative": dict_c_e["coordinates_negative"][i],
            "elements_index": dict_c_e["elements_index"][i],
            "index_max": dict_c_e["index_max"],
            "cd_z_max": dict_c_e["cd_z_max"],
            "test_points": dict_c_e["test_points"],
            # "weld_joint": dict_c_e["weld_joint"][i:8],  # js
            "weld_joint_list": sum(dict_c_e["weld_joint"][i:8], []),  # C#

            "stress_w_jin": dict_s_d["stress_w_jin"][i],
            "deformation_w_jin": dict_s_d["deformation_w_jin"][i],
            "stress_w_hui": dict_s_d["stress_w_hui"][i],
            "deformation_w_hui": dict_s_d["deformation_w_hui"][i],
            "m": dict_s_d["m"],
            "x_train": dict_s_d["x_train"],
            "prs_type": dict_s_d["prs_type"],

            "jin_krg": dict_s_krg["jin_krg"],
            "hui_krg": dict_s_krg["hui_krg"],

            "force_w": dict_f["force_w"],
            "delta_stress_w": dict_delta_s["delta_stress_w"][i],
        }
    else:
        dict_result = {
            "coordinates": dict_c_e["coordinates"][i],
            "coordinates_negative": dict_c_e["coordinates_negative"][i],
            "elements_index": dict_c_e["elements_index"][i],
            # "weld_joint": dict_c_e["weld_joint"][i * 8:(i + 1) * 8],  # js
            "weld_joint_list": sum(dict_c_e["weld_joint"][i * 8:(i + 1) * 8], []),  # C#

            "stress_w_jin": dict_s_d["stress_w_jin"][i],
            "deformation_w_jin": dict_s_d["deformation_w_jin"][i],
            "stress_w_hui": dict_s_d["stress_w_hui"][i],
            "deformation_w_hui": dict_s_d["deformation_w_hui"][i],
            "m": dict_s_d["m"],
            "x_train": dict_s_d["x_train"],
            "prs_type": dict_s_d["prs_type"],

            "force_w": dict_f["force_w"],
            "delta_stress_w": dict_delta_s["delta_stress_w"][i],
        }
    with open(path_read + r"prs\\"
              + dict_s_d["prs_type"] + r"\\"
              + path_switch[4:-7] + "_component_" + str(i + 1) + "_prs.json", "w") as f:
        json.dump(dict_result, f)
