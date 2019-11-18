from Gene_Algorithm import GA, GA_TSP
from Gene_Algorithm import ranking_linear, ranking_raw, crossover_2point, selection_roulette_2, mutation
import numpy as np


# 定义锦标赛选择方法: 从群体中随机抽取tourn_size个，找出tourn_size中适应度函数值最大的；
# 重复size_pop（种群数量）次，确保下一代种群数量保持一致。
def selection_tournament(self, tourn_size):
    FitV = self.FitV   #适应度函数
    sel_index = []
    for i in range(self.size_pop):
        aspirants_index = np.random.choice(range(self.size_pop), size=tourn_size)
        # 在size_pop的范围内随机抽取tourn_size个
        sel_index.append(max(aspirants_index, key=lambda i: FitV[i]))
    self.Chrom = self.Chrom[sel_index, :]  # next generation
    return self.Chrom


demo_func = lambda x: x[0] ** 2 + (x[1] - 0.05) ** 2 + x[2] ** 2
# 定义目标函数，此函数中包含三个变量
ga = GA(func=demo_func, n_dim=3, size_pop=100, max_iter=500, lb=[-1, -10, -5], ub=[2, 10, 2])
# GA函数的参数输入： 目标方程，维数，种群数量，最大迭代次数，自变量上下限

#  定义线性排序，定义交叉方式（两点交叉）  定义变异   定义选择机制（锦标赛选择）
ga.register(operator_name='ranking', operator=ranking_linear). \
    register(operator_name='crossover', operator=crossover_2point). \
    register(operator_name='mutation', operator=mutation). \
    register(operator_name='selection', operator=selection_tournament, tourn_size=3)
best_x, best_y = ga.run()
print('best_x:', best_x, '\n', 'best_y:', best_y)
