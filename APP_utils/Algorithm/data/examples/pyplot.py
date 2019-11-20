import matplotlib.pyplot as plt
import numpy as np

# The default format string is 'b-', which is a solid blue line.
plt.plot([1, 2, 3, 4], [1, 4, 9, 16], 'ro')
plt.plot([1, 2, 3, 4], [1, 4, 9, 16])
t = np.arange(0., 5., 0.2)
# plt.plot(t, t, 'r--', t, t ** 2, 'bs', t, t ** 3, 'g^')
plt.plot(t, t, 'r--', t, t ** 2, 'bs', t, t ** 3, 'g^', markevery=2)
plt.axis([0, 50, 0, 50])
data = {'a': np.arange(50),
        'c': np.random.randint(0, 50, 50),
        'd': np.random.randn(50)}
data['b'] = data['a'] + 10 * np.random.randn(50)
data['d'] = np.abs(data['d']) * 100
# 根据data属性，可以将其他的数值变为缩写
plt.scatter('a', 'b', c='c', s='d', data=data)
# plt.scatter([5, 1, 4], [40, 30, 5], c=[0, 10, 2], s=[20, 20, 90])
plt.xlabel('entry a')
plt.ylabel('entry b')
plt.show()

names = ['group_a', 'group_b', 'group_c']
values = [1, 10, 100]

plt.figure(figsize=(9, 3))

plt.subplot(131)
plt.bar(names, values)
plt.subplot(132)
plt.scatter(names, values)
plt.subplot(133)
plt.plot(names, values)
plt.suptitle('Categorical Plotting')
plt.show()
"""
There are several ways to set line properties:
    1.  Use keyword args:
        plt.plot(x, y, linewidth=2.0)
    2.  Use the setter methods of a Line2D instance:
        line, = plt.plot(x, y, '-')
        line.set_antialiased(False) # turn off antialiasing
    3.  Use the setp() command:
        lines = plt.plot(x1, y1, x2, y2)
        # use keyword args
        plt.setp(lines, color='r', linewidth=2.0)
        # or MATLAB style string value pairs
        plt.setp(lines, 'color', 'r', 'linewidth', 2.0)
     
"""

