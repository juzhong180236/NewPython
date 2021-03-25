# https://www.jb51.net/article/178330.htm
"""
无穷迭代器 cycle()
"""
from itertools import cycle

c = cycle('ABCD')
for i in range(10):
    print(next(c), end=',')
from itertools import count

"""
无穷的迭代器 count()
"""
c = count(0, 2)
v = next(c)
while v < 10:
    v = next(c)
    print(v, end=',')

"""
无穷迭代器 repeat()
"""
from itertools import repeat

r = repeat(1, 3)
for i in range(3):
    print(next(r), end=',')