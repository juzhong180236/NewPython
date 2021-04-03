from Demo.Telescopic_boom_2021.element_data import ElementData

elements = open(r'C:\Users\asus\Desktop\elements\1_1.txt', 'rt')
elements_str = elements.read()
elements_list = elements_str.split("C")
ele_result_list = []
for ele_str in elements_list:
    ele_component_list = []
    temp_list = ele_str.strip().split("\n")
    for temp_list_child in temp_list:
        _list = temp_list_child.strip().split()
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
# print(len(ele_result_list))
# print(len(ele_result_list[0]))
# print(len(ele_result_list[1]))
# print(len(ele_result_list[2]))
# print(ele_result_list[3][-1])
ele_data = ElementData(geometry_type=['3D4_P'], data_list=ele_result_list)
ele_list_result = ele_data.surfaceEle_Sequence_aerofoil()
# print(ele_list_result[0])
# print(ele_data.set_SurfaceEle_aerofoil())
elements.close()

coordinates = open(r'C:\Users\asus\Desktop\coordinates\1_1.txt', 'rt')
coordinates_str = coordinates.read()
coordinates_list = coordinates_str.split("C")
cd_result_list = []
for cd_list in coordinates_list:
    cd_component_list = []
    temp_list = cd_list.split("\n")
    for temp_list_child in temp_list:
        _list = temp_list_child.split()
        cd_x = float(_list[1].strip())
        cd_y = float(_list[2].strip())
        cd_z = float(_list[3].strip())
        cd_component_list.extend([cd_x, cd_y, cd_z])
    cd_result_list.append(cd_component_list)
# print(len(coordinates_str.split("\n")))
# print(s.split("C")[1])
coordinates.close()
