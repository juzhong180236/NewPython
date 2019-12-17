import numpy as np
import matplotlib.pyplot as plt
from RBF_crane import RBF

# from smt.surrogate_models import RBF

xt = np.array([[0, 1], [1, 2], [3, 4.0], [3, 5], [3, 5]])
yt = np.array([1, 2, 3, 4, 5])
max_distance_list = []
for i in range(xt.shape[0]):
    # print(np.linalg.norm(yt - yt[i]))
    print([np.linalg.norm(m) for m in xt - xt[i]])
    print(np.sqrt(np.sum((xt - xt[i]) ** 2, axis=-1)))
    # print(np.linalg.norm(xt - xt[i]))
    max_distance_list.append(max([np.linalg.norm(m) for m in xt - xt[i]]))
# print(max_distance_list)
std = max(max_distance_list) / (2 * xt.shape[0])
# print(std)
# print((np.sum(np.abs(xt[0] - xt))) ** 2)
#
# aa = [1, 1]
# aa1 = np.array(aa)
# print(np.array([3]) + 2)

# Y_pre1 = RBF('mq')
# Y_pre1.fit(xt, yt)
# y_Pre1 = Y_pre1.predict(d_pred)
# print(xt)
# sm = RBF(d0=5)
# sm.set_training_values(xt, yt)
# sm.train()

# num = 100
# x = np.linspace(0.0, 4.0, num)
# y = sm.predict_values(x)
#
# plt.plot(xt, yt, "o")
# plt.plot(x, y)
# plt.xlabel("x")
# plt.ylabel("y")
# plt.legend(["Training data", "Prediction"])
# plt.show()
