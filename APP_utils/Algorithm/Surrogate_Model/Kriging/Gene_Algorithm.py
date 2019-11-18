#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/8/20
# @Author  : github.com/guofei9987


import numpy as np
import types
# Copyright 2007 Google, Inc. All Rights Reserved.
# Licensed to PSF under a Contributor Agreement.

"""Abstract Base Classes (ABCs) according to PEP 3119."""


def abstractmethod(funcobj):
    """A decorator indicating abstract methods.

    Requires that the metaclass is ABCMeta or derived from it.  A
    class that has a metaclass derived from ABCMeta cannot be
    instantiated unless all of its abstract methods are overridden.
    The abstract methods can be called using any of the normal
    'super' call mechanisms.

    Usage:

        class C(metaclass=ABCMeta):
            @abstractmethod
            def my_abstract_method(self, ...):
                ...
    """
    funcobj.__isabstractmethod__ = True
    return funcobj


class abstractclassmethod(classmethod):
    """A decorator indicating abstract classmethods.

    Similar to abstractmethod.

    Usage:

        class C(metaclass=ABCMeta):
            @abstractclassmethod
            def my_abstract_classmethod(cls, ...):
                ...

    'abstractclassmethod' is deprecated. Use 'classmethod' with
    'abstractmethod' instead.
    """

    __isabstractmethod__ = True

    def __init__(self, callable):
        callable.__isabstractmethod__ = True
        super().__init__(callable)


class abstractstaticmethod(staticmethod):
    """A decorator indicating abstract staticmethods.

    Similar to abstractmethod.

    Usage:

        class C(metaclass=ABCMeta):
            @abstractstaticmethod
            def my_abstract_staticmethod(...):
                ...

    'abstractstaticmethod' is deprecated. Use 'staticmethod' with
    'abstractmethod' instead.
    """

    __isabstractmethod__ = True

    def __init__(self, callable):
        callable.__isabstractmethod__ = True
        super().__init__(callable)


class abstractproperty(property):
    """A decorator indicating abstract properties.

    Requires that the metaclass is ABCMeta or derived from it.  A
    class that has a metaclass derived from ABCMeta cannot be
    instantiated unless all of its abstract properties are overridden.
    The abstract properties can be called using any of the normal
    'super' call mechanisms.

    Usage:

        class C(metaclass=ABCMeta):
            @abstractproperty
            def my_abstract_property(self):
                ...

    This defines a read-only property; you can also define a read-write
    abstract property using the 'long' form of property declaration:

        class C(metaclass=ABCMeta):
            def getx(self): ...
            def setx(self, value): ...
            x = abstractproperty(getx, setx)

    'abstractproperty' is deprecated. Use 'property' with 'abstractmethod'
    instead.
    """

    __isabstractmethod__ = True


try:
    from _abc import (get_cache_token, _abc_init, _abc_register,
                      _abc_instancecheck, _abc_subclasscheck, _get_dump,
                      _reset_registry, _reset_caches)
except ImportError:
    from _py_abc import ABCMeta, get_cache_token
    ABCMeta.__module__ = 'abc'
else:
    class ABCMeta(type):
        """Metaclass for defining Abstract Base Classes (ABCs).

        Use this metaclass to create an ABC.  An ABC can be subclassed
        directly, and then acts as a mix-in class.  You can also register
        unrelated concrete classes (even built-in classes) and unrelated
        ABCs as 'virtual subclasses' -- these and their descendants will
        be considered subclasses of the registering ABC by the built-in
        issubclass() function, but the registering ABC won't show up in
        their MRO (Method Resolution Order) nor will method
        implementations defined by the registering ABC be callable (not
        even via super()).
        """
        def __new__(mcls, name, bases, namespace, **kwargs):
            cls = super().__new__(mcls, name, bases, namespace, **kwargs)
            _abc_init(cls)
            return cls

        def register(cls, subclass):
            """Register a virtual subclass of an ABC.

            Returns the subclass, to allow usage as a class decorator.
            """
            return _abc_register(cls, subclass)

        def __instancecheck__(cls, instance):
            """Override for isinstance(instance, cls)."""
            return _abc_instancecheck(cls, instance)

        def __subclasscheck__(cls, subclass):
            """Override for issubclass(subclass, cls)."""
            return _abc_subclasscheck(cls, subclass)

        def _dump_registry(cls, file=None):
            """Debug helper to print the ABC registry."""
            print(f"Class: {cls.__module__}.{cls.__qualname__}", file=file)
            print(f"Inv. counter: {get_cache_token()}", file=file)
            (_abc_registry, _abc_cache, _abc_negative_cache,
             _abc_negative_cache_version) = _get_dump(cls)
            print(f"_abc_registry: {_abc_registry!r}", file=file)
            print(f"_abc_cache: {_abc_cache!r}", file=file)
            print(f"_abc_negative_cache: {_abc_negative_cache!r}", file=file)
            print(f"_abc_negative_cache_version: {_abc_negative_cache_version!r}",
                  file=file)

        def _abc_registry_clear(cls):
            """Clear the registry (for debugging or testing)."""
            _reset_registry(cls)

        def _abc_caches_clear(cls):
            """Clear the caches (for debugging or testing)."""
            _reset_caches(cls)


