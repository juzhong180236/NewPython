import numpy as np


# def b(x, y, x1, y1):
#     return np.sqrt(np.square(x - x1) + np.square(y - y1))
#
#
# def a(x):
#     return 100 * np.exp(-0.3 * x)
#
#
# # print(b(61, 139, 63, 140))
# # print(a(b(61, 139, 63, 140)))
# # print(a(b(61, 139, 64, 129)))
# # print(a(b(63, 140, 64, 129)))
#
# x = [[2, 4, 6], [3, 5, 6]]
# # print(np.linalg.norm(x) ** 2)
# #
# # m = np.array(50)
# # print(m.shape)
# # print(m.ndim)
# # print(0.001 / 10)
# # print(0.01 // 10)
# # print(int(1.1))
# # mm = [100, 5454]
# # print(list(map(lambda n: int(np.log10(n)) + 1, mm)))
# # print(list(map(lambda n: int(np.log2(n)) + 1, mm)))
# delta = 0.1
# while ((np.log2((5 - 2) / delta)) + 1) < 6:
#     delta = delta / 10
# print(np.random.randint(1, 2, size=3))
#

def fitnessFunction():
    # return lambda x: 21.5 + x[0] * np.sin(4 * np.pi * x[0]) + x[1] * np.sin(20 * np.pi * x[1])
    # return lambda x:  x[0]
    return lambda x: np.power(x[0], 2)


def f(fun, d):
    print(type(fun(d)))


# bb = np.array([100.01599316, 4.65601367])
bb = np.array([100.01599316, 3])
# print(np.square(bb) ** 2)

# f(fitnessFunction(), bb)
# print(np.where(bb > 1)[0][0])
# print(np.uint8(2.5 * 0.5))
# print(np.delete(bb, -1))
# print(list(range(1, 1)))
# print(np.random.choice(range(1, 15), 1, replace=False)[0])
print(bb[0:])
cc = np.zeros(bb.shape)
cc[0:0] = bb[0:0]
cc[0:] = bb[0:]
print(cc)
ccc = np.array([[3, 8], [2, 7], [5, 6]])
cccc = np.array([4, 6])
ccccc = [1, 5]

# print(((cccc - ccc) ** 2))
# print(((cccc - ccc) ** 2).ravel())
# print(ccc.shape)
# print(cccc.shape[0])
d = np.array([-17, -13, -9, -5, -1, 0, 1, 5, 9, 13, 17])


def gaussian(X1, X2):
    return X1 + X2


def corelation(func, X, Y):
    list_result = []
    for i in range(X.shape[0]):
        if func.__name__ == 'gaussian':
            list_result.append(func(X[i], Y).ravel())
    return np.array(list_result)


print(corelation(gaussian, d, d))

print(ccc / np.max(ccc, axis=0))
print(d.shape[0] == d.ndim)
print(d.ndim)
