import numpy as np
import matplotlib.pyplot as plt

"""
对非线性的状态和观测方程线性化，即使用泰勒公式近似

EKF

x(k)=sin(3*x(k-1))
y(k)=x(k)^2

注意似然概率是多峰分布，具有强烈的非线性，
"""
# X(k-1)服从期望为X(k-1)+，方差为P(k-1)+的正态分布
