import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score

# 决策树是一个需要很多数据训练的模型
"""读取csv文件"""
data = pd.read_csv('data/Titanic_data/train.csv')
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
print(score_cv)
