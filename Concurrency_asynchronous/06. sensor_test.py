import serial
import serial.tools.list_ports
import asyncio
from threading import Thread
import time

port_list = list(serial.tools.list_ports.comports())


def return_correct_port():
    for p in port_list:
        if p.vid == 1659 and p.pid == 8963:
            return p.name


serialPort = return_correct_port()  # 串口名称的字符串
baudRate = 460800  # 波特率   acceleration sensor-- 115200; pose sensor--460800

ser = serial.Serial(serialPort, baudRate, timeout=None)  # 默认打开
"""
input 是传感器给到电脑的
output 是电脑给到传感器的
"""

_list = []
start_time = time.time()

pitch_angle_degree = 0


def generator():
    global pitch_angle_degree
    while True:
        # print(ser.in_waiting)
        if ser.in_waiting >= 134:
            receive_data = ser.read(134)
            ser.flushInput()
            if b'YIS' in receive_data:
                _index = receive_data.index(b'YIS')
                pitch_angle_degree = round(int.from_bytes(receive_data[_index + 78:_index + 82], byteorder='little',
                                                          signed=True) * 0.000001, 2)
                # if pitch_angle_degree == temp_angle:
                #     continue
                # else:
                #     pitch_angle_degree = temp_angle
                # print(temp_angle)
                # print(pitch_angle_degree)
                _list.append(pitch_angle_degree)
                if len(_list) == 1000:
                    print(time.time() - start_time)
            # await asyncio.sleep(0)


def test(text):
    for i in range(20):
        # await asyncio.sleep(0.5)
        print(text)


try:
    # generator = generator()
    # test = test('我是 test！')
    # loop = asyncio.get_event_loop()
    # asyncio.ensure_future(generator)
    # asyncio.ensure_future(test)
    # loop.run_forever()
    t1 = Thread(target=generator())
    t2 = Thread(target=test('sdf'))
    t1.start()
    t2.start()
except (ValueError, RuntimeError, TypeError, NameError):
    ser.close()
finally:
    ser.close()
