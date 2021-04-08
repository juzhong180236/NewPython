import numpy as np
from scipy.interpolate import UnivariateSpline

# 通过人工方式添加噪声数据
sample = 30
x = np.linspace(1, 10 * np.pi, sample)
y = np.cos(x) + np.log10(x) + np.random.randn(sample) / 10

# 插值，参数s为smoothing factor
f = UnivariateSpline(x, y, s=1)
xint = np.linspace(min(x), max(x), 1000)
yint = f(xint)
import pylab as pl

pl.plot(xint, f(xint), color="green", label="Interpolation")
pl.plot(x, y, color="blue", label="Original")
pl.legend(loc="best")
pl.show()
