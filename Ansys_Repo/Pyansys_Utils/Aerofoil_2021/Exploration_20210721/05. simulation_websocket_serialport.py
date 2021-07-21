from ansys.mapdl.core import launch_mapdl
import numpy as np
import pyvista as pv
import pyvistaqt as pvqt
import asyncio
import serial.tools.list_ports
import websockets
import time

_radian = np.pi / 180
''' Find serial port list'''
port_list = list(serial.tools.list_ports.comports())


def return_correct_port():
    for p in port_list:
        if p.vid == 1659 and p.pid == 8963:
            return p.name


serialPort = return_correct_port()  # 串口名称的字符串
baudRate = 460800  # 波特率   acceleration sensor-- 115200; pose sensor--460800

ser = serial.Serial(serialPort, baudRate, timeout=None)  # 默认打开
pitch_angle_degree = 0  # 度数

_list = []
start_time = time.time()


async def read_sensor_data():
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
                # print(pitch_angle_degree)
                _list.append(pitch_angle_degree)
                if len(_list) == 10:
                    print(time.time() - start_time)
            await asyncio.sleep(0)


''' Simulation initialization '''
mapdl = launch_mapdl()
mapdl.clear()

''' Geometry '''
mapdl.prep7()
mapdl.units('SI')
k0 = mapdl.k("", 0, 0, 0)
k1 = mapdl.k("", 0, 0.05, 0)
k2 = mapdl.k("", 0.06, 0.05, 0)
k3 = mapdl.k("", 0.2802, 0.016, 0)
k4 = mapdl.k("", 0.2802, 0, 0)
l0 = mapdl.l(k0, k1)
l1 = mapdl.l(k1, k2)
l2 = mapdl.l(k2, k3)
l3 = mapdl.l(k3, k4)
l4 = mapdl.l(k4, k0)
anum = mapdl.al(l0, l1, l2, l3, l4)

''' Meshing '''
mapdl.et(1, 181)
# mapdl.r(1, 0.00115)
mapdl.esize(0.004)
# mapdl.etcontrol('set')
mapdl.amesh('ALL')
mapdl.sectype(1, "shell")
mapdl.secdata(0.00115)
mapdl.run("secoff,mid")
# vertices = mapdl.mesh.nodes
# elements = mapdl.mesh.elem
# mesh = mapdl.mesh.grid
# faces = np.hstack((map(lambda x: np.hstack((4, x[-4:])), mapdl.mesh.elem)))
# mesh = pv.PolyData(vertices, faces)
# mesh.plot()
# mesh = pv.wrap(mapdl.mesh.grid)
# pl = pvqt.BackgroundPlotter()
# pl.add_mesh(mesh)
# pl.camera_position = 'iso'
# pl.background_color = 'white'
# cpos = pl.show()

# mapdl.aplot(show_lines=True, line_width=5, show_bounds=True, cpos='xy')
# mapdl.eplot(show_bounds=True, cpos='iso')

''' Material Properties '''
mapdl.mp('ex', 1, 7.1e10)
mapdl.mp('nuxy', 1, 0.33)
mapdl.mp('dens', 1, 2.83e3)

''' Boundary Conditions '''
# Fix the left-hand side of the aerofoil.
mapdl.nsel('S', 'LOC', 'X', 0)
mapdl.d("all", "all")
# Apply a force on the right-hand side of the aerofoil.
mapdl.nsel('S', 'LOC', 'X', 0.2802)
assert np.allclose(mapdl.mesh.nodes[:, 0], 0.2802)
# mapdl.cp(5, 'UZ', 'ALL')
# mapdl.nsel('R', 'LOC', 'Y', 0.008)
mapdl.d("all", "uz", -0.08)

# _ = mapdl.allsel()
mapdl.finish()  # 退出prep7处理器

''' Solve '''
mapdl.slashsolu()
mapdl.antype(antype='static')
mapdl.eqslv(lab='sparse', keepfile=1)
# mapdl.nlgeom(key='on')
mapdl.solve()
output = mapdl.finish()

''' Post-Processing '''


# grab the result from the ``mapdl`` instance
# result = mapdl.result
# nnum, stress = result.nodal_stress(0)
# nnum1, displacement = result.nodal_displacement(0)

# mesh.plot(scalars=stress)
# mesh.plot(scalars=displacement)

# result.plot_principal_nodal_stress(0, 'SEQV', lighting=False,
#                                    cpos='iso', background='w',
#                                    text_color='k', add_text=False,
#                                    show_edges=True, show_displacement=True)


async def update():
    while True:
        mapdl.prep7()
        mapdl.d("all", "uz", 0.2802 * np.sin(pitch_angle_degree * _radian))
        # _ = mapdl.allsel()
        mapdl.finish()  # 退出prep7处理器

        ''' Solve '''
        mapdl.slashsolu()
        mapdl.antype(antype='static')
        mapdl.eqslv(lab='sparse', keepfile=1)
        # mapdl.nlgeom(key='on')
        mapdl.solve()
        mapdl.finish()
        result = mapdl.result
        global stress, displacement
        nnum, stress = result.nodal_stress(0)
        nnum, displacement = result.nodal_displacement(0)
        # print("This is update")
        # print(stress)
        await asyncio.sleep(0)
        # element_stress, elemnum, enode = result.element_stress(0)


async def send_data(websocket, path):
    while True:
        try:
            _uz = await websocket.recv()
            if _uz == "s":
                await websocket.send(','.join(map(str, stress)))
            elif _uz == 'd':
                await websocket.send(','.join(map(str, displacement)))
            else:
                pass
            await asyncio.sleep(0)
        except websockets.WebSocketException:
            print('客户端连接断开！')
            break
    return


try:
    start_server = websockets.serve(send_data, "127.0.0.1", 3000)
    read_sensor_data = read_sensor_data()
    update = update()
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(read_sensor_data)
    asyncio.ensure_future(update)
    loop.run_until_complete(start_server)
    loop.run_forever()
except (ValueError, RuntimeError, TypeError, NameError):
    ser.close()
finally:
    ser.close()
# mapdl.post_processing.plot_nodal_displacement('Z')
# result.plot_nodal_displacement(0, 'UZ')
# nnum, stress = result.nodal_stress(0)
# nnum1, displacement = result.nodal_displacement(0)
# element_stress, elemnum, enode = result.element_stress(0)
