import asyncio
import websockets
import numpy as np
from ansys.mapdl.core import launch_mapdl


def producer(_uz):
    mapdl.prep7()
    mapdl.d("all", "uz", -_uz)
    # _ = mapdl.allsel()
    mapdl.finish()  # 退出prep7处理器

    ''' Solve '''
    mapdl.slashsolu()
    mapdl.antype(antype='static')
    mapdl.eqslv(lab='sparse', keepfile=1)
    mapdl.nlgeom(key='on')
    mapdl.solve()
    mapdl.finish()
    result = mapdl.result
    nnum, stress = result.nodal_stress(0)
    # nnum1, displacement = result.nodal_displacement(0)
    # element_stress, elemnum, enode = result.element_stress(0)
    return stress


async def time(websocket, path):
    while True:
        try:
            _uz = await websocket.recv()
            # print(f"{name}")
            _se = producer(float(_uz))
            # await websocket.send(str(_se.force['N']))
            await websocket.send('\n'.join(map(str, _se)))
            await asyncio.sleep(0.001)
        except websockets.WebSocketException:
            print('客户端连接断开！')
            break
    return


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

start_server = websockets.serve(time, "127.0.0.1", 3001)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
