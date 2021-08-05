# FREECAD_PATH = r'H:\Code\DT_Telescopic_Boom_v1.0\APP_models\pre_telescopic_boom_v2.0\Data\X_train1.txt'
# infile = open(FREECAD_PATH, 'rt')
# list_ = []
# i = 0
# for line in infile:
#     # list_everyline = line.split()
#     i += 1
#     print(line)
# print(i)
import numpy as np

a = np.array([[1, 2, 3], [4, 5, 6]])

print(a[:, 0:3])
