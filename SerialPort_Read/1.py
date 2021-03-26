import serial
import serial.tools.list_ports
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation  # 导入负责绘制动画的接口

# port_list = list(serial.tools.list_ports.comports())
# # https://blog.csdn.net/weixin_30689307/article/details/98043846
# for p in port_list:
#     print(p.description)
#     print(p.hwid)
#     print(p.vid)
#     print(p.pid)
#     print(p.serial_number)
#     print(p.location)
#     print(p.manufacturer)
#     print(p.product)
#     print(p.interface)
#     print(1)
# print(int(bytes.fromhex("59")[0]))
# print(int.from_bytes(b'\x12\x34'))
# fig, ax = plt.subplots()  # 生成轴和fig,  可迭代的对象
# x, y = [], []  # 用于接受后更新的数据
# line, = plt.plot([], [], '.-')  # 绘制线对象，plot返回值类型，要加逗号
#
#
# def init():
#     # 初始化函数用于绘制一块干净的画布，为后续绘图做准备
#     ax.set_xlim(-5, 15 * np.pi)  # 初始函数，设置绘图范围
#     ax.set_ylim(-3, 3)
#     return line
#
#
# def update(step):  # 通过帧数来不断更新新的数值
#     x.append(step)
#     y.append(np.cos(step / 3) + np.sin(step ** 2))  # 计算y
#     line.set_data(x, y)
#     return line
#
#
# # fig 是绘图的画布
# # update 为更新绘图的函数，step数值是从frames 传入
# # frames 数值是用于动画每一帧的数据
# ani = FuncAnimation(fig, update, frames=np.linspace(0, 13 * np.pi, 128),
#                     init_func=init, interval=20)
# plt.show()

fig, ax = plt.subplots()
x, y = [], []
line, = plt.plot([], [], '.-', color='orange')
nums = 50  # 需要的帧数


def init():
    ax.set_xlim(-5, 60)
    ax.set_ylim(-3, 3)
    return line


def update(step):
    if len(x) >= nums:  # 通过控制帧数来避免不断的绘图
        return line
    x.append(step)
    y.append(np.cos(step / 3) + np.sin(step ** 2))  # 计算y
    line.set_data(x, y)
    return line


ani = FuncAnimation(fig, update, frames=nums,  # nums输入到frames后会使用range(nums)得到一系列step输入到update中去
                    init_func=init, interval=20)
# plt.show()


