import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split  # 将数据分为训练数据和测试数据
from sklearn.linear_model import Lasso, Ridge
from sklearn.model_selection import GridSearchCV  # 交叉验证

if __name__ == "__main__":
    data = pd.read_csv('data/tv_radio_newspaper.csv')
    x = data[['TV', 'Radio', 'Newspaper']]
    y = data['Sales']
    # print(x)
    # print(y)
    # 将数据分为训练数据和测试数据，random_state是为了让每次运行程序时，数据分类和前一次运行相同
    # 默认训练数据是75%，也可以直接设置数字，如100，就是100个样本为训练数据，也可以设置test_size
    x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=1, train_size=0.75)
    model = Lasso()  # 正则项
    alpha_can = np.logspace(-3, 2, 10)  # 0.01 ~ 100
    np.set_printoptions(suppress=True)  # 不使用科学计数法
    print('alpha_can = ', alpha_can)
    lasso_model = GridSearchCV(model, param_grid={'alpha': alpha_can}, cv=5)
    lasso_model.fit(x_train, y_train)
    print('超参数：\n', lasso_model.best_params_)

    # order = y_test.argsort(axis=0)
    # y_test = y_test.values[order]
    # x_test = x_test.values[order, :]
    y_hat = lasso_model.predict(x_test)
    print(lasso_model.score(x_test, y_test))  # 线性回归r2=0.9不算好
    mse = np.average((y_hat - np.asarray(y_test)) ** 2)  # Mean Squared Error
    rmse = np.sqrt(mse)  # Root Mean Squared Error
    print(mse, rmse)

    t = np.arange(len(x_test))
    mpl.rcParams['font.sans-serif'] = [u'simHei']
    mpl.rcParams['axes.unicode_minus'] = False
    plt.figure()
    plt.plot(t, y_test, 'r-', linewidth=2, label=u'真实数据')
    plt.plot(t, y_hat, 'g-', linewidth=2, label=u'预测数据')
    plt.title(u'线性回归预测模型', fontsize=18)
    plt.legend(loc='upper right')
    plt.grid()
    plt.show()
