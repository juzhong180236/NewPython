import numpy as np
from dat_to_file_v_results import DataToFile
from ReadExcel import readExcel
from txt_file_create import text_Create

path_prefix = r"C:\Users\asus\Desktop\Papers\paper_result_truss\equivalent_stress_point_v2_72_400N\\"
fd_train = np.arange(0, 73)

list_result_w = []
for i in range(1, 9):  # 总共8个测试点
    path_real_stress = str(i) + r"\\"
    path_read_real_stress = path_prefix + path_real_stress
    # 桁架
    dtf_stress = DataToFile(path_read_real_stress, path_prefix)
    w = dtf_stress.dataToPostFile_paper_result_pulley(fd_train, data_title='Sample Point No.' + str(i),
                                                      input_dimension=2,
                                                      which_point=i)
    list_result_w.append(w)
text_Create(path_prefix, "w_4", "\n".join(list_result_w))
