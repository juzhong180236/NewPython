import numpy as np
import sys
import time
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from matplotlib import cm
from ReadExcel import readExcel


# import timeit
# from scipy.optimize import fsolve
def gaussian(para_list, X1, X2):
    if X2.ndim != 1:
        return np.prod(np.exp(-para_list[0] * (np.abs(X1 - X2) ** para_list[1])), axis=-1)
    else:
        return np.exp(-para_list[0] * (np.abs(X1 - X2) ** para_list[1]))


class Kriging(object):
    def __init__(self, X=None, Y=None, para_array=None, max_iter=50, mp=0.01, cp=0.8, delta=0.0001):
        if X is None:
            X = np.array([])
        if Y is None:
            Y = np.array([])
        if para_array is None:
            para_array = np.array([])
        self.X = X
        self.Y = Y
        self.para_array = para_array
        self.max_iter = max_iter
        self.mp = mp
        self.cp = cp
        self.delta = delta
        self.x_normalization = None
        self.parameters = None
        self.beta = None
        self.beta_normalize = None
        self.sigma2 = None
        self.Vkriging = None

        # 根据解的精度确定染色体(chromosome)的长度——确定二进制编码的长度

    # 需要根据决策变量的上下边界来确定
    def get_encoded_length(self):
        # 每个变量的编码长度
        lengths = []
        # 根据给定的定义域（自变量的范围）来获取其二进制的长度
        for i in self.para_array:
            lower = i[0]
            upper = i[1]
            while ((np.log2((upper - lower) / self.delta)) + 1) < 6:
                self.delta = self.delta / 10
            # print((upper - lower) / delta)
            # [[-3.0, 12.1], [4.1, 5.8]]
            # res = fsolve(lambda x: ((upper - lower) * 1 / delta) - 2 ** x + 1, np.array([50]))
            # length = int(np.ceil(res[0]))
            # 得到十进制数的二进制的位数
            length = int(np.log2((upper - lower) / self.delta)) + 1
            # print(length)
            lengths.append(length)
        return lengths

    # GA NI_GA  PSO  模拟退火

    # 随机生成初始编码种群——二进制编码    (编码长度，种群大小)
    # 第一代
    def get_initial_population(self, encode_length, population_size):
        # 种群初始化
        chromosomes = np.zeros((population_size, sum(encode_length)), dtype=np.uint8)
        # 以0，1随机生成初代种群（染色体/个体的集合）
        for i in range(population_size):
            chromosomes[i, :] = np.random.randint(0, 2, sum(encode_length))  # 随机生成 encode_length个0和1
        return chromosomes

    # 染色体解码得到表现型的解，染色体=个体，每个0，1代表基因
    def decoded_chromosome(self, encode_length, chromosomes, boundary_list):
        populations = chromosomes.shape[0]  # 染色体的个数 10
        variables = len(encode_length)  # 染色体片段数（种群的个数） 2
        decoded_values = np.zeros((populations, variables))  # 解码出来的个体的存储ndarray
        for k, chromosome in enumerate(chromosomes):
            # print(k, chromosome)
            chromosome = chromosome.tolist()  # 将每个单独的染色体从ndarray转换为列表
            start = 0
            for index, length in enumerate(encode_length):
                # 将一个染色体进行拆分，得到染色体片段，也就相当于将每个二进制组拆分，得到每个变量的二进制片段
                power = length - 1
                # 将二进制转换为十进制
                decimal = 0
                for i in range(start, start + length):
                    decimal += chromosome[i] * (2 ** power)
                    power -= 1

                # 得到初始的十进制数，再次存为lower，upper
                lower = boundary_list[index][0]
                upper = boundary_list[index][1]
                # 将前面二进制和转换出的十进制缩小倍数再加上lower，得到在Lower和upper中间的十进制数
                decoded_value = lower + decimal * (upper - lower) / (2 ** length - 1)
                # (upper - lower) / (2 ** length - 1) 表示精度
                decoded_values[k, index] = decoded_value
                # 将start也就是二进制的索引位置移到染色体下一段的开始位置
                start = length
        return decoded_values
        # 得到一矩阵，最外围维度表示种群中个体数量，下一维度表示决策变量（染色体片段数或种群个数）个数

    def get_fitness_value(self, func, chromosomes_decoded):
        """
        得到适应度值和累计概率
                参数：
                    func: 求最优解的函数
                    chromosomes_decoded: 解码后的种群集合
                返回：
                    fitness_values: 染色体片段（个体）的适应度值
                    cum_probability: 每个个体被选择的累积概率
        """
        # 得到种群的染色体数（个体数）population，染色体片段数或种群数（决策变量的个数）nums
        population, nums = chromosomes_decoded.shape
        # 初始化种群的适应度值为0
        fitness_values = np.zeros((population, 1))
        # 计算适应度值,其实就是所求的函数值，因为根据函数的大小判断其是否保留，所以也叫适应度值
        # print(type(chromosomes_decoded[0, :]))
        for i in range(population):
            fitness_values[i, 0] = func(gaussian, chromosomes_decoded[i, :])
        # print(fitness_values)
        # 轮盘赌选择法，
        # 计算每个染色体被选择的概率
        probability = fitness_values / np.sum(fitness_values)
        # print(probability)
        # print(probability)
        # 得到前n个染色体被选中的概率
        cum_probability = np.cumsum(probability)
        # print(cum_probability)
        return fitness_values, cum_probability

    def select_new_population(self, chromosomes, cum_probability):
        """
        新种群选择
                参数：
                    chromosomes: 上一代种群
                    cum_probability: 累计概率
                返回：
                    new_population: 返回新一代种群
        """
        # 上一代种群的个数m.染色体片段数（或个体数）n
        m, n = chromosomes.shape
        # 新一代的种群
        new_population = np.zeros((m, n), dtype=np.uint8)
        # 随机产生m个概率值x,用于与初代累计概率进行比较
        randoms = np.random.rand(m)
        # 为保障种群的染色体数目（个体数）不变，将生成的m个随机数与上一代种群比较，再次生成新的含有m个个体的种群
        for i, random_a in enumerate(randoms):
            logical = cum_probability >= random_a
            # 当r<cum_[1]，则选择个体1，
            # 否则，选择个体k，使得：q[k-1]<r≤q[k] 成立；
            index = np.where(logical == 1)
            # 将第一个满足条件的染色体（或个体）放入新一代种群，可能会有相同个体放入多次。index是tuple,tuple中元素是ndarray
            new_population[i, :] = chromosomes[index[0][0], :]
            # 在累计概率中最后一个元素值为1，可保证index[0][0]永远不为空
        # print(new_population)
        # 返回新一代种群（二进制形式）
        return new_population

    # 定义锦标赛选择方法: 从群体中随机抽取tour_size个，找出tour_size中适应度函数值最大的；
    # 重复chromosomes（种群数量）次，确保下一代种群数量保持一致。
    def select_tournament(self, chromosomes, tour_size):
        fit_value = self.fitnessFunction  # 适应度函数
        sel_index = []
        for i in range(chromosomes):
            aspirants_index = np.random.choice(range(chromosomes), size=tour_size)
            # 在chromosomes的范围内随机抽取tour_size个
            sel_index.append(max(aspirants_index, key=lambda i: fit_value[i]))
        new_population = chromosomes[sel_index, :]  # next generation
        return new_population

    def crossover(self, population):
        """
        种群交叉
            参数：
            population: 新种群
            Pc: 交叉概率默认是0.8
            返回：
            return: 交叉后得到的新种群
        """
        # 种群的染色体数（个体数）m，每个染色体的基因数量n
        m, n = population.shape
        # 使用uint8存储，顺便取整
        numbers = np.uint8(m * self.cp)
        # 确保进行交叉的染色体个数是偶数个
        if numbers % 2 != 0:
            numbers += 1
        # 交叉后得到的新种群
        update_population = np.zeros((m, n), dtype=np.uint8)
        # 在所选择出的新种群中进行交叉，交叉过后，替换掉原来的。
        # 根据原始种群的染色体总数（个体总数）产生随机索引，比如总数为10，则从集合[0,9]中不重复抽取numbers个数字
        index = np.random.choice(range(m), numbers, replace=False).tolist()
        # 从序列range(m)中随机截取number长的片段
        # 不进行交叉的染色体进行复制（不在index里面的种群直接传给update_population）
        for i in range(m):
            # if not index.__contains__(i):
            if i not in index:
                update_population[i, :] = population[i, :]
        # crossover
        while len(index) > 0:
            # 从后向前依次选取，直至没有可以进行交叉的个体
            a = index.pop()  # a 表示index中最后一个元素值
            b = index.pop()  # b 表示index中倒数第二个元素值
            # 在一个染色体的基因序列中随机选取一个交叉点
            crossover_point = np.random.choice(range(1, n), 1, replace=False)[0]
            # 在染色体中确认交叉点的位置,也就是索引为a、b的染色体在选择的交叉点进行变换

            update_population[a, 0:crossover_point] = population[a, 0:crossover_point]
            update_population[a, crossover_point:] = population[b, crossover_point:]
            update_population[b, 0:crossover_point] = population[b, 0:crossover_point]
            update_population[b, crossover_point:] = population[a, crossover_point:]
        # 返回交叉后的种群（二进制）
        return update_population

    def mutation(self, population):
        """
        种群染色体变异
            参数：
            population: 经交叉后得到的种群
            Pm: 变异概率默认是0.01
            返回：
            return: 经变异操作后的新种群
        """
        update_population = np.copy(population)
        # 种群的染色体数（个体数）m，每个染色体的基因数量n
        m, n = population.shape
        # 计算需要变异的基因个数
        gene_num = np.uint8(m * n * self.mp)
        # 将所有的基因按照序号进行10进制编码，则共有m*n个基因
        # 随机抽取gene_num个基因进行基本位变异
        mutation_gene_index = np.random.choice(range(0, m * n), gene_num, replace=False)
        # 确定每个将要变异的基因在整个染色体中的基因座(即基因的具体位置)
        for gene in mutation_gene_index:
            # 确定变异基因位于第几个染色体
            chromosome_index = gene // n
            # 确定变异基因位于当前染色体的第几个基因位
            gene_index = gene % n
            # 变异，1变成0，0变成1
            if update_population[chromosome_index, gene_index] == 0:
                update_population[chromosome_index, gene_index] = 1
            else:
                update_population[chromosome_index, gene_index] = 0
        # 变异后的种群
        return update_population

    def fitnessFunction(self, func, para_array):
        # def fitnessFunction(self):
        """
           定义适应度函数
               参数：
               func: Kriging相关函数

               返回：
               return: 适应度函数的值
        """
        matrix = self.corelation(func, self.X, self.X, para_array)
        num = matrix.shape[-1]
        # 相关矩阵的逆矩阵
        matrixR = matrix + ((1000 + num) * np.finfo(np.float64).tiny * np.eye(num))
        inverse_matrix = np.linalg.inv(matrixR)
        # 单位向量
        F = np.ones(num)
        # 均值
        self.beta = F.T.dot(inverse_matrix).dot(self.Y) / (F.T.dot(inverse_matrix).dot(F))
        # 方差
        self.sigma2 = ((self.Y - F.dot(self.beta)).T.dot(inverse_matrix).dot(self.Y - F.dot(self.beta))) / F.shape[
            -1]
        R = np.linalg.det(matrix)
        # 自己的方法，直接用sys.float_info.min替换掉零
        # R = sys.float_info.min if R == 0 else R
        # 自己的方法，直接用 np.finfo(np.float64).tiny替换掉零
        R = np.finfo(np.float64).tiny if R == 0 else R
        # if np.linalg.det(matrix) == 0:
        #     print(np.linalg.det(matrix))
        return -self.sigma2 * (F.shape[-1] / 2) - np.log(R)

    def genetic_algorithm(self):
        # 每次迭代得到的最优解
        optimal_solutions = []
        optimal_values = []
        # 决策变量（自变量）的取值范围，维数多就增加数组元素个数，例如[[4.1, 5.8]，[8, 10]]
        # decision_variables = [[4.1, 5.8]]
        # decision_variables = [[100, 100.5], [4.1, 5.8]]
        # 得到染色体编码长度
        length_encode = self.get_encoded_length()
        # 得到初始种群编码
        chromosomes_encoded = self.get_initial_population(length_encode, 10)
        # 种群解码
        decoded = self.decoded_chromosome(length_encode, chromosomes_encoded, self.para_array)
        # evalvalues, cum_proba = get_fitness_value(fitnessFunction(), decoded)
        # 得到个体适应度值和个体的累积概率
        fitness_values, cum_individual_proba = self.get_fitness_value(self.fitnessFunction, decoded)
        for iteration in range(self.max_iter):
            # 选择新的种群
            new_populations = self.select_new_population(chromosomes_encoded, cum_individual_proba)
            # 进行交叉操作
            crossover_population = self.crossover(new_populations)
            # mutation进行变异
            mutation_population = self.mutation(crossover_population)
            # 将变异后的种群解码，得到每轮迭代最终的种群
            final_decoded = self.decoded_chromosome(length_encode, mutation_population, self.para_array)
            # 变异后的适应度值，累计概率
            fitness_values, cum_individual_proba = self.get_fitness_value(self.fitnessFunction, final_decoded)
            # 搜索每次迭代的最优解（当前是取最大值，所以是max），以及最优解对应的目标函数（十进制染色体）的取值
            # optimal_values.append(np.max(list(fitness_values)))
            optimal_values.append(np.max(list(fitness_values)))
            index = np.where(fitness_values == max(list(fitness_values)))
            optimal_solutions.append(final_decoded[index[0][0], :])
        # 从每次迭代的最优解集合中找到总体的最优解
        # optimal_value = np.max(optimal_values)
        optimal_value = np.max(optimal_values)
        # 根据全局最优解得到最优解的索引位置
        optimal_index = np.where(optimal_values == optimal_value)
        # 得到优化参数的值组成的list
        optimal_solution = optimal_solutions[optimal_index[0][0]]
        return optimal_solution

    def corelation(self, func, X, Y, para_array):
        list_result = []
        for i in range(X.shape[0]):
            if func.__name__ == 'gaussian':
                list_result.append(func(para_array, X[i], Y).ravel())
        return np.array(list_result)

    def fit(self):
        # 求得超参数值
        self.parameters = self.genetic_algorithm()
        # 训练值归一化
        self.x_normalization = self.X / (np.max(self.X, axis=0) - np.min(self.X, axis=0))
        # 相关矩阵
        matrix = self.corelation(gaussian, self.x_normalization, self.x_normalization, self.parameters)
        inverse_matrix_normalize = np.linalg.inv(matrix)
        F = np.ones(matrix.shape[-1])
        self.beta_normalize = F.T.dot(inverse_matrix_normalize).dot(self.Y) / (F.T.dot(inverse_matrix_normalize).dot(F))
        self.Vkriging = inverse_matrix_normalize.dot((self.Y - F.dot(self.beta_normalize)))
        # 相关矩阵求逆
        return self.Vkriging

    def predict(self, X_pre):
        # 预测值归一化
        x_pred_normalization = X_pre / (np.max(X_pre, axis=0) - np.min(X_pre, axis=0))
        # 相关向量
        vector = self.corelation(gaussian, self.x_normalization, x_pred_normalization, self.parameters)
        # print(vector)
        # 预测值
        Y_pre = self.beta_normalize + vector.T.dot(self.Vkriging)
        return Y_pre


