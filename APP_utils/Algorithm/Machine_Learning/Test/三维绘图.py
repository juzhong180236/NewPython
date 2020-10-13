import numpy as np
import matplotlib.pyplot as plt

x, y = np.ogrid[-3:3:7j, -3:3:7j]
# 2
x1, y1 = np.mgrid[-3:3:101j, -3:3:101j]
# 3:和2结果一样
u = np.linspace(-3, 3, 7)
x2, y2 = np.meshgrid(u, u)
# print(x)
# print(y)
# print(x1)
# print(y1)
z = x1 * y1 * np.exp(-(x1 ** 2 + y1 ** 2) / 2) / np.sqrt(2 * np.pi)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(x1, y1, z, rstride=5, cstride=5, cmap=plt.get_cmap('Blues'), lw=0.5)
plt.show()
