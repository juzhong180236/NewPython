import numpy as np
import matplotlib.pyplot as plt
import random


class DrawFunction(object):

    def __init__(self, X=np.arange(-2, 2, 0.01), P=None, N=None):
        if P is None:
            P = [0.1, 0.5, 1, 2, 3, 10]
        if N is None:
            N = list(map(str, P))
        self.X = X
        self.P = P
        self.N = N

    def Gaussian_theta(self, i):
        return np.exp(-self.P[i] * (self.X ** 2))

    def Multiquadric(self, i):
        return np.sqrt(self.X ** 2 + self.P[i] ** 2)

    def Gaussian(self, i):
        return np.exp(-(np.abs(self.X) ** self.P[i]))

    def Power(self, i):
        return 1 / np.power(np.abs(self.X), self.P[i])

    def linear_abs(self, i):
        return np.abs(self.X - 0)

    def random_color(self):
        color = str(hex(int(random.uniform(0.001, 1) * 0xffffff))).lstrip('0x')
        if len(color) == 6:
            color = color
        else:
            color = color + '0' * (6 - len(color))
        return color

    def draw(self, whichOne):
        func_index = {'gs': self.Gaussian,
                      'gs_t': self.Gaussian_theta,
                      'mq': self.Multiquadric,
                      'power': self.Power,
                      'lin_a': self.linear_abs}
        # func = [, self.Gaussian_theta, self.Multiquadric,
        #         self.Power, self.linear_abs]
        for i in range(len(self.P)):
            plt.plot(self.X, func_index[whichOne](i), color='#' + self.random_color(),
                     label=self.N[i])
            if i == 0:
                plt.title(func_index[whichOne].__name__)
        plt.legend()
        plt.show()


if __name__ == "__main__":
    aa = DrawFunction()
    aa.draw(3)

''' sqrt(xi^2+s^2) s变化 '''
# X1 = np.arange(-2, 2, 0.01)
# P1 = [0.1, 0.5, 1, 2, 3, 10]
# N1 = ['0.1', '0.5', '1', '2', '3', '10']
#
# for i in range(len(P1)):
#     plt.plot(X, Multiquadric(X1, P[i]), color='#' + Random_color(),
#              label=N1[i])
# plt.legend()
# plt.show()

''' exp(-θ|xi-x|^2) θ变化 '''
# X3 = np.arange(-2, 2, 0.01)
# P3 = [0.1, 0.5, 1, 2, 3, 10]
# N3 = ['0.1', '0.5', '1', '2', '3', '10']
#
# for i in range(len(P3)):
#     plt.plot(X3, Gaussian_theta(X3, P3[i]), color='#' + Random_color(),
#              label=N3[i])
# plt.legend()
# plt.show()

''' 1/d^n n变化 '''
# X4 = np.arange(-2, 2, 0.01)
# P4 = [0.1, 0.5, 1, 2, 3, 10]
# N4 = ['0.1', '0.5', '1', '2', '3', '10']
#
# for i in range(len(P4)):
#     plt.plot(X4, Gaussian_theta(X4, P4[i]), color='#' + Random_color(),
#              label=N4[i])
# plt.legend()
# plt.show()
