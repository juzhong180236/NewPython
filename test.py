import data_to_file as dtf


def calc(*numbers):
    sum = 0
    for n in numbers:
        sum = sum + n * n
    print(sum)


calc(1, 2, 3, 4)


def f(a, *args):
    print(args)


f(1, 2, 3, 4)


def d(**kargs):
    print(kargs)


d(a=1, b=2)


# 在函数混合使用*以及**。
def h(a, *args, **kargs):
    print(a, args, kargs)


h(1, 2, 3, x=4, y=5)
