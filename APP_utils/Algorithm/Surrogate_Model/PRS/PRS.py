import APP_utils.Algorithm.Surrogate_Model.PRS.bp_complicated_PRS as bp_com
import APP_utils.Algorithm.Surrogate_Model.PRS.simple_PRS as simple
import APP_utils.Algorithm.Surrogate_Model.PRS.simple_multiple_PRS as simple_m
import APP_utils.Algorithm.Surrogate_Model.PRS.stepwise_complicated_PRS as sw_com


class PRS(object):
    """ 代理模型PRS【bp、有/无常数项交叉、】

        def __init__(self, name='full'):
        选择PRS类，默认为有交叉项
        ['full', 'bp', 'zi', 'simple', 'simple_m', 'stepwise']分别为
        有交叉项，向后传播，截距为零，无交叉项一维，无交叉项多维，逐步回归
        self.name = name
        self.prs = None

        NOTE: matlab中默认的full mode和python的simple mode相同
    """

    def __init__(self, name='simple', m=3):
        self.name = name
        self.m = m
        self.prs = None
        if self.name in ['full', 'bp', 'zi']:
            self.prs = bp_com.PRS(name=self.name, m=self.m)
        elif self.name == 'simple':
            self.prs = simple.PRS(m=self.m)
        elif self.name == 'simple_m':
            self.prs = simple_m.PRS(m=self.m)
        elif self.name == 'stepwise':
            self.prs = sw_com.PRS(m=self.m)
            # 有其他的继续往下加

    def calc_gram_matrix(self, X):
        return self.prs.calc_gram_matrix(X)

    def fit(self, Y):
        return self.prs.fit(Y)

    def predict(self, X_Pre):
        return self.prs.predict(X_Pre)


if __name__ == "__main__":
    pass
