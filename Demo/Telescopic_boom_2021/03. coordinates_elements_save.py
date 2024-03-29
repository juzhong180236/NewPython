from Demo.Telescopic_boom_2021.libs.element_data import ElementData
import json

"""
因为ansys中的文件顺序（也就是工况顺序）是乱序排列，所以要使用filename_sort将文件排列好后进行存储
"""
path_prefix = r"C:\Users\asus\Desktop\Code\DT_Telescopic_Boom_v1.0\APP_models\\"
# path_switch = 'rbf_correct_model'
path_switch = r'pre_telescopic_boom\\'
# 读取路径(读pre)
path_four_read = path_prefix + path_switch

for i in range(16):
    # for i in [7, 8]:
    file_name = str(i + 1) + "_1"

    elements = open(path_four_read + r'elements_sort\\' + file_name + '.txt', 'rt')
    elements_str = elements.read()
    elements_list = elements_str.split("C")
    ele_result_list = []
    for ele_str in elements_list:
        ele_component_list = []
        temp_list = ele_str.strip().split("\n")
        for temp_list_child in temp_list:
            _list = temp_list_child.split()
            ele_number = int(_list[0])
            node_1 = int(_list[1])
            node_2 = int(_list[2])
            node_3 = int(_list[3])
            node_4 = int(_list[4])
            node_5 = int(_list[5])
            node_6 = int(_list[6])
            node_7 = int(_list[7])
            node_8 = int(_list[8])
            ele_component_list.append(
                [ele_number, node_1, node_2, node_3, node_4,
                 node_5, node_6, node_7, node_8])
        ele_result_list.append(ele_component_list)
    elements.close()

    ele_data = ElementData(geometry_type=['3D4_P'], data_list=ele_result_list)
    # list_ele_surface_list = ele_data.surfaceEle_Sequence_aerofoil()
    set_ele_surface_list = ele_data.set_SurfaceEle_aerofoil()
    # 在Three.js中可用的索引数据
    ele_data_save = ele_data.surfaceEle_Real_Sequence_aerofoil(
        path_four_read + r'coordinates_sort\\' + file_name + '.txt')

    coordinates = open(path_four_read + r'coordinates_sort\\' + file_name + '.txt', 'rt')
    coordinates_str = coordinates.read()
    coordinates_list = coordinates_str.split("C")
    cd_result_list = []
    cd_result_list_negative = []
    # 命名为C_1到C_4的Component，共4个Components，即4次循环
    for i_cd_list, _ in enumerate(coordinates_list):
        cd_component_list = []
        cd_component_list_negative = []
        temp_list = coordinates_list[i_cd_list].strip().split("\n")
        # 每个Component中的坐标，应力，位移个数。根据Component的不同循环次数不同
        for i_list_child, _ in enumerate(temp_list):
            _list = temp_list[i_list_child].split()
            cd_index = int(_list[0])
            if cd_index in set_ele_surface_list[i_cd_list]:
                cd_x = float(_list[1])
                cd_y = float(_list[2])
                cd_z = float(_list[3])
                cd_component_list.extend([cd_x, cd_y, cd_z])
                cd_component_list_negative.extend([-cd_x, cd_y, cd_z])
        cd_result_list.append(cd_component_list)
        cd_result_list_negative.append(cd_component_list_negative)

    coordinates.close()
    dict_rbf_model = {
        "coordinates": cd_result_list,
        "coordinates_negative": cd_result_list_negative,
        "elements_index": ele_data_save,

        # "stress_w": list_w_stress,
        # "stress_step": s_step,
        # "stress_min": s_min,
        #
        # "deformation_w": list_w_dSum,
        # "deformation_step": d_step,
        # "deformation_min": d_min,
        #
        # "y_w": list_w_y,
        # "z_w": list_w_z,
        #
        # "stds": stds,
        # "x_train": x_train,
        # "rbf_type": rbf_type,
    }

    json_rbf_model = json.dumps(dict_rbf_model)
    with open(path_prefix + "sort_sequence/" + file_name + "_" + path_switch[4:-2] + "_rbf.json", "w") as f:
        json.dump(json_rbf_model, f)
    print("\r" + str(i + 1) + '/16 json file(s) have been created...', end="")
