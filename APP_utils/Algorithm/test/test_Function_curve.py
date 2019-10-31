from APP_utils.Algorithm.test.Function_drawing import DrawFunction
import numpy as np

# func = [self.Gaussian, self.Gaussian_theta, self.Multiquadric, self.Power]
dd = np.linspace(-1, 1, 100)
# dd = np.arange(-1, 1, 0.01)
print(dd)
print(np.argwhere(dd == 0))
# df = DrawFunction(X=np.delete(dd, np.argwhere(dd == 0)[0][0]), P=[2])
df = DrawFunction(X=dd, P=[2])
df.draw('lin_a')
# df1 = DrawFunction()
# df1.draw(2)

# a = [[2, 3, 5], [3, 4, 5], [5, 6, 7]]
# print(a)
# print(np.var(a))
# b = np.array([[2, 3, 5], [3, 4, 5], [5, 6, 7]])
# print(b)
# print(np.var(b))
# c = [(2, 3, 5), (3, 4, 5), (5, 6, 7)]
# print(c)
# print(np.var(c))
# aa = np.arange(-1, 5, 1)
# print(aa)
