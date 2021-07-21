import json
import matplotlib.pyplot as plt
import numpy as np

path = r'C:\Users\asus\Desktop\resultv3.0.json'
file_content = open(path, 'rt')
obj = json.load(file_content)

x_list = []
y_list = []
for x in obj.keys():
    x_list.append(int(x))
for y in obj.values():
    y_list.append(round(y, 2))
print(x_list)
print(y_list)
x_ticks = np.arange(0, max(x_list) + 500, 500)
plt.rc('xtick', labelsize=5)
plt.xticks(rotation=270)
plt.xticks(x_ticks)
plt.scatter(x_list, y_list, marker=",", s=1)
plt.show()
