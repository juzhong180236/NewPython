import numpy as np
import matplotlib.pyplot as plt


class PSO(object):
    def __init__(self, population_size, max_iter, obj_func, x_bound, dim, c=2, w=0.8):
        """
        根据粒子群数量，迭代次数，目标函数，目标函数自变量上下界，自变量维数得到最优值
        :param population_size: 粒子群数量
        :param max_iter:迭代次数
        :param obj_func:目标函数
        :param x_bound:目标函数自变量上下界
        :param dim:自变量维度
        :param c: 加速系数
        :param w: 惯性权重
        """
        self.obj_func = obj_func
        self.population_size = population_size
        self.dim = dim
        self.max_steps = max_iter
        self.x_bound = x_bound
        # 加速系数
        self.c1 = self.c2 = c
        # 惯性权重
        self.w = w
        # 初始化粒子群位置
        self.x = np.random.uniform(self.x_bound[0], self.x_bound[1],
                                   (self.population_size, self.dim))
        self.v = np.random.rand(self.population_size, self.dim)  # 初始化粒子群速度
        fitness = self.calculate_fitness(self.x)
        self.p = self.x  # 个体的最佳位置
        self.pg = self.x[np.argmin(fitness)]  # 全局最佳位置
        self.individual_best_fitness = fitness  # 个体的最优适应度
        self.global_best_fitness = np.min(fitness)  # 全局最佳适应度

    def calculate_fitness(self, x):
        return self.obj_func(x, self.dim, self.population_size)

    def evolve(self):
        for step in range(self.max_steps):
            r1 = np.random.rand(self.population_size, self.dim)
            r2 = np.random.rand(self.population_size, self.dim)
            # 更新速度和权重
            self.v = self.w * self.v + self.c1 * r1 * (self.p - self.x) + self.c2 * r2 * (self.pg - self.x)
            self.x = self.v + self.x
            fitness = self.calculate_fitness(self.x)
            # 需要更新的个体
            update_id = np.greater(self.individual_best_fitness, fitness)
            self.p[update_id] = self.x[update_id]
            self.individual_best_fitness[update_id] = fitness[update_id]
            # 新一代出现了更小的fitness，所以更新全局最优fitness和位置
            if np.min(fitness) < self.global_best_fitness:
                self.pg = self.x[np.argmin(fitness)]
                self.global_best_fitness = np.min(fitness)


def Sphere(x, dim, pop_size):
    # print(x.shape)
    return np.sum(x ** 2, axis=1)


def Sum_Squares(x, dim, pop_size):
    parameters = np.repeat(np.array([np.arange(1, dim + 1)]), pop_size, axis=0)
    return np.sum(parameters * x ** 2, axis=1)


def Step(x, dim, pop_size):
    return np.sum(np.floor(x + 0.5) ** 2, axis=1)


def Quartic(x, dim, pop_size):
    parameters = np.repeat(np.array([np.arange(1, dim + 1)]), pop_size, axis=0)
    return np.sum(parameters * x ** 4, axis=1) + np.random.rand()


def Easom(x, dim, pop_size):
    return -np.cos(x[:, 0]) * np.cos(x[:, 1]) * \
           np.exp(-(x[:, 0] - np.pi) ** 2 - (x[:, 1] - np.pi) ** 2)


def Matyas(x, dim, pop_size):
    return 0.26 * (x[:, 0] ** 2 + x[:, 1] ** 2) \
           - 0.48 * x[:, 0] * x[:, 1]


def test_func(x_bound, dim, obj_func, pop_size, max_iter, c, w):
    """
    :param x_bound: 搜索空间，自变量
    :param dim: 维度
    :param obj_func: 目标函数
    :param pop_size: 粒子群数量
    :param max_iter: 最大迭代次数
    :param c: 加速系数
    :param w: 惯性权重
    :return: 最优值
    """
    pso = PSO(pop_size, max_iter, obj_func, x_bound, dim, c, w)
    pso.evolve()
    # print('{0}的最优目标函数值:{1:.2f}'.format(obj_func.__name__, pso.global_best_fitness))
    return pso.global_best_fitness


