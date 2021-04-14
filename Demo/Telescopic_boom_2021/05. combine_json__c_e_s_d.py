import json

"""
因为json字符串中对象种类过多，load第一次解析出来的是str，再loads一次才能是字典对象
"""

path_switch = r'pre_telescopic_boom\\'

with open(r"C:\Users\asus\Desktop\Code\DT_Telescopic_Boom_v1.0\APP_models\sort_sequence\1_1_telescopic_boom_rbf.json",
          "r") as f:
    dict_c_e = json.loads(json.load(f))

# with open(r"C:\Users\asus\Desktop\Code\DT_Telescopic_Boom_v1.0\APP_models\telescopic_boom_s_d_rbf.json",
with open(r"C:\Users\asus\Desktop\telescopic_boom_s_d_rbf.json",
          "r") as f:
    dict_s_d = json.loads(json.load(f))

for i in range(4):
    dict_result = {
        "coordinates": dict_c_e["coordinates"][i],
        "coordinates_negative": dict_c_e["coordinates_negative"][i],
        "elements_index": dict_c_e["elements_index"][i],
        "stress_w": dict_s_d["stress_w"][i],
        "deformation_w": dict_s_d["deformation_w"][i],
        "stds": dict_s_d["stds"],
        "x_train": dict_s_d["x_train"],
        "rbf_type": dict_s_d["rbf_type"],
    }
    # dict_c_e.update(dict_s_d)
    with open("C:/Users/asus/Desktop/" + path_switch[4:-2] + "_component_" + str(i + 1) + "_rbf.json", "w") as f:
        json.dump(dict_result, f)
