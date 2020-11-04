import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
import matplotlib.pyplot as plt

# 决策树是一个需要很多数据训练的模型
"""读取csv文件"""
data = pd.read_csv('../data/Titanic_data/train.csv')
"""显示数据"""
# 显示列表的概括信息
# data.info()
# 显示数据表的前n行信息
# print(data.head(6))  # 默认是值展示5行
"""删除特征"""
# data = data.drop(['TV', 'Radio'], axis=1) # 不覆盖删除
data.drop(['Ticket', 'Name', 'Cabin'], inplace=True, axis=1)  # 根据表头删除列 # inplace=是否覆盖原先的数据表，axis=删除1轴
# data.drop([0, 1], inplace=True)  # 根据索引删除行
# print(data.head(6))
"""填补缺失值"""
# data['Age'] = data['Age'].fillna(data['Age'].mean())  # fillna
data['Age'].fillna(data['Age'].mean(), inplace=True)  # fillna
"""删除缺失值"""
data.dropna(axis=0, inplace=True)  # 默认axis=0
# data.info()
"""将特征数据转换为数字"""
# 取出某一特征去重后元素的ndarray，并转为list
# print(data['Embarked'].unique())
labels = data['Embarked'].unique().tolist()
# 使用apply对data['Embarked']中的每一个元素执行label.index获取其索引，并赋值给data['Embarked']
data['Embarked'] = data['Embarked'].apply(lambda x: labels.index(x))  # 少于10个可以用这个方法
# print(data['Embarked'])
# 直接使用astype改变ndarray中所有数据的类型，将True和False改为1,0
data['Sex'] = (data['Sex'] == "male").astype('int')
# print(data['Sex'])
# print(data.head(6))

"""取出特征值和标签值"""
x = data.iloc[:, data.columns != 'Survived']
y = data.iloc[:, data.columns == 'Survived']
# print(y)
"""将数据分为训练集和测试集"""
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=1)
# print(x_train)
"""重设索引"""
# 索引被打乱后，应该将索引重设为以0开始的数
for i in x_train, x_test, y_train, y_test:
    i.index = range(i.shape[0])
# print(x_train)
"""建立模型"""
clf = DecisionTreeClassifier(random_state=1)
clf = clf.fit(x_train, y_train)
# 不使用交叉验证
# score = clf.score(x_test, y_test)
# print(score)
# 使用交叉验证
score_cv = cross_val_score(clf, x, y, cv=10).max()
# print(score_cv)

"""在不同的剪枝参数下模型的r2"""
tr = []
te = []
for i in range(10):
    clf = DecisionTreeClassifier(random_state=1,
                                 max_depth=i + 1,
                                 criterion='entropy',
                                 )
    clf = clf.fit(x_train, y_train)
    score_tr = clf.score(x_train, y_train)
    score_te = cross_val_score(clf, x, y, cv=10).mean()
    tr.append(score_tr)
    te.append(score_te)
# print(max(te))
plt.plot(range(1, 11), tr, label='train')
plt.plot(range(1, 11), te, label='test')
plt.xticks(range(1, 11))
plt.legend()
plt.show()

"""使用网格搜索 

能够同时调整多个参数的技术，枚举技术，计算量大，所以要定好搜索范围

"""
clf = DecisionTreeClassifier(random_state=1,
                             max_depth=i + 1,
                             criterion='entropy',
                             )
# gini_threholds = np.linspace(0,0.5,50) entropy_threholds = np.linspace(0,0.5,50)
parameters = {'criterion': ['gini', 'entropy'],
              'splitter': ['best', 'random'],
              'max_depth': [*range(1, 8)],
              'min_samples_leaf': [*range(1, 50, 10)],
              'min_impurity_decrease': [*np.linspace(0, 0.5, 10)]  # 根据gini系数和entropy来定
              }

GS = GridSearchCV(clf, parameters, cv=10)
GS.fit(x_train, y_train)
print(GS.best_params_)  # 根据已输入的参数和参数取值，返回最佳参数组合
print(GS.best_score_)  # 网格搜索后的评判标准