# 10 2 表示维度
dim_10_plus = 10
dim_2 = 2
# 搜索空间
x_bound_100 = [-100, 100]
x_bound_10 = [-10, 10]
x_bound_128 = [-1.28, 1.28]


def test_all_func(c, w, max_iter, pop_size):
    """
    :param c: 加速系数
    :param w: 惯性权重
    :param max_iter: 最大迭代次数
    :param pop_size: 粒子群数量
    :return: 每个目标函数最优值组成的数组
    """
    # Sphere
    value_sphere = test_func(x_bound_100, dim_10_plus, Sphere, pop_size, max_iter, c, w)

    # Sum_Squares
    value_sum_squares = test_func(x_bound_10, dim_10_plus, Sum_Squares, pop_size, max_iter, c, w)

    # Step
    value_step = test_func(x_bound_100, dim_10_plus, Step, pop_size, max_iter, c, w)

    # Quartic
    value_quartic = test_func(x_bound_128, dim_10_plus, Quartic, pop_size, max_iter, c, w)

    # # Easom
    value_matyas = test_func(x_bound_100, dim_2, Easom, pop_size, max_iter, c, w)

    # Matyas
    value_easom = test_func(x_bound_10, dim_2, Matyas, pop_size, max_iter, c, w)

    value_array = np.array([value_sphere, value_sum_squares, value_step,
                            value_quartic, value_matyas, value_easom])
    return value_array


def draw_results(para_array, which_para):
    result_array = []
    i_array = np.arange(1, len(para_array) + 1)
    for i_para, i_process in zip(para_array, i_array):
        if which_para == 'Inertia Weight':
            result = test_all_func(i_para, 0.7, 300, 60)
        elif which_para == 'Acceleration Coefficient':
            result = test_all_func(2, i_para, 300, 60)
        elif which_para == 'Max Iteration':
            result = test_all_func(2, 0.7, i_para, 60)
        elif which_para == 'Population Size':
            result = test_all_func(2, 0.7, 300, i_para)
        else:
            return
        result_array.append(result)
        print("\r程序当前已完成：" + str(round(i_process / len(i_array) * 100)) + '%', end="")
    plt.figure()
    plt.title(which_para, fontdict={'family': 'Times New Roman', 'size': 20})
    plt.xlabel('different values of parameters: ' + which_para, fontdict={'family': 'Times New Roman', 'size': 16})
    plt.ylabel('optimum', fontdict={'family': 'Times New Roman', 'size': 16})
    plt.plot(para_array, np.array(result_array).T[0], color='#0000ff', marker='+', linestyle='-.',
             label='Sphere')
    plt.plot(para_array, np.array(result_array).T[1], color='#ff0000', marker='+', linestyle=':',
             label='Sum_Squares')
    plt.plot(para_array, np.array(result_array).T[2], color='#00ff00', marker='+', linestyle='--',
             label='Step')
    plt.plot(para_array, np.array(result_array).T[3], color='#ff00aa', marker='+', linestyle='-',
             label='Quartic')
    plt.plot(para_array, np.array(result_array).T[4], color='#ffaa00', marker='+', linestyle='--',
             label='Matyas')
    plt.plot(para_array, np.array(result_array).T[5], color='#000000', marker='+', linestyle='-',
             label='Easom')
    # plt.plot(d, result_array, color='#ff00ff', marker='+', linestyle='-',
    #          label=('' if i == 0 else '_') + 'y-real')
    plt.legend()
    plt.show()


# value_sum_squares = test_func(x_bound_10, dim_10_plus, Sum_Squares, 100, 50, 2, 0.6)
"""程序入口 四个参数分别进行寻优"""

# 改变参数——加速系数
c_array = np.arange(0.0001, 3.6, 0.1)
draw_results(c_array, "Inertia Weight")

# 改变参数——惯性权重
w_array = np.arange(0.5, 0.91, 0.05)
# draw_results(w_array, "Acceleration Coefficient")

# # 改变参数——最大迭代次数
max_iter_array = np.arange(10, 500, 20)
# draw_results(max_iter_array, "Max Iteration")

# # 改变参数——粒子数量
pop_size_array = np.arange(10, 200, 10)
# draw_results(pop_size_array, "Population Size")