if __name__ == "__main__":
    parameter_array_c = np.array([[0, 1], [1, 2]])
    # 第一组数据
    path_excel = r"C:\Users\asus\Desktop\History\History_codes\NewPython\APP_utils\Algorithm\data\Function1.xlsx"
    data_real = readExcel(path_excel, "Sheet2", 1, 20, 2)
    data_pre = readExcel(path_excel, "Sheet2", 50, 100, 2)
    start = time.perf_counter()
    # kriging = Kriging(X=data_real[0], Y=data_real[1], para_array=parameter_array_c, max_iter=50)
    # Vkriging = kriging.fit()
    # print(Vkriging)
    # data_pred = kriging.predict(data_pre[0])

    # 第二组数据
    # d = np.array([-17, -13, -9, -5, -1, 0, 1, 5, 9, 13, 17])
    # y = np.array([22.3, 16.85, 11.4, 5.9501, 0.95417, 0.5, 0.95417, 5.9501, 11.4, 16.85, 22.3])
    # d_pred = np.arange(-17, 18)
    #
    # kriging = Kriging(X=d, Y=y, para_array=parameter_array_c, max_iter=3)
    # Vkriging1 = kriging.fit()
    # y_pred = kriging.predict(d_pred)
    A_value = 0.5
    B_value = 10
    C_value = -5


    # 高保真的曲线函数表达式
    def high_fidelity_curve(x):
        return (6 * x - 2) ** 2 * np.sin(12 * x - 4)


    # 高保真的曲线函数表达式
    def low_fidelity_curve(x, A=A_value, B=B_value, C=C_value):
        return A * high_fidelity_curve(x) + B * (x - 0.5) + C

        # 低保真的曲线


    XC = np.linspace(0, 1)
    YC = low_fidelity_curve(XC)

    XC_point = np.array([0, 0.2, 0.5, 0.6, 0.9, 1])
    YC_point = low_fidelity_curve(XC_point)
    # print(YC_point)

    kriging = Kriging(X=XC_point, Y=YC_point, para_array=parameter_array_c, max_iter=3)
    Vkriging1 = kriging.fit()
    XE_PRED = np.linspace(0, 1)
    YE_pred = kriging.predict(XE_PRED)
    plt.plot(XE_PRED, YE_pred, color='#ff0000', label='Kriging data interpolation curve', linestyle=':')
    plt.plot(XC, YC, color='#ffff00', label='Kriging curve', linestyle='-')
    plt.scatter(XC_point, YC_point, color='#000000', label='low fidelity sample data', marker='s')

    print('theta和p的最优解分别是:', kriging.parameters)
    # print('最优目标函数值:', value)
    plt.figure()
    # plt.plot(data_pre[0], data_pre[1], color='#ff0000', marker='+', linestyle='-',
    #          label='z-real')
    # plt.plot(data_pre[0], data_pred, color='#0000ff', marker='+', linestyle='-.',
    #          label='z-predict')
    # plt.plot(d, y, color='#ff00ff', linestyle='-',
    #          label='y-real')
    # plt.scatter(d_pred, y_pred, color='#000000', marker='8',
    #             label='y-predict')

    # RR = 1 - (np.sum(np.square(data_pre[1] - y_pred)) / np.sum(np.square(data_pre[1] - np.mean(data_pre[1]))))
    # RR1 = 1 - (np.sum(np.square(y - y_pred)) / np.sum(np.square(y - np.mean(y))))
    # print(RR)

    # fig = plt.figure()
    # ax = fig.gca(projection='3d')
    # print(data_pre)
    # X = np.array(data_pre[0][:, 0])
    # Y = np.array(data_pre[0][:, 1])
    # Z = np.array(data_pre[1]).reshape(Y.shape[0])
    # Z_pred = np.array(y_pred)

    # print(X)
    # print(Y)
    # print(Z)
    # ax.scatter(X, Y, Z, c='#ff0000', s=30, label='dot', alpha=0.6, edgecolors='black')
    # ax.plot_trisurf(X, Y, Z, linewidth=0.2, antialiased=True)
    # ax.plot_trisurf(X, Y, y_pred, linewidth=0.2, antialiased=True, color='r')
    # ax.plot_wireframe(X, Y, Z, rstride=10, cstride=10)
    # ax.plot_surface(X, Y, Z, rstride=1, cstride=1, color='r')
    # ax.plot_surface(X, Y, Z, linewidth=0, antialiased=False)
    # ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=False)

    # cset = ax.contour(X, Y, Z, zdir='z', offset=-100, cmap=cm.coolwarm)
    # cset = ax.contour(X, Y, Z, zdir='x', offset=-40, cmap=cm.coolwarm)
    # cset = ax.contour(X, Y, Z, zdir='y', offset=40, cmap=cm.coolwarm)
    # ax.set_xlabel('X')
    # ax.set_xlim(-1, 1)
    # ax.set_ylabel('Y')
    # ax.set_ylim(-1, 1)
    # ax.set_zlabel('Z')
    # ax.set_zlim(-10, 10)
    # plt.legend()
    plt.show()
    elapsed = (time.perf_counter() - start)
    print("Time used:", elapsed)
    # 测量运行时间
    # elapsed_time = timeit.timeit(stmt=main, number=1)
    # print('Searching Time Elapsed:(S)', elapsed_time)
