import math
import numpy as np

# 桁架起升角度theta
theta = 70 * math.pi / 180
f = 300

# 余弦定理的桁架下面杆和垂直之间的角度
deg_gang = 60 * math.pi / 180 + theta

l_ver = 646
l_gan = 334

# 余弦定理，计算液压杆长
l_yeyagan = (l_ver ** 2 + l_gan ** 2 - 2 * l_ver * l_gan * math.cos(deg_gang)) ** 0.5

# 正弦定理，计算液压杆与垂直的角度
a = math.asin(l_gan / (l_yeyagan / math.sin(deg_gang)))

beta = math.pi / 2 - a
# beta是液压杆推力的角度


# 对整体桁架做受力分析，计算固定点受力，液压缸推力
# 已知条件是顶端受力F，和桁架起升角度theta

func_crane = [[0, 1, math.sin(beta)],
              [1, 0, math.cos(beta)],
              [0, 0, math.sin(beta) * math.cos(theta - 30 * math.pi / 180) - math.cos(beta) * math.sin(
                  theta - 30 * math.pi / 180)]]

f_crane = np.array(func_crane)
res_crane = [f, 0, 2 * 3 ** 0.5 * math.cos(theta) * f]
r_crane = np.array(res_crane)

x = np.linalg.solve(f_crane, r_crane)
# x[0]:固定端fx
# x[1]:固定端fy
# x[2]:液压缸推力fn
# print(x)

# 计算3个杆的内力fn1,fn2,fn3
func_inside = [[math.cos(theta), math.cos(30 * math.pi / 180 + theta), math.cos(theta)],
               [math.sin(theta), math.sin(30 * math.pi / 180 + theta), math.sin(theta)],
               [0, math.cos(30 * math.pi / 180 + theta) * math.sin(theta - 30 * math.pi / 180) - math.sin(
                   30 * math.pi / 180 + theta) * math.cos(theta - 30 * math.pi / 180),
                math.cos(theta) * math.sin(theta - 30 * math.pi / 180) - math.sin(theta) * math.cos(
                    theta - 30 * math.pi / 180)]]
f_inside = np.array(func_inside)
res_inside = [-x[0] - x[2] * math.cos(beta),
              -x[1] - x[2] * math.sin(beta),
              -x[2] * math.cos(beta) * math.sin(theta - 30 * math.pi / 180) + math.sin(beta) * math.cos(
                  theta - 30 * math.pi / 180)
              ]
r_inside = np.array(res_inside)

y = np.linalg.solve(f_inside, r_inside)
print(y[0] / 0.044)
print(y[1] / 0.044)
print(y[2] / 0.044)
