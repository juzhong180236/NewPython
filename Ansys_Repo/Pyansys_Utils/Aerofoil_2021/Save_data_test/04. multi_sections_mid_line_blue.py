'''
2021.07.27
将机翼划分为多个四边形区域，每个四边形由4个关键点包围而成
但是这会导致机翼中间的应力计算出错，中轴线应力最小
'''
import numpy as np
from ansys.mapdl.core import launch_mapdl
import time

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
    mapdl.a(line_1_k[_i], line_mid1_k[_i], line_mid1_k[_i + 1], line_1_k[_i + 1])
    mapdl.a(line_2_k[_i], line_mid1_k[_i], line_mid1_k[_i + 1], line_2_k[_i + 1])

line_3_k = []
line_4_k = []
line_mid2_k = []
for _x in np.linspace(x1 + 0.01, length, 22):
    line_3_k.append(mapdl.k("", _x, line(x1, 0, length, y1, _x), 0))
    line_4_k.append(mapdl.k("", _x, line(x1, height1, length, y2, _x), 0))
    line_mid2_k.append(mapdl.k("", _x, y_mid, 0))

a1 = mapdl.a(line_1_k[6], line_mid1_k[6], line_mid2_k[0], line_3_k[0])
a2 = mapdl.a(line_2_k[6], line_mid1_k[6], line_mid2_k[0], line_4_k[0])

# mapdl.kplot(show_keypoint_numbering=True, background='black', show_bounds=True, font_size=26)


for _i in range(len(line_mid2_k) - 1):
    mapdl.a(line_3_k[_i], line_mid2_k[_i], line_mid2_k[_i + 1], line_3_k[_i + 1])
    mapdl.a(line_4_k[_i], line_mid2_k[_i], line_mid2_k[_i + 1], line_4_k[_i + 1])

# mapdl.aplot(show_lines=True, line_width=5, show_bounds=True, cpos='xy')

''' Meshing '''
mapdl.et(1, 181)
mapdl.type(1)
mapdl.esize(0.01)
mapdl.mshkey(key=1)
mapdl.mshape(key=2, dimension='2D')

for _i in range(len(line_mid1_k) - 1):
    mapdl.amap(1 + _i * 2, line_1_k[_i], line_mid1_k[_i], line_mid1_k[_i + 1], line_1_k[_i + 1])
    mapdl.amap(2 + _i * 2, line_2_k[_i], line_mid1_k[_i], line_mid1_k[_i + 1], line_2_k[_i + 1])

mapdl.amap(a1, line_1_k[6], line_mid1_k[6], line_mid2_k[0], line_3_k[0])
mapdl.amap(a2, line_2_k[6], line_mid1_k[6], line_mid2_k[0], line_4_k[0])

_index = (len(line_mid1_k) - 1) * 2 + 3
for _i in range(len(line_mid2_k) - 1):
    mapdl.amap(_index + _i * 2, line_3_k[_i], line_mid2_k[_i], line_mid2_k[_i + 1], line_3_k[_i + 1])
    mapdl.amap(_index + _i * 2 + 1, line_4_k[_i], line_mid2_k[_i], line_mid2_k[_i + 1], line_4_k[_i + 1])

mapdl.amesh('ALL')
mapdl.sectype(1, "SHELL")
mapdl.secdata(0.00115)
mapdl.secoffset('MID')
# mapdl.eplot(show_bounds=True, show_node_numbering=True, cpos='ISO')

''' Material Properties '''
mapdl.mp('EX', 1, 7.1e10)
mapdl.mp('NUXY', 1, 0.33)
mapdl.mp('DENS', 1, 2.83e3)

''' Boundary Conditions '''
mapdl.nsel('S', 'LOC', 'X', 0)
mapdl.d("all", "all")

# for _dx in np.linspace(0.05, length, 24):
#     # temp = []
#     for _uz in np.arange(0.001, 0.5 * _dx + 0.01, 0.01):
#         # temp.append([_dx, _uz])
start = time.perf_counter()
mapdl.nsel('S', 'LOC', 'X', 0.28)
assert np.allclose(mapdl.mesh.nodes[:, 0], 0.28)
mapdl.d("ALL", "UZ", 0.08)
mapdl.finish()  # 退出prep7处理器

''' Solve '''
mapdl.slashsolu()
mapdl.antype(antype='STATIC')
mapdl.eqslv(lab='SPARSE', keepfile=1)  # 0.5193
# mapdl.eqslv(lab='JCG')  # 1.5536
# mapdl.eqslv(lab='ICCG')  # 30.8854
# mapdl.eqslv(lab='QMR')  # 0.5074
# mapdl.eqslv(lab='PCG')  # 0.7199
mapdl.nlgeom(key='ON')
mapdl.solve()
output = mapdl.finish()
#
# ''' Post-Processing '''
mapdl.run('/POST1')
results_selected_nodes_dict = {}
result = mapdl.result

for _dx in np.linspace(0.05, 0.28, 24):
    # mapdl.parameters['mdx'] = _dx
    # mapdl.nsel('S', '', '', 'NODE(mdx,0.025,0)')
    mapdl.nsel('S', 'LOC', 'X', _dx)
    mapdl.nsel('R', 'LOC', 'Y', y_mid)
    mapdl.get(par='n_numb', entity='NODE', item1='NUM', it1num='MIN')
    mapdl.run('n_rot_y=ROTY(n_numb)')

    results_selected_nodes_dict[int(mapdl.parameters['n_numb'])] = mapdl.parameters['n_rot_y'] * 180 / np.pi
    # nnum1, displacement = result.nodal_displacement(rnum=0, nodes=[int(mapdl.parameters['n_numb'])])

print(results_selected_nodes_dict)
print(len(results_selected_nodes_dict.values()))
# mapdl.eplot(show_node_numbering=True, show_bounds=True, cpos='ISO')

# end = time.perf_counter()
# print(start - end)
# result = mapdl.result
result.plot_principal_nodal_stress(0, 'SEQV', lighting=False,
                                   cpos='iso', background='w',
                                   text_color='k', add_text=False,
                                   show_edges=True, show_displacement=True)
