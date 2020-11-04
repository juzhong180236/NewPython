import pandas as pd
from sklearn import tree
from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
import graphviz
import matplotlib.pyplot as plt

boston = load_boston()
# print(boston)
regressor = tree.DecisionTreeRegressor(random_state=0)
# data = pd.concat([pd.DataFrame(boston.data), pd.DataFrame(boston.target)], axis=1)
# 不需要再分训练集和测试集，scroing是衡量标准，默认是r2
score = cross_val_score(regressor,
                        boston.data,
                        boston.target,
                        cv=10,
                        scoring='neg_mean_squared_error',
                        )
print(score)
