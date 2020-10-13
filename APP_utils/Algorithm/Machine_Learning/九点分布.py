import math
import matplotlib.pyplot as plt
import numpy as np


def first_digital(x):
    while x >= 10:
        x //= 10
    return x


if __name__ == "__main__":
    n = 1
    frequency = [0] * 9
    list_m = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for i in range(1, 1000):
        n *= i
        m = first_digital(n)
        frequency[m - 1] += 1
    print(frequency)
    plt.plot(list_m, frequency, 'r-', linewidth=2)
    plt.plot(list_m, frequency, 'go', markersize=8)
    plt.grid(True)
    plt.show()
