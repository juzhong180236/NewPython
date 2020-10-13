import numpy as np
import time
import math

for j in np.logspace(0, 7, 8, dtype=np.int):

    x = np.linspace(0, 10, j)
    start = time.time()
    y = np.sin(x)
    t1 = time.time() - start

    x1 = x.tolist()
    start1 = time.time()
    for i, x_i in enumerate(x1):
        y1 = math.sin(i)
    t2 = time.time() - start1
    print(j, ":", t1, t2)
