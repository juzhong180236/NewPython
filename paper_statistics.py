import matplotlib.pyplot as plt
import numpy as np

b = np.arange(2003, 2021, 1)
a = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 24, 80, 290, 551]
plt.figure(figsize=(16, 10), dpi=100)
plt.xlabel("Publication Year", fontsize=24)
plt.ylabel("Number of Papers", fontsize=24)
x_ticks = np.arange(2003, 2021, 1)
plt.xticks(x_ticks, rotation=30)
plt.tick_params(labelsize=16)
plt.bar(b, a)
plt.savefig(r'C:\Users\laisir\Desktop\c.png', bbox_inches='tight')
plt.show()