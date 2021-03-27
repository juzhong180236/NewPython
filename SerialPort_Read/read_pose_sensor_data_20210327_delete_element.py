"""
使用itertools.count来不断生成顺序数字来做x轴，这样就可以不断读取数据
"""
import serial
import itertools
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import serial.tools.list_ports
from numpy import abs

port_list = list(serial.tools.list_ports.comports())


def return_correct_port():
    for p in port_list:
        if p.vid == 6790 and p.pid == 29987:
            return p.name


serialPort = return_correct_port()  # 串口名称的字符串

baudRate = 460800  # 波特率   acceleration sensor-- 115200; pose sensor--460800
ser = serial.Serial(serialPort, baudRate, timeout=None)  # 默认打开

"""
input 是传感器给到电脑的
output 是电脑给到传感器的
"""
fig, ax = plt.subplots()
line, = ax.plot([], [], lw=1.5)
ax.grid()
plt.xlabel("Points")
plt.ylabel("Angle (°)")
xdata, ydata = [], []
y_lim = 10


def init():
    ax.set_ylim(-y_lim, y_lim)
    ax.set_xlim(0, 300)
    line.set_data(xdata, ydata)
    return line


def run(data):
    receive_data = ser.read(120)
    ser.flushInput()
    if receive_data[0:3] == b'YIS':
        xdata.append(data)
        y = int.from_bytes(receive_data[78:82], byteorder='little', signed=True) * 0.000001
        ymin, ymax = ax.get_ylim()
        if abs(y) >= ymax:
            ax.set_ylim(-2 * ymax, 2 * ymax)
            ax.figure.canvas.draw()
        ydata.append(y)
    xmin, xmax = ax.get_xlim()
    if data >= xmax:
        # print(xmax / 2 + 1)
        del xdata[0:int(xmax)]
        del ydata[0:int(xmax)]
        ax.set_xlim(xmax, xmax + 300)
        ax.figure.canvas.draw()
    line.set_data(xdata, ydata)

    return line


def data_gen():
    for cnt in itertools.count():
        t = cnt
        yield t


ani = animation.FuncAnimation(fig, run, data_gen, interval=10, init_func=init)
plt.show()

ser.close()
# """
#     timeout = None 读到所要求数量的字节再返回，要不就一直阻塞
#     timeout = 0 立即返回，返回0，或者更多，取决于要读取的字节数
#     timeout = x 等待x秒，字节数够立即返回，不够等待x秒有多少字节返回多少字节
#     ser = serial.Serial()  # 默认不打开
#     print(ser.is_open)
#     ser.port = 'xxx'
#     ser.baudrate = 460800
#     ser.bytesize = 8
#     ser.parity = serial.PARITY_NONE
#     ser.stopbits = 1
#     ser.open()
#     ser.close()
# """

