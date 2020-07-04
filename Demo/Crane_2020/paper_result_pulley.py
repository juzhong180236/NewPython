import numpy as np
from dat_to_file_v_results import DataToFile
from ReadExcel import readExcel
from txt_file_create import text_Create

# path_data_test_d = r"C:\Users\asus\Desktop\Papers\应力\300N\300N_d.xlsx"
path_data_test_d = r"C:\Users\asus\Desktop\Papers\应力\200N\200N_d.xlsx"
# path_data_test = r"C:\Users\asus\Desktop\Papers\应力\300N\300N_angle_post.xlsx"
path_data_test = r"C:\Users\asus\Desktop\Papers\应力\200N\200N_d_post.xlsx"
# sheet_name_d = "300N_d"
sheet_name_d = "200N_d"
# sheet_name = "300N_angle"
sheet_name = "Sheet1"


# path_data_test ={"continuous sampling":""}

def read_test_data():
    data_y, data_x = readExcel(path_data_test, sheet_name,
                               row_num=35,
                               y_column=13)
    # data_x_real = []
    # data_y_mean_arr = []
    # for data in data_y:
    #     data_y_mean = []
    #     for i in range(0, len(data), 5):
    #         mean = (data[i] + data[i + 1] + data[i + 2] + data[i + 3] + data[i + 4]) / 5
    #         data_y_mean.append(mean)
    #     data_y_mean_arr.append(data_y_mean)
    # for i in range(0, len(data_x), 5):
    #     data_x_real.append(data_x[i])
    data_y_d, data_x_d = readExcel(path_data_test_d, sheet_name_d, row_num=8054,
                                   y_column=1)
    # return data_x_real, data_y_mean_arr, data_x_d, data_y_d
    return data_x, data_y, data_x_d, data_y_d


# path_prefix = r"C:\Users\asus\Desktop\Papers\paper_result_pulley\\"
# path_prefix = r"C:\Users\asus\Desktop\paper_result_pulley\\"
path_prefix = r"C:\Users\asus\Desktop\Papers\paper_result_truss\equivalent_stress_point_v2_72\\"

# path_real_stress = r'equivalent_stress_point\\'

geometry_type = ['3D4_L']
# fd_train = np.asarray([3.5, 24, 44.5, 66])
fd_train = np.arange(0, 73)
data_test = read_test_data()
list_result_w = []
for i in range(1, 9):  # 总共8个测试点
    path_real_stress = str(i) + r"\\"
    path_read_real_stress = path_prefix + path_real_stress

    # path_real_displacement = r'dopAndCoord_point\\'
    # path_read_real_displacement = path_prefix + path_real_displacement

    # 桁架
    dtf_stress = DataToFile(path_read_real_stress, path_prefix, geometry_type)
    w = dtf_stress.dataToPostFile_paper_result_pulley(fd_train, data_title='Sample Point No.' + str(i),
                                                      input_dimension=1,
                                                      which_point=i, data_test=data_test)
    list_result_w.append(w)
text_Create(path_prefix, "w", "\n".join(list_result_w))
# 天轮
# dtf_dis = DataToFile(path_read_real_displacement, None, geometry_type)
# dtf_dis.dataToPostFile_paper_result_pulley(fd_train, path_real_data=path_read_real_displacement, rbf_type=rbf_type)
# dtf_dis.dataToPostFile_paper_result_pulley(fd_train, data_type='deformation', input_dimension=1)
