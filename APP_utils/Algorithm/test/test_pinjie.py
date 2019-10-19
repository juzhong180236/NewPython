import numpy as np


# # np.concatenate
# # arr1 = np.concatenate((np.array([2, 3]), 2))
# arr2 = np.concatenate((np.array([[2, 3]]), np.array([[2, 5]])), axis=0)
# arr3 = np.concatenate((np.array([[2, 3]]), np.array([[2, 5]])))
# # np.append
# arr11 = np.append(np.array([[2, 3], [3, 4]]), 4)
# arr12 = np.append(np.array([[2, 3]]), np.array([[2, 5]]), axis=0)
# arr13 = np.append(np.array([[2, 3]]), np.array([[2, 5]]))
# # print(arr1)
# print(arr2)
# print(arr3)
#
# print(arr11)
# print(arr12)
# print(arr13)
#
# arr21 = np.empty((3, 4))
# arr21[0][2] = 1
# print(arr21)
#
# arr31 = np.array([3, 4])
# arr32 = np.array([5, 6])

# arr41 = np.array([[1, 2, 3], [2, 3, 5], [4, 5, 7]])
# max_distance_lsit = []
# for i in range(len(arr41)):
#     max_distance_lsit.append(max([np.linalg.norm(m) for m in arr41 - np.array([arr41[i]])]))
# max_distance = max(max_distance_lsit)
#
# np.repeat(max_distance, 2)
# print(max_distance)
def calc_max_eleNumber(eachNum, expNum):
    result = eachNum
    for num in range(expNum):
        result = result + result * eachNum
    return result


#
# arr41 = np.array([[2, 3, 4], [2, 3, 5], [4, 5, 7]])
# # max_distance_lsit = []
# # for i in range(len(arr41)):
# #     max_distance_lsit.append(max([np.linalg.norm(m) for m in arr41 - np.array([arr41[i]])]))
# # max_distance = max(max_distance_lsit)
# expNumber = 3
# list_final_result = []
# for i in range(arr41.shape[0]):  # m
#     # list_temp_ss = []
#     list_result = arr41[i]
#     list_combine = arr41[i]
#     list_each_result = []
#     # ss = arr41[i]
#     for j in range(expNumber):
#         list_temp = [m * list_result for m in np.array(arr41[i])]
#         # list_temp_ss = [m * ss for m in np.array(arr41[i])]
#         # ss = np.concatenate((ss, np.array(list_temp_ss).flatten()))
#         list_result = np.array(list_temp).flatten()
#         list_combine = np.concatenate((list_combine, list_result))
#     print(list_combine)

# list_final_result.append(np.array(list_each_result).flatten())

# print(list_final_result)
# print(ss[len(ss) - calc_max_eleNumber(arr41.shape[-1], expNumber):len(ss)])
# list_temp.append(X[i] ** j)
# data_PRS_result[i][j] = X[i] ** j
# list_PRS_result.append(np.array(list_temp).ravel())

arr51 = np.array([[2, 3, 6], [3, 5], [7]])
print(arr51[1] * np.array([4]))
arr52 = np.array([2, 3, 6, 3, 5, 7])
print(arr52[-6:len(arr52)])
