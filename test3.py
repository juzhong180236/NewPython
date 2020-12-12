import numpy as np

result0 = np.random.randn(2000, 2000)
result1 = np.random.randn(2000, 2000)

result = result1.dot(result0)
# 创建空的ndarray装每一个特征的样本点
# temp = np.empty([10])

# temp[0] = 1
# temp[1] = 2
# temp[2] = 3

# result[0] = temp
print(result)