class ABC(metaclass=ABCMeta):
    """Helper class that provides a standard way to create an ABC using
    inheritance.
    """
    __slots__ = ()


def func_transformer(func):
    '''
    transform this kind of function:
    ```
    def demo_func(x):
        x1, x2, x3 = x
        return x1 ** 2 + (x2 - 0.05) ** 2 + x3 ** 2
    ```
    into this kind of function:
    ```
    def demo_func(x):
        x1, x2, x3 = x
        return x1 ** 2 + x2 ** 2 + x3 ** 2
    ```
    :param func:
    :return:
    '''

    prefered_function_format = '''
    def demo_func(x):
        x1, x2, x3 = x
        return x1 ** 2 + (x2 - 0.05) ** 2 + x3 ** 2
    '''
    if func.__code__.co_argcount == 1:
        return func
    elif func.__code__.co_argcount > 1:

        def func_transformed(x):
            args = tuple(x)
            return func(*args)

        return func_transformed
    else:
        raise ValueError('''
        object function error,
        function should be like this:
        ''' + prefered_function_format)


class GA_base(metaclass=ABCMeta):
    @abstractmethod
    def ranking(self):
        pass

    @abstractmethod
    def selection(self):
        pass

    @abstractmethod
    def crossover(self):
        pass

    @abstractmethod
    def mutation(self):
        pass

    def register(self, operator_name, operator, *args, **kwargs):
        '''
        regeister udf to the class
        :param operator_name: string in {'crossover', 'mutation', 'selection', 'ranking'}
        :param operator: a function
        :param args: arg of operator
        :param kwargs: kwargs of operator
        :return:
        '''
        valid_operator_name = {'crossover', 'mutation', 'selection', 'ranking'}
        if operator_name not in valid_operator_name:
            raise NameError(operator_name + "is not a valid operator name, should be in " + str(valid_operator_name))

        def operator_wapper(*wrapper_args):
            return operator(*(wrapper_args + args), **kwargs)

        setattr(self, operator_name, types.MethodType(operator_wapper, self))
        return self


# %% operators:

def ranking_raw(self):
    # GA select the biggest one, but we want to minimize func, so we put a negative here
    self.FitV = -self.Y
    return self.FitV


def ranking_linear(self):
    '''
    For more details see [Baker1985]_.

    :param self:
    :return:

    .. [Baker1985] Baker J E, "Adaptive selection methods for genetic
    algorithms, 1985.

    :param self:
    :return:
    '''
    self.FitV = np.argsort(np.argsort(-self.Y))
    return self.FitV


def selection_tournament(self, tourn_size=3):
    '''
    Select the best individual among *tournsize* randomly chosen
    individuals,
    :param self:
    :param tourn_size:
    :return:
    '''
    FitV = self.FitV
    sel_index = []
    for i in range(self.size_pop):
        aspirants_index = np.random.choice(range(self.size_pop), size=tourn_size)
        sel_index.append(max(aspirants_index, key=lambda i: FitV[i]))
    self.Chrom = self.Chrom[sel_index, :]  # next generation
    return self.Chrom


def selection_roulette_1(self):
    '''
    Select the next generation using roulette
    :param self:
    :return:
    '''
    FitV = self.FitV
    FitV = FitV - FitV.min() + 1e-10
    # the worst one should still has a chance to be selected
    sel_prob = FitV / FitV.sum()
    sel_index = np.random.choice(range(self.size_pop), size=self.size_pop, p=sel_prob)
    self.Chrom = self.Chrom[sel_index, :]
    return self.Chrom


