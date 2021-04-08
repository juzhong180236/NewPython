import numpy as np
from scipy.interpolate import interp1d

# 创建待插值的数据
x = np.linspace(0, 10 * np.pi, 20)
y = np.cos(x)

# 分别用linear和quadratic插值
fl = interp1d(x, y, kind='linear')
fq = interp1d(x, y, kind='quadratic')

# 设置x的最大值和最小值以防止插值数据越界
xint = np.linspace(min(x), max(x), 1000)
yintl = fl(xint)
yintq = fq(xint)

import pylab as pl
pl.plot(xint,fl(xint), color="green", label = "Linear")
pl.plot(xint,fq(xint), color="blue", label ="Quadratic")
pl.legend(loc = "best")
pl.show()