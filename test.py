import numpy as np

#
#
# # def b(x, y, x1, y1):
# #     return np.sqrt(np.square(x - x1) + np.square(y - y1))
# #
# #
# # def a(x):
# #     return 100 * np.exp(-0.3 * x)
# #
# #
# # # print(b(61, 139, 63, 140))
# # # print(a(b(61, 139, 63, 140)))
# # # print(a(b(61, 139, 64, 129)))
# # # print(a(b(63, 140, 64, 129)))
# #
# # x = [[2, 4, 6], [3, 5, 6]]
# # # print(np.linalg.norm(x) ** 2)
# # #
# # # m = np.array(50)
# # # print(m.shape)
# # # print(m.ndim)
# # # print(0.001 / 10)
# # # print(0.01 // 10)
# # # print(int(1.1))
# # # mm = [100, 5454]
# # # print(list(map(lambda n: int(np.log10(n)) + 1, mm)))
# # # print(list(map(lambda n: int(np.log2(n)) + 1, mm)))
# # delta = 0.1
# # while ((np.log2((5 - 2) / delta)) + 1) < 6:
# #     delta = delta / 10
# # print(np.random.randint(1, 2, size=3))
# #
#
# def fitnessFunction():
#     # return lambda x: 21.5 + x[0] * np.sin(4 * np.pi * x[0]) + x[1] * np.sin(20 * np.pi * x[1])
#     # return lambda x:  x[0]
#     return lambda x: np.power(x[0], 2)
#
#
# def f(fun, d):
#     print(type(fun(d)))
#
#
# # bb = np.array([100.01599316, 4.65601367])
# bb = np.array([100.01599316, 3])
# # print(np.square(bb) ** 2)
#
# # f(fitnessFunction(), bb)
# # print(np.where(bb > 1)[0][0])
# # print(np.uint8(2.5 * 0.5))
# # print(np.delete(bb, -1))
# # print(list(range(1, 1)))
# # print(np.random.choice(range(1, 15), 1, replace=False)[0])
# ccc = np.array([[3, 8], [2, 7], [5, 6]])
#
# print(ccc[:, 0].shape)
# print(ccc[:, :1].shape)
# print(ccc[0, :].shape)
# print(ccc[:1, :].shape)
# print(bb[1:])
# bbb = ccc.flat
# # for i in bbb[1:]:
#     # i.remove()
# print(ccc)

# print(np.arange(0, 300).reshape((3, 4, 5
# def getForce(force, degree):
#     print('当前载荷和角度为：' + str(force) + ',' + str(degree))
#     print('z:' + str(-force * np.cos(degree * np.pi / 180)))
#     print('y:' + str(-force * np.sin(degree * np.pi / 180)))
#
#
# forceArr = [10, 200, 400, 600]
# degreeArr = [0, 20, 40, 60]
# # combine = np.zeros(shape=(forceArr.shape[-1], degreeArr.shape[-1]))
# combine = []
#
# for iForce in range(len(forceArr)):
#     for iDegree in range(len(degreeArr)):
#         combine.append((forceArr[iForce], degreeArr[iDegree]))
#
#
# for x, y in combine:
#     getForce(x, y)
# print(len(combine))
# def linear_abs(x, c):
#     return np.abs(x - c)
#
#
# aaa = []
# forceArr_1 = np.array([[10, 20], [200, 300], [400, 600], [33, 55]])
# w = np.array([1, 2])
# # for f in forceArr_1:
# #     aaa.append(linear_abs(f, [3, 5]))
#
# print(forceArr_1.dot(w))
ddd = np.array([1, 1, 1, 1]).reshape(4, 1)
print(ddd)
aaa = np.array([[1, 2, 3, 4], [1, 1, 2, 3], [1, 1, 2, 3], [1, 1, 2, 3]])
print(aaa)
print(3 ** 2 * aaa.dot(ddd))
print(np.hstack((aaa, ddd)))