def selection_roulette_2(self):
    '''
    Select the next generation using roulette
    :param self:
    :return:
    '''
    FitV = self.FitV
    FitV = (FitV - FitV.min()) / (FitV.max() - FitV.min() + 1e-10) + 0.2
    # the worst one should still has a chance to be selected
    sel_prob = FitV / FitV.sum()
    sel_index = np.random.choice(range(self.size_pop), size=self.size_pop, p=sel_prob)
    self.Chrom = self.Chrom[sel_index, :]
    return self.Chrom


def crossover_1point(self):
    Chrom, size_pop, len_chrom = self.Chrom, self.size_pop, self.len_chrom
    for i in range(0, size_pop, 2):
        Chrom1, Chrom2 = self.Chrom[i], self.Chrom[i + 1]
        n1 = np.random.randint(0, self.len_chrom, 1)
        # crossover at the point n1
        Chrom1[n1:], Chrom2[n1:] = Chrom2[n1:], Chrom1[n1:]
    return self.Chrom


def crossover_2point(self):
    Chrom, size_pop, len_chrom = self.Chrom, self.size_pop, self.len_chrom
    for i in range(0, size_pop, 2):
        Chrom1, Chrom2 = self.Chrom[i], self.Chrom[i + 1]
        n1, n2 = np.random.randint(0, self.len_chrom, 2)
        if n1 > n2:
            n1, n2 = n2, n1
        # crossover at the points n1 to n2
        Chrom1[n1:n2], Chrom2[n1:n2] = Chrom2[n1:n2], Chrom1[n1:n2]
    return self.Chrom


# def crossover_rv_3(self):
#     Chrom, size_pop = self.Chrom, self.size_pop
#     i = np.random.randint(1, self.len_chrom)  # crossover at the point i
#     Chrom1 = np.concatenate([Chrom[::2, :i], Chrom[1::2, i:]], axis=1)
#     Chrom2 = np.concatenate([Chrom[1::2, :i], Chrom[0::2, i:]], axis=1)
#     self.Chrom = np.concatenate([Chrom1, Chrom2], axis=0)
#     return self.Chrom


def mutation(self):
    # mutation of 0/1 type chromosome
    mask = (np.random.rand(self.size_pop, self.len_chrom) < self.prob_mut) * 1
    self.Chrom = (mask + self.Chrom) % 2
    return self.Chrom


def crossover_pmx(self):
    '''
    Executes a partially matched crossover (PMX) on Chrom.
    For more details see [Goldberg1985]_.

    :param self:
    :return:

    .. [Goldberg1985] Goldberg and Lingel, "Alleles, loci, and the traveling
   salesman problem", 1985.
    '''
    Chrom, size_pop, len_chrom = self.Chrom, self.size_pop, self.len_chrom
    for i in range(0, size_pop, 2):
        Chrom1, Chrom2 = self.Chrom[i], self.Chrom[i + 1]
        n1, n2 = np.random.randint(0, self.len_chrom, 2)
        if n1 > n2:
            n1, n2 = n2, n1
        # crossover at the point n1 to n2
        for j in range(n1, n2):
            x = np.argwhere(Chrom1 == Chrom2[j])
            y = np.argwhere(Chrom2 == Chrom1[j])
            Chrom1[j], Chrom2[j] = Chrom2[j], Chrom1[j]
            Chrom1[x], Chrom2[y] = Chrom2[y], Chrom1[x]
        self.Chrom[i], self.Chrom[i + 1] = Chrom1, Chrom2
    return self.Chrom


def mutation_TSP_1(self):
    for i in range(self.size_pop):
        for j in range(self.n_dim):
            if np.random.rand() < self.prob_mut:
                n = np.random.randint(0, self.len_chrom, 1)
                self.Chrom[i, j], self.Chrom[i, n] = self.Chrom[i, n], self.Chrom[i, j]
    return self.Chrom


def mutation_TSP_3(self):
    for i in range(self.size_pop):
        if np.random.rand() < self.prob_mut:
            n1, n2 = np.random.randint(0, self.len_chrom, 2)
            self.Chrom[i, n1], self.Chrom[i, n2] = self.Chrom[i, n2], self.Chrom[i, n1]
    return self.Chrom


# %%

