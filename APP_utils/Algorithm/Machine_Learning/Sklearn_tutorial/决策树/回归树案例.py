import numpy as np
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeRegressor

rng = np.random.RandomState(1)
x = np.sort(5 * rng.rand(80, 1), axis=0)  # 随机取点
y = np.sin(x).ravel()  # 生成正弦曲线
y[::5] += 3 * (0.5 - rng.rand(y[::5].size))  # 加噪声

regr_1 = DecisionTreeRegressor(max_depth=2)
regr_2 = DecisionTreeRegressor(max_depth=5)
regr_1.fit(x, y)
regr_2.fit(x, y)

x_test = np.arange(0.0, 5.0, 0.01)[:, np.newaxis]
y_pred_1 = regr_1.predict(x_test)
y_pred_2 = regr_2.predict(x_test)

plt.figure()
plt.scatter(x, y, edgecolor='black', c='darkorange', label='data')
plt.plot(x_test, y_pred_1, label='max_depth=2')
plt.plot(x_test, y_pred_2, label='max_depth=5')
plt.xlabel('data')
plt.ylabel('target')
plt.title('Decision Tree Regression')
plt.legend()
plt.show()
