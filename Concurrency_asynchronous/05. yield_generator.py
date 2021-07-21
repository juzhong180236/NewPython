def range_generator(n):
    i = 0
    while i < n:
        print("Generating value {}".format(str(i)))
        yield i
        i += 1


# generator = range_generator(3)
# print(generator)
# print(next(generator))
# print(next(generator))


def my_generator(_list):
    _i = 0
    while _list and _i < len(_list):
        if _i > 0:
            if _list[_i] == _list[_i - 1]:
                _i += 1
                continue  # 估计是这里的问题，没有yield
            else:
                yield _list[_i]
        else:
            yield _list[_i]
        _i += 1


# my_list = [2, 2, 2, 23, 23, 5.6, 3.4]
# my_gen = my_generator(my_list)
# # print(my_gen)
# for i in range(len(my_list)):
#     print(next(my_gen))

# def my_generator2(n):
#     _i = 0
#     while _i < n:
#         yield _i
#         _i += 1
#
#
# my_gen2 = my_generator2(3)
# for i in range(3):
#     print(next(my_gen2))

# def my_generator3():
#     _i = 0
#     while True:
#         yield _i
#         _i += 1
#
#
# my_gen3 = my_generator3()
# for i in range(100):
#     print(next(my_gen3))

def parrot():
    while True:
        message = yield
        print("Parrot says: {}".format(message))


my_parrot = parrot()
my_parrot.send(None)
my_parrot.send(1)
my_parrot.send(2)
