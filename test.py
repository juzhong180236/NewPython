import numpy as np
import matplotlib.pyplot as plt
import math


def R2fun(x_real, x_predict):
    return 1 - (np.sum((x_real - x_predict) ** 2) / np.sum((x_real - np.mean(x_real)) ** 2))


x = np.linspace(-np.pi, np.pi, 50)
y_sin = np.sin(x)
y_sin_ = -np.sin(x)
plt.plot(x, y_sin_, c='r')
plt.plot(x, y_sin, c='k')
plt.show()
y_real = y_sin
y_predict = y_sin_

print(np.mean(y_real))

R2 = 1 - np.sum((y_real - y_predict) ** 2) / np.sum((y_real - np.mean(y_real)) ** 2)
print('R2  1-SSE/SST  ' + str(R2))
R22 = np.sum((y_predict - np.mean(y_real)) ** 2) / np.sum((y_real - np.mean(y_real)) ** 2)
print('R2  SSR/SST    ' + str(R22))
print(R2fun(y_real, y_predict))
