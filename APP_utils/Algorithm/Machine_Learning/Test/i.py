import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-1.3, 1.3, 101)
i = x > 0
# print(i)
y = np.ones_like(x)
y[i] = np.power(x[i], x[i])
# print(y)

x = np.arange(1, 0, -0.001)
y = (-3 * x * np.log(x) + np.exp(-(40 * (x - 1 / np.e)) ** 4) / 25) / 2
plt.figure(figsize=(5, 7))
plt.plot(y, x, 'r-', linewidth=2)
plt.grid(True)
# plt.title('q')
plt.show()
print(np.exp(-(40 * (x - 1 / np.e)) ** 4 / 25))

