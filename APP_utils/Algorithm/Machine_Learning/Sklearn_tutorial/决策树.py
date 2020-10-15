import pandas as pd
from sklearn import tree
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
import graphviz

"""
[1] 如何从数据表中找出最佳节点和最佳分枝
[2] 如何让决策树停止生长，防止过拟合
"""
"""加载数据"""
wine = load_wine()
# print(wine)
# print(wine.data)
# print(wine.target)
"""将特征与标签合并"""
data = pd.concat([pd.DataFrame(wine.data), pd.DataFrame(wine.target)], axis=1)
# print(data)
# print(wine.feature_names)
# print(wine.target_names)
"""测试集与训练集分开"""
x_train, x_test, y_train, y_test = train_test_split(wine.data, wine.target, test_size=0.3, random_state=7)
# print(x_train.shape)

"""
criterion衡量不纯度最优指标的不同标准

random_state用来设置分枝中的随机模式的参数，默认是None，高维数据随机性会更明显，低维数据，随机性基本不会显现

splitter也是用来控制决策树的随机选项的，有best和random两个值，best会根据feature_importances_来分枝，
而random会更加随机，树会更深，对训练集的拟合会降低，是防止过拟合一种方式

在不加限制条件的基础上，一棵决策树会生长到衡量不纯度指标最优，或者没有更多的特征可用为止，这样的决策树往往会过拟合。
它会在训练集上表现很好，在测试集上表现却很糟糕。我们收集的样本数据不可能和整体的状况完全一致，如果一棵决策树对训练
数据有了过于优秀的解释性，它找出的规则必然包含了训练样本中的噪声，并使它对未知数据的拟合程度不足。

为了使决策树有更好的泛化性，要对决策树进行剪枝，剪枝策略对决策树影响巨大，正确的剪枝策略是优化决策树算法的核心
sklearn提供了各种不同的剪枝策略
max_depth:限制树的最大深度，超过设定深度的树枝全部剪掉，用的最广泛的剪枝参数，在高纬度低样本量的时候非常有效，
决策树多生长一层，对样本量的需求就会增加一倍。实际使用中，建议从3开始尝试

min_samples_leaf限定，一个节点在分枝后的每个子节点都必须包含至少min_samples_leaf个训练样本，否则分枝就不会发生，
或者分枝会朝着满足每个子节点都包含min_samples_leaf个样本的方向去发生，搭配max_depth使用，在回归树中有神奇的效果，
可以让模型变得更加平滑。这个参数的数量设置得太小会引起过拟合，设置的太大就会阻止模型学习数据。一般来说，建议从=5开始。
有时候训练集和测试集差距很大，就需要把这个改为浮点数，从而设置一个百分比数。

min_samples_split限定，一个节点必须包含至少min_samples_split个训练样本，才被允许分枝。


"""
"""创建、训练并给模型评分"""
# 模型
clf = tree.DecisionTreeClassifier(criterion='entropy',
                                  random_state=30,
                                  splitter='random',
                                  # max_depth=3, #这个模型得7层才最优
                                  # min_samples_leaf=10,
                                  # min_samples_split=26,
                                  )
clf = clf.fit(x_train, y_train)
# 训练集打分
score_train = clf.score(x_train, y_train)
print(score_train)
# 测试集打分
score = clf.score(x_test, y_test)  # 返回预测的准确度accuracy
print(score)
"""将决策树画图"""
feature_names = ['酒精', '苹果酸', '灰', '灰的碱性', '镁', '总酚', '类黄酮', '非酚类', '花青素', '颜色强度', '色调', 'od280/od315稀释葡萄酒', '脯氨酸']
dot_data = tree.export_graphviz(clf,  # 决策树名称
                                # out_file=None,
                                feature_names=feature_names,  # 特征名字
                                class_names=['琴酒', '雪梨', '贝尔摩德'],  # 标签名字
                                filled=True,  # 给画的图中的框填充颜色
                                rounded=True,  # 给画出的框加圆边
                                )
graph = graphviz.Source(dot_data)
graph.view()
# graph.render('tree')
"""特征重要性"""
# print(clf.feature_importances_)
# print([*zip(feature_names, clf.feature_importances_)])
