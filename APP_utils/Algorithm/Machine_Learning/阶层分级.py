import numpy as np

A = np.array([0.65, 0.28, 0.07, 0.15, 0.67, 0.18, 0.12, 0.36, 0.52]).reshape(3, 3)

Pi_1 = np.array([0.22, 0.68, 0.1])
Pi_2 = np.array([0.75, 0.15, 0.1])
Pi_3 = np.array([0.5, 0.3, 0.2])
for i in range(30):
    Pi_1 = Pi_1.dot(A)
    Pi_2 = Pi_2.dot(A)
    Pi_3 = Pi_3.dot(A)
    print("第" + str(i + 1) + "次\r\nPi_1", Pi_1, "\r\nPi_2", Pi_2, "\r\nPi_3", Pi_3)
