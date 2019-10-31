import numpy as np

a = np.array([[1, 2, 3, 4, 5],
              [6, 7, 8, 9, 6],
              [5, 6, 4, 5, 3],
              [2, 7, 8, 8, 3],
              [9, 5, 7, 8, 7],
              [4, 2, 4, 8, 6]])

q, r = np.linalg.qr(a, mode="reduced")
# print(q)
# print(r)
help(np.linalg.qr)
b = np.array([[5, 6, 9], [8, 4, 6], [7, 3, 2], [9, 8, 6]])
q1, r1 = np.linalg.qr(b, mode="complete")
print(q1)
print(r1)

aa = np.array([[2, 3], [1, 1], [2, 2]])
bb = np.array([[1, 1, 1], [5, 5, 5]])
print(aa.dot(bb))
