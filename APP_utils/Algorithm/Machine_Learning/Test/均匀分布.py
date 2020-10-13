import numpy as np
import matplotlib.pyplot as plt

x = np.random.rand(5)
t = np.arange(len(x))
# plt.hist(x, 30, color='m', alpha=0.5, label="uniform distribution")
plt.plot(t, x, 'r.')
plt.legend(loc="upper left")
# plt.grid()
plt.show()