class GA(GA_base):
    """
    Do genetic algorithm
    Parameters
    ----------------
    func : function
        The func you want to do optimal
    n_dim : int
        number of variables of func
    lb : array_like
        The lower bound of every variables of func
    ub : array_like
        The upper bound of every vaiiables of func
    precision : array_like
        The precision of every vaiiables of func
    size_pop : int
        Size of population
    max_iter : int
        Max of iter
    prob_mut : float between 0 and 1
        Probability of mutation
    Attributes
    ----------------------
    Lind : array_like
         The num of genes of every variable of func（segments）
    generation_best_X : array_like. Size is max_iter.
        Best X of every generation
    generation_best_ranking : array_like. Size if max_iter.
        Best ranking of every generation
    Examples
    -------------
    >>> demo_func=lambda x: x[0]**2 + x[1]**2 + x[2]**2
    >>> ga = GA(func=demo_func,n_dim=3, max_iter=500, lb=[-1, -10, -5], ub=[2, 10, 2])
    >>> best_x, best_y = ga.fit()
    """

    def __init__(self, func, n_dim,
                 size_pop=50, max_iter=200,
                 prob_mut=0.001, **kwargs):
        self.func = func_transformer(func)
        self.size_pop = size_pop  # size of population
        self.max_iter = max_iter
        self.prob_mut = prob_mut  # probability of mutation
        self.n_dim = n_dim

        self.define_chrom(kwargs)
        self.crtbp(self.size_pop, self.len_chrom)

        self.X = None  # shape is size_pop, n_dim (it is all x of func)
        self.Y = None  # shape is size_pop,
        self.FitV = None

        # self.FitV_history = []
        self.generation_best_X = []
        self.generation_best_Y = []
        self.all_history_Y = []
        # self.generation_best_ranking = []

    def define_chrom(self, kwargs):
        # define the types of Chrom
        self.lb = kwargs.get('lb', [-1] * self.n_dim)
        self.ub = kwargs.get('ub', [1] * self.n_dim)
        self.precision = kwargs.get('precision', [1e-7] * self.n_dim)

        # Lind is the num of genes of every variable of func（segments）
        Lind = np.ceil(np.log2((np.array(self.ub) - np.array(self.lb)) / np.array(self.precision))) + 1
        self.Lind = np.array([int(i) for i in Lind])
        self.len_chrom = int(sum(self.Lind))

    def crtbp(self, size_pop=10, len_chrom=30):
        # create the population
        self.Chrom = np.random.randint(low=0, high=2, size=(size_pop, len_chrom))
        return self.Chrom

    def gray2rv(self, gray_code):
        # Gray Code to real value: one piece of a whole chromosome
        # input is a 2-dimensional numpy array of 0 and 1.
        # output is a 1-dimensional numpy array which convert every row of input into a real number.
        # gray_code = crtbp(4, 2),gray2rv(gray_code)
        _, len_gray_code = gray_code.shape
        b = gray_code.cumsum(axis=1) % 2
        mask = np.logspace(start=1, stop=len_gray_code, base=0.5, num=len_gray_code)
        return (b * mask).sum(axis=1) / mask.sum()

    def chrom2x(self):
        # Chrom to the variables of func
        Chrom = self.Chrom
        Lind = self.Lind
        lb = self.lb
        ub = self.ub
        cumsum_len_segment = Lind.cumsum()
        X = np.zeros(shape=(Chrom.shape[0], len(Lind)))
        for i, j in enumerate(cumsum_len_segment):
            if i == 0:
                Chrom_temp = Chrom[:, :cumsum_len_segment[0]]
            else:
                Chrom_temp = Chrom[:, cumsum_len_segment[i - 1]:cumsum_len_segment[i]]
            temp1 = self.gray2rv(Chrom_temp)
            X[:, i] = lb[i] + (ub[i] - lb[i]) * temp1
        self.X = X
        return self.X

    def x2y(self):
        '''
        calculate Y for every X
        :return:
        '''
        self.Y = np.array([self.func(x) for x in self.X])
        return self.Y

    ranking = ranking_raw
    selection = selection_tournament
    crossover = crossover_2point
    mutation = mutation

    def run(self):
        for i in range(self.max_iter):
            self.X = self.chrom2x()
            self.x2y()
            self.ranking()
            self.selection()
            self.crossover()
            self.mutation()

            # record the best ones
            generation_best_index = self.Y.argmin()
            self.generation_best_X.append(self.X[generation_best_index, :])
            self.generation_best_Y.append(self.Y[generation_best_index])
            self.all_history_Y.append(self.Y)

        general_best_index = (np.array(self.generation_best_Y)).argmin()
        general_best_X, general_best_Y = \
            self.generation_best_X[general_best_index], self.generation_best_Y[general_best_index]
        return general_best_X, general_best_Y

    fit = run


