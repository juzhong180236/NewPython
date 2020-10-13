from sympy import *

x, y, z = symbols('x y z')
# x = sin(1)
expr1 = x * sin(x ** 2)
print(expr1.subs({x: 2}).n(3))
print(expr1.subs({x: 2}).evalf(3))
print(expr1.n())