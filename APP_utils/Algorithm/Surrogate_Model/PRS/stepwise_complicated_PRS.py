import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import statsmodels.api as sm
import pandas as pd


def stepwise_selection(X, y,
                       initial_list=None,
                       threshold_in=0.8,
                       threshold_out=0.9,
                       verbose=True):
    if initial_list is None:
        initial_list = []
    included = list(initial_list)
    while True:
        changed = False
        # forward step
        excluded = list(set(X.columns) - set(included))  # Gramian矩阵剩余量
        # print(list(set(X.columns)))
        # print(sm.add_constant(pd.DataFrame(X[included + [2]])))
        # print(X[included + [1]])
        # print(excluded)
        new_pval = pd.Series(index=excluded)  # Gramian矩阵剩余量类字典型数据
        # print(new_pval)
        # 算出每一列的p值
        for new_column in excluded:
            # X = pd.DataFrame(sm.add_constant(weekly[predictors].values, has_constant='add'),
            #                  columns=['const'] + weekly[predictors].columns.tolist())
            model = sm.OLS(y, pd.DataFrame(
                sm.add_constant(pd.DataFrame(X[included + [new_column]]).values, has_constant='add'),
                columns=['const'] + pd.DataFrame(X[included + [new_column]]).columns.tolist())).fit()
            new_pval[new_column] = model.pvalues[new_column]  # model.pvalues类似字典
        # print(new_pval)
        # print(model.pvalues)
        best_pval = new_pval.min()
        # print('1:'+str(best_pval))
        # print('2:'+str(threshold_in))
        if best_pval < threshold_in:
            best_feature = new_pval.idxmin()
            included.append(best_feature)
            changed = True
            if verbose:
                print('Add  {:30} with p-value {:.6}'.format(best_feature, best_pval))

        # backward step
        # model = sm.OLS(y, sm.add_constant(pd.DataFrame(X[included]))).fit()  # 计算因最小放入included所对应的预测因子
        model = sm.OLS(y, pd.DataFrame(sm.add_constant(pd.DataFrame(X[included]).values, has_constant='add'),
                                       columns=['const'] + pd.DataFrame(X[included]).columns.tolist())).fit()
        # use all coefs except intercept
        # print(model.pvalues)
        pvalues = model.pvalues.iloc[1:]
        # print(model.pvalues.iloc[0:][0])
        worst_pval = pvalues.max()  # nan if pvalues is empty
        # print(worst_pval)
        if worst_pval > threshold_out:
            changed = True
            worst_feature = pvalues.idxmax()
            included.remove(worst_feature)
            if verbose:
                print('Drop {:30} with p-value {:.6}'.format(worst_feature, worst_pval))
        if not changed:
            break
    return excluded


class PRS(object):
    ''' 代理模型PRS【bp、有/无常数项交叉、】

        def __init__(self, m=3, w=0):
        初始化PRS类，默认次数取3，权重取0
        self.m = m
        self.w = w

        def fit(self, X, Y):
        根据X，Y数据进行训练
        参数：
            X: 给定数据的输入，一维或多维
            Y: 给定数据的输出，一维
        返回：
            返回self.w权重值

        def predict(self, X_Pre):
        根据fit方法训练的模型和X_Pre，预测相应的Y_Pre
        参数：
            X_Pre: 预测数据的输入值
        返回：
            Y_Pre: 预测的输出数据
    '''

    def __init__(self, m=3, w=0, remove_index=None):
        if remove_index is None:
            remove_index = []
        self.m = m
        self.w = w
        self.remove_index = remove_index
        self.gram_matrix = None

    def calc_gram_matrix(self, X):
        list_PRS_result = []  # 存放最终的Gramian矩阵的列表
        for i in range(X.shape[0]):  # 遍历输入值X的每个元素
            arr_result = X[i]  # 输入值X的每一个元素的在每一次m（次数）的Gramian矩阵
            arr_combine = X[i]  # 输入值X的每一个元素经过m（次数）次合并的Gramian矩阵
            list_index = list(range(1, X.shape[-1] + 1))
            list_index.reverse()  # 得到初始的每一次m时的Gramian矩阵的每一行元素个数，初始为3,2,1
            for j in range(self.m - 1):  # 遍历输入值X的每个元素个次数m
                list_temp = []  # 数据与arr_result一样，类型为list
                for h in range(X.shape[-1]):  # 遍历输入值X的每个元素的每个维度
                    # print("当前Gramian矩阵的第" + str(h) + "行:" + str(list_result[-list_index[h]:len(list_result)]))
                    # x1*(x1,x2,x3), x2*(x2,x3), x3*(x3), 类似这样的式子，根据list_index中的元素，从后往前取
                    list_temp.extend(X[i][h] * arr_result[-list_index[h]:len(arr_result)])
                    # 更新list_index中的元素，更新后的list第一个元素为原list所有元素相加，第二个元素为原list去掉第一个元素后所有元素相加，以此类推
                    list_index[h] = sum(list_index[h:])
                arr_result = np.array(list_temp)  # 将list转为ndarray
                arr_combine = np.hstack((arr_combine, arr_result))  # 将ndarray组合起来作为每个元素的Gramian矩阵
                # print("当前的Gramian矩阵:" + str(list_combine))
            list_PRS_result.append(np.hstack([[1] * X.shape[-1], arr_combine]))  # 每个元素的Gramian矩阵
        PRS_result = np.array(list_PRS_result)
        self.gram_matrix = np.insert(PRS_result, 0, 1, axis=1)  # 所有元素的Gramian矩阵，将list转为ndarray
        return self.gram_matrix

    def fit(self, Y):
        self.w = np.linalg.pinv(self.gram_matrix).dot(Y)  # 根据Y和Gramian矩阵的伪逆求出权重w
        self.remove_index = stepwise_selection(pd.DataFrame(self.gram_matrix), Y)
        self.w = np.delete(self.w, self.remove_index, axis=0)
        PRS_result = np.delete(self.gram_matrix, self.remove_index, axis=1)
        return self.w, PRS_result

    def predict(self, X_Pre):
        list_pre_x = []
        for i in range(X_Pre.shape[0]):
            list_result = X_Pre[i]
            list_combine = X_Pre[i]
            list_index = list(range(1, X_Pre.shape[-1] + 1))
            list_index.reverse()
            for j in range(self.m - 1):
                list_temp = []
                for h in range(X_Pre.shape[-1]):
                    list_temp.extend(X_Pre[i][h] * list_result[-list_index[h]:len(list_result)])
                    list_index[h] = sum(list_index[h:])
                list_result = np.array(list_temp).flatten()
                list_combine = np.hstack((list_combine, list_result))
            list_pre_x.append(np.hstack([[1] * X_Pre.shape[-1], list_combine]))
        array_pre_x = np.array(list_pre_x)
        array_pre_x = np.insert(array_pre_x, 0, 1, axis=1)
        array_pre_x = np.delete(array_pre_x, self.remove_index, axis=-1)
        Y_Pre = array_pre_x.dot(self.w)
        return Y_Pre


if __name__ == "__main__":
    pass