class GA_TSP(GA):
    """
    Do genetic algorithm to solve the TSP (Travelling Salesman Problem)
    Parameters
    ----------------
    func : function
        The func you want to do optimal.
        It inputs a candidate solution(a routine), and return the costs of the routine.
    size_pop : int
        Size of population
    max_iter : int
        Max of iter
    prob_mut : float between 0 and 1
        Probability of mutation
    Attributes
    ----------------------
    Lind : array_like
         The num of genes corresponding to every variable of func（segments）
    generation_best_X : array_like. Size is max_iter.
        Best X of every generation
    generation_best_ranking : array_like. Size if max_iter.
        Best ranking of every generation
    Examples
    -------------
    Firstly, your data (the distance matrix). Here I generate the data randomly as a demo:
    ```py
    num_points = 8
    points_coordinate = np.random.rand(num_points, 2)  # generate coordinate of points
    distance_matrix = spatial.distance.cdist(points_coordinate, points_coordinate, metric='euclidean')
    print('distance_matrix is: \n', distance_matrix)
    def cal_total_distance(routine):
        num_points, = routine.shape
        return sum([distance_matrix[routine[i % num_points], routine[(i + 1) % num_points]] for i in range(num_points)])
    ```
    Do GA
    ```py
    from sko.GA import GA_TSP
    ga_tsp = GA_TSP(func=cal_total_distance, n_dim=8, pop=50, max_iter=200, Pm=0.001)
    best_points, best_distance = ga_tsp.fit()
    ```
    """

    def define_chrom(self, kwargs):
        self.len_chrom = self.n_dim

    def chrom2x(self):
        self.X = self.Chrom
        return self.X

    def crtbp(self, size_pop=10, len_chrom=30):
        # create the population
        tmp = np.random.rand(size_pop, len_chrom)
        self.Chrom = tmp.argsort(axis=1)
        return self.Chrom

    crossover = crossover_pmx
    mutation = mutation_TSP_1


# %% will be deprecated
from copy import deepcopy


def ga_with_udf(GA_class, options):
    '''
    will be deprecated
    options = {'selection': {'udf': selection_tournament, 'kwargs': {'tourn_size': 5}},
           'mutation': {'udf': mutation_TSP_type3}}
    GA_TSP2 = ga_register_udf(options)
    :param options:
    :return:
    '''
    print(ga_with_udf.__name__ + 'will be deprecated. Use GA.register instead')
    options = deepcopy(options)

    class GAUdf(GA_class):
        if 'crossover' in options:
            def crossover(self):
                crossover_udf = options['crossover']['udf']
                kwargs = options['crossover'].get('kwargs', dict())
                self.Chrom = crossover_udf(self, **kwargs)

        if 'mutation' in options:
            def mutation(self):
                mutation_udf = options['mutation']['udf']
                kwargs = options['mutation'].get('kwargs', dict())
                self.Chrom = mutation_udf(self, **kwargs)

        if 'selection' in options:
            def selection(self):
                selection_udf = options['selection']['udf']
                kwargs = options['selection'].get('kwargs', dict())
                self.Chrom = selection_udf(self, **kwargs)

        if 'ranking' in options:
            def ranking(self):
                ranking_udf = options['ranking']['udf']
                kwargs = options['ranking'].get('kwargs', dict())
                self.FitV = ranking_udf(self, **kwargs)

    return GAUdf


def ga_register_udf(udf_func_dict):
    '''
    will be deprecated
    :param udf_func_dict:
    :return:
    '''
    print(ga_register_udf.__name__ + 'will be deprecated. Use ga.register instead')

    class GAUdf(GA):
        pass

    for udf_name, udf in udf_func_dict.items():
        if udf_name == 'crossover':
            GAUdf.crossover = udf
        elif udf_name == 'mutation':
            GAUdf.mutation = udf
        elif udf_name == 'selection':
            GAUdf.selection = udf
        elif udf_name == 'ranking':
            GAUdf.ranking = udf
    return GAUdf