# hex_str = bytes.fromhex(str(450146))  # 串口接收信号开始传输数据
# ser.write(hex_str)
#
#
# # define the twos_operation
# def twos_operation(x):
#     a = int(x, 16)
#     if a < 2 ** 31:
#         positive_number = a * 0.000001  # +-2g  256000;   +-8g  64000
#
#     else:
#         reversed_code = a  # 将对应的数据码取反
#         twos_code = bin(reversed_code).replace('0b', '')
#         sum = 0
#         for k in range(len(twos_code)):
#             sum += 1 * 2 ** (len(twos_code) - k - 1)
#             if k == len(twos_code) - 1:
#                 break
#
#         positive_number = (sum - int(twos_code, 2) + 1) * (-1) * 0.000001
#
#     return positive_number
#
#
# calculate_velocity, calculate_displacement = 0, 0
# integrated_speed, integrated_displacement = [], []
#
#
# # integrated_speed.append(calculate_velocity)
# # integrated_displacement.append(calculate_displacement)
#
# ### 定义由加速度---速度---位移
# def acceleration_to_velocity(x):
#     global calculate_velocity, calculate_displacement
#     global integrated_speed, integrated_displacement
#
#     if len(x) == 1:
#         calculate_velocity += np.trapz([0, x[-1]], dx=0.02)
#         integrated_speed.append(calculate_velocity)  #### 存储计算的速度
#
#         calculate_displacement += np.trapz([0, integrated_speed[-1]], dx=0.02)  ### 计算位移
#         integrated_displacement.append(calculate_displacement)  #### 存储计算的位移
#
#
#     elif x[-1] > 0 and len(x) >= 2 and x[-1] - x[-2] > 0:  ### 向上加速运动；速度增加，位移为负值，但趋近于0
#         calculate_velocity -= np.trapz([x[-2], x[-1]], dx=0.02)
#         integrated_speed.append(calculate_velocity)
#
#         calculate_displacement += np.trapz([integrated_speed[-1], integrated_speed[-2]], dx=0.02)  ### 计算位移
#         integrated_displacement.append(calculate_displacement)  #### 存储计算的位移
#
#
#     elif x[-1] > 0 and len(x) >= 2 and x[-1] - x[-2] < 0:  ### 向下加速运动，速度反向增加，位移减小
#         calculate_velocity -= np.trapz([x[-2], x[-1]], dx=0.02)
#         integrated_speed.append(calculate_velocity)
#
#         calculate_displacement += np.trapz([integrated_speed[-1], integrated_speed[-2]], dx=0.02)  ### 计算位移
#         integrated_displacement.append(calculate_displacement)  #### 存储计算的位移
#
#
#     elif x[-1] < 0 and len(x) >= 2 and x[-1] - x[-2] > 0:  ###向上加速运动
#         calculate_velocity -= np.trapz([x[-2], x[-1]], dx=0.02)
#         integrated_speed.append(calculate_velocity)
#
#         calculate_displacement += np.trapz([integrated_speed[-1], integrated_speed[-2]], dx=0.02)  ### 计算位移
#         integrated_displacement.append(calculate_displacement)  #### 存储计算的位移
#
#
#     elif x[-1] < 0 and len(x) >= 2 and x[-1] - x[-2] < 0:  ### 向下减少
#         calculate_velocity -= np.trapz([x[-2], x[-1]], dx=0.02)
#         integrated_speed.append(calculate_velocity)
#
#         calculate_displacement += np.trapz([integrated_speed[-1], integrated_speed[-2]], dx=0.02)  ### 计算位移
#         integrated_displacement.append(calculate_displacement)  #### 存储计算的位移
#
#     return integrated_speed, integrated_displacement
#
#
# sensor1_axis1, sensor1_axis2, sensor1_axis3 = [], [], []
# sensor2_axis1, sensor2_axis2, sensor2_axis3 = [], [], []
# sensor3_axis1, sensor3_axis2, sensor3_axis3 = [], [], []
# sensor4_axis1, sensor4_axis2, sensor4_axis3 = [], [], []
# sensor5_axis1, sensor5_axis2, sensor5_axis3 = [], [], []
# sensor6_axis1, sensor6_axis2, sensor6_axis3 = [], [], []
# sensor7_axis1, sensor7_axis2, sensor7_axis3 = [], [], []
# sensor8_axis1, sensor8_axis2, sensor8_axis3 = [], [], []
#
# sampling_time = []
#
# # plt.ion()
# # plt.figure()
#
# displacement = 0
# # sampling_time.append(displacement)
#
# # 收发数据
# while 1:
#     # global displacement
#
#     begin_time = time()
#     s = ser.readline(104)
#
#     log += 1
#     k = s.hex()
#     print('k', k)
#     # sampling_time.append(log)
#
#     for i in range(int(len(k))):
#
#         if str(k[i:i + 2]) == str(10) and str(k[i + 28:i + 30]) == str(11):
#             axis_1 = k[i + 10:i + 12] + k[i + 8:i + 10] + k[i + 6:i + 8] + k[i + 4:i + 6]
#             sensor1_axis1.append(twos_operation(axis_1))
#
#             axis_2 = k[i + 18:i + 20] + k[i + 16:i + 18] + k[i + 14:i + 16] + k[i + 12:i + 14]
#             sensor1_axis2.append(twos_operation(axis_2))
#
#             axis_3 = k[i + 26:i + 28] + k[i + 24:i + 26] + k[i + 22:i + 24] + k[i + 20:i + 22]
#             sensor1_axis3.append(twos_operation(axis_3))
#
#             sampling_time.append(log)
#
#             acceleration_to_velocity(sensor1_axis1)
#
#         # elif str(k[i:i+2]) == str(40)and str(k[i+2:i+4])== str(0)+'c':
#         #     # global displacement
#         #     axis_1 =k[i+4:i+12]
#         #     sensor2_axis1.append(twos_operation(axis_1))
#         #     sampling_time.append(log)
#         #
#         #     #### 输出对应的积分速度和位移值
#         #     # speed,displacement = acceleration_to_velocity(sensor2_axis3)
#         #
#         #
#         #     axis_2 =k[i+12:i+20]
#         #     print('b',axis_2)
#         #     sensor2_axis2.append(twos_operation(axis_2))
#         #
#         #     axis_3 = k[i+20:i+28]
#         #     sensor2_axis3.append(twos_operation(axis_3))
#         #
#         #
#         #     # print('accel_tovelocity',acceleration_to_velocity(sensor2_axis3))
#         #     # print('sampling_time',sampling_time)
#         #     # print('displacement',displacement)
#         #
#         # elif str(k[i:i+2]) == str(33)and str(k[i+20:3*i+22])==str(44):
#         #     axis_1 =k[i+2:i+7]
#         #     sensor3_axis1.append(twos_operation(axis_1))
#         #
#         #     axis_2 =k[i+8:i+13]
#         #     sensor3_axis2.append(twos_operation(axis_2))
#         #
#         #     axis_3 = k[i+14:i+19]
#         #     sensor3_axis3.append(twos_operation(axis_3))
#         #
#         # elif str(k[i:i+2]) == str(44) and str(k[i+20:3*i+22])==str(55):
#         #     axis_1 =k[i+2:i+7]
#         #     sensor4_axis1.append(twos_operation(axis_1))
#         #
#         #     axis_2 =k[i+8:i+13]
#         #     sensor4_axis2.append(twos_operation(axis_2))
#         #
#         #     axis_3 = k[i+14:i+19]
#         #     sensor4_axis3.append(twos_operation(axis_3))
#         #
#         #
#         # elif str(k[i:i+2]) == str(55) and str(k[i+20:i+22])==str(66) and str(k[i+40:i+42])==str(77):
#         #     axis_1 =k[i+2:i+7]
#         #     sensor5_axis1.append(twos_operation(axis_1))
#         #
#         #     axis_2 =k[i+8:i+13]
#         #     sensor5_axis2.append(twos_operation(axis_2))
#         #
#         #     axis_3 = k[i+14:i+19]
#         #     sensor5_axis3.append(twos_operation(axis_3))
#         #
#         #
#         # elif str(k[i:i+2]) == str(66)and str(k[i+20:i+22])==str(77):
#         #     axis_1 =k[i+2:i+7]
#         #     sensor6_axis1.append(twos_operation(axis_1))
#         #
#         #     axis_2 =k[i+8:i+13]
#         #     sensor6_axis2.append(twos_operation(axis_2))
#         #
#         #     axis_3 = k[i+14:i+19]
#         #     sensor6_axis3.append(twos_operation(axis_3))
#         #
#         # elif str(k[i:i+2]) == str(77)and str(k[i+20:i+22])==str(88):
#         #     axis_1 =k[i+2:i+7]
#         #     sensor7_axis1.append(twos_operation(axis_1))
#         #
#         #     axis_2 =k[i+8:i+13]
#         #     sensor7_axis2.append(twos_operation(axis_2))
#         #
#         #     axis_3 = k[i+14:i+19]
#         #     sensor7_axis3.append(twos_operation(axis_3))
#         #
#         # elif str(k[i:i+2]) == str(88) and str(k[i-20:i-19]) == str(77):
#         #     axis_1 =k[i+2:i+7]
#         #     sensor8_axis1.append(twos_operation(axis_1))
#         #
#         #     axis_2 =k[i+8:i+13]
#         #     sensor8_axis2.append(twos_operation(axis_2))
#         #
#         #     axis_3 = k[i+14:i+19]
#         #     sensor8_axis3.append(twos_operation(axis_3))
#
#     end_time = time()
#     run_time = end_time - begin_time
#
#     if log == 200:
#         data22 = pd.DataFrame({'sen1_axis1': sensor1_axis1, 'sen1_axis2': sensor1_axis2, 'sen1_axis3': sensor1_axis3})
#         data22.to_csv('3011_data_to.csv')
#         break
#
#     # print('sensor2_100',sensor2_axis1_100)
#
#     # print('run_time',run_time)
#     # print('displacement',displacement)
#     # plt.plot(sampling_time, displacement,'r-')
#     # plt.pause(0.000000001)
#
#     if len(sampling_time) <= 100:
#         plt.subplot(131)
#         plt.plot(sampling_time, sensor1_axis1, 'r-')
#         # plt.ylim(-4,+4)
#         plt.title('sensor1_axis1')
#         plt.subplot(132)
#         plt.plot(sampling_time, integrated_displacement, 'b-')
#         # plt.ylim(-4,+4)
#         plt.title('sensor1_axis2')
#         plt.subplot(133)
#         plt.plot(sampling_time, sensor1_axis3, 'y-')
#         # plt.ylim(0,-10)
#         plt.title('sensor1_axis3')
#         plt.pause(0.00000001)
#     else:
#         plt.subplot(131)
#         plt.plot(sampling_time[-99:-1], sensor1_axis1[-99:-1], 'r-')
#         # plt.ylim(-4,+4)
#         plt.xlim(sampling_time[-99], sampling_time[-1])
#         plt.title('sensor1_axis1')
#         plt.subplot(132)
#         plt.plot(sampling_time[-99:-1], integrated_displacement[-99:-1], 'b-')
#         # plt.ylim(-4,+4)
#         plt.xlim(sampling_time[-99], sampling_time[-1])
#         plt.title('sensor1_axis2')
#         plt.subplot(133)
#         plt.plot(sampling_time[-99:-1], sensor1_axis3[-99:-1], 'y-')
#         # plt.ylim(0,-10)
#         plt.xlim(sampling_time[-99], sampling_time[-1])
#         plt.title('sensor1_axis3')
#         plt.pause(0.00000001)
#
#     # plt.plot(sampling_time, displacement,'r-')
#     # plt.pause(0.00000001)
#
#     # end_time = time()
#     # run_time = end_time - begin_time
#     # print('run_time',run_time)

# ser.close()
