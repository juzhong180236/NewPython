'''
2021.07.27
将机翼划分为多个四边形区域，每个四边形由6个关键点包围而成
'''
import numpy as np
from ansys.mapdl.core import launch_mapdl
import time
import json

mapdl = launch_mapdl()
mapdl.clear()
length = 0.28
height1 = 0.05
x1 = 0.06
x_separation = 0.07
y1 = 0.00943
y2 = 0.02543
y_mid = 0.025


def line(_x1, _y1, _x2, _y2, _x):
    return (_y2 - _y1) / (_x2 - _x1) * (_x - _x1) + _y1


''' Geometry '''
mapdl.prep7()
mapdl.units('SI')
line_1_k = []
line_2_k = []
line_mid1_k = []
for _x in np.linspace(0, x1, 7):
    line_1_k.append(mapdl.k("", _x, 0, 0))
    line_2_k.append(mapdl.k("", _x, height1, 0))
    line_mid1_k.append(mapdl.k("", _x, y_mid, 0))
for _i in range(len(line_mid1_k) - 1):
    mapdl.a(line_1_k[_i], line_mid1_k[_i], line_2_k[_i], line_2_k[_i + 1], line_mid1_k[_i + 1], line_1_k[_i + 1])
line_3_k = []
line_4_k = []
line_mid2_k = []
for _x in np.linspace(x1 + 0.01, length, 22):
    line_3_k.append(mapdl.k("", _x, line(x1, 0, length, y1, _x), 0))
    line_4_k.append(mapdl.k("", _x, line(x1, height1, length, y2, _x), 0))
    line_mid2_k.append(mapdl.k("", _x, y_mid, 0))
a1 = mapdl.a(line_1_k[6], line_mid1_k[6], line_2_k[6], line_4_k[0], line_mid2_k[0], line_3_k[0])
# # mapdl.kplot(show_keypoint_numbering=True, background='black', show_bounds=True, font_size=26)
for _i in range(len(line_mid2_k) - 1):
    mapdl.a(line_3_k[_i], line_mid2_k[_i], line_4_k[_i], line_4_k[_i + 1], line_mid2_k[_i + 1], line_3_k[_i + 1])
# mapdl.aplot(show_lines=True, line_width=1, show_bounds=True, cpos='xy')

''' Meshing '''
mapdl.et(1, 181)
mapdl.type(1)
mapdl.esize(0.01)
mapdl.mshkey(key=1)
mapdl.mshape(key=2, dimension='2D')
for _i in range(len(line_mid1_k) - 1):
    mapdl.amap(1 + _i, line_1_k[_i], line_2_k[_i], line_2_k[_i + 1], line_1_k[_i + 1])
mapdl.amap(a1, line_1_k[6], line_2_k[6], line_3_k[0], line_4_k[0])
_index = len(line_mid1_k) + 1
for _i in range(len(line_mid2_k) - 1):
    mapdl.amap(_index + _i, line_3_k[_i], line_4_k[_i], line_4_k[_i + 1], line_3_k[_i + 1])
mapdl.amesh('ALL')
mapdl.sectype(1, "SHELL")
mapdl.secdata(0.00115)
mapdl.secoffset('MID')
mapdl.eplot(show_bounds=True, show_node_numbering=True, cpos='ISO')

''' Material Properties '''
mapdl.mp('EX', 1, 7.1e10)
mapdl.mp('NUXY', 1, 0.33)
mapdl.mp('DENS', 1, 2.83e3)

''' Boundary Conditions '''
mapdl.nsel('S', 'LOC', 'X', 0)
mapdl.d("all", "all")
mapdl.finish()

x_train = []
y_train = []
time_list = []
''' Solve In Different Conditions '''
i_count = 1
i_sum = 0
for _dx in map(lambda x: round(x, 2), np.linspace(0.05, length, 24)):
    for _uz in map(lambda x: round(x, 3), np.arange(0.001, 0.5 * _dx + 0.01, 0.01)):
        i_sum += 1

for _dx in map(lambda x: round(x, 2), np.linspace(0.05, length, 24)):
    for _uz in map(lambda x: round(x, 3), np.arange(0.001, 0.5 * _dx + 0.01, 0.01)):
        # print(_dx, _uz)
        x_train.append([_dx, _uz])
        mapdl.prep7()
        start = time.perf_counter()
        mapdl.nsel('S', 'LOC', 'X', _dx)
        assert np.allclose(mapdl.mesh.nodes[:, 0], _dx)
        mapdl.d("ALL", "UZ", _uz)
        mapdl.finish()

        ''' Solve '''
        mapdl.slashsolu()
        mapdl.antype(antype='STATIC')
        mapdl.eqslv(lab='SPARSE', keepfile=1)  # 0.5193
        mapdl.nlgeom(key='ON')
        mapdl.solve()
        output = mapdl.finish()

        ''' Post-Processing '''
        mapdl.run('/POST1')
        results_selected_nodes_dict = {}
        result = mapdl.result

        for _sx in [0.06, 0.14, 0.21, 0.28]:
            mapdl.nsel('S', 'LOC', 'X', _sx)
            mapdl.nsel('R', 'LOC', 'Y', y_mid)
            mapdl.get(par='n_numb', entity='NODE', item1='NUM', it1num='MIN')
            mapdl.run('n_rot_y=ROTY(n_numb)')
            results_selected_nodes_dict[int(mapdl.parameters['n_numb'])] = mapdl.parameters['n_rot_y'] * 180 / np.pi
            # nnum1, displacement = result.nodal_displacement(rnum=0, nodes=[int(mapdl.parameters['n_numb'])])
        displacement_z = mapdl.post_processing.nodal_displacement(component='Z')
        # stress_eqv = mapdl.post_processing.nodal_eqv_stress
        num1, stress_eqv = result.principal_nodal_stress(rnum=0)
        end = time.perf_counter()
        i_count += 1
        print('\r' + '程序' + str(i_count) + '正在运行...' + ' 当前程序总进程为' + str(
            round(i_count / i_sum * 100, 2)) + '%', end="")
        time_list.append(end - start)
        # print("每一步运行的时间为：" + str(end - start) + "秒")
        # result.plot_principal_nodal_stress(0, 'SEQV', lighting=False,
        #                                    cpos='iso', background='w',
        #                                    text_color='k', add_text=False,
        #                                    show_edges=True, show_displacement=True)
        mapdl.finish()
        mapdl.prep7()
        mapdl.nsel('S', 'LOC', 'X', _dx)
        mapdl.ddele(node="ALL", lab="UZ")
        mapdl.finish()
        y_train_step_data = {
            "displacement_z": displacement_z.tolist(),
            "stress_eqv": stress_eqv[:, 4].tolist(),
            "sensor_rotation": results_selected_nodes_dict,
        }
        y_train.append(y_train_step_data)
print(np.average(time_list))
json_model = json.dumps(y_train)
with open(r"./json_data/performance_data.json", "w") as f:
    json.dump(json_model, f)
