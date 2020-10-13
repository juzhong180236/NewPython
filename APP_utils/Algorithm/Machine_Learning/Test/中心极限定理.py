import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

t = 1000
a = np.zeros(10000)
for i in range(t):
    a += np.random.uniform(-5, 5, 10000)
a /= t
plt.hist(a, bins=30, color='r', alpha=0.5)
plt.show()

da = 10
p = stats.poisson(da)
y = p.rvs(size=1000)
mx = 30
r = (0, mx)
bins = r[1] - r[0]
plt.figure(figsize=(15, 8))
plt.subplot(121)
plt.hist(y, bins=bins, range=r, color='r', alpha=0.5, density=True)  # density：归一化
t = np.arange(0, mx + 1)
plt.plot(t, p.pmf(t), 'ro-', lw=2)

N = 1000
M = 10000
plt.subplot(122)
a = np.zeros(M, dtype=np.float)
p = stats.poisson(da)
for i in np.arange(N):
    a += p.rvs(size=M)
a /= N
plt.hist(a, bins=20, color='r', alpha=0.5, density=True)

plt.show()
