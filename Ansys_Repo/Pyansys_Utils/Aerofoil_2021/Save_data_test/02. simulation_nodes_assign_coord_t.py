'''
2021.07.26
由点到线，由线到面，在特定位置设定关键点，进而在这些位置生成节点，
根据节点的坐标来定义需要输出结果的节点位置
'''
import numpy as np
from ansys.mapdl.core import launch_mapdl
import time

mapdl = launch_mapdl()
mapdl.clear()

''' Geometry '''
mapdl.prep7()
mapdl.units('SI')
k1 = mapdl.k("", 0, 0, 0)
k2 = mapdl.k("", 0, 0.05, 0)
k3 = mapdl.k("", 0.06, 0.05, 0)
k4 = mapdl.k("", 0.28, 0.02543, 0)
k5 = mapdl.k("", 0.28, 0.00943, 0)
k6 = mapdl.k("", 0.06, 0, 0)
k7 = mapdl.k("", 0.06, 0.025, 0)
k8 = mapdl.k("", 0.28, 0.025, 0)

k9 = mapdl.k("", 0.14, 0.025, 0)
k10 = mapdl.k("", 0.21, 0.025, 0)

l1 = mapdl.l(k1, k2)
l2 = mapdl.l(k2, k3)
l3 = mapdl.l(k3, k4)
# l4 = mapdl.l(k4, k5)
l5 = mapdl.l(k5, k6)
l6 = mapdl.l(k6, k1)
l7 = mapdl.l(k3, k7)
l8 = mapdl.l(k7, k6)

l9 = mapdl.l(k7, k9)

l10 = mapdl.l(k4, k8)
l11 = mapdl.l(k8, k5)

l12 = mapdl.l(k9, k10)
l13 = mapdl.l(k10, k8)

a1 = mapdl.al(l1, l2, l7, l8, l6)
a2 = mapdl.al(l3, l10, l13, l12, l9, l7)
a3 = mapdl.al(l9, l12, l13, l11, l5, l8)

''' Meshing '''
mapdl.et(1, 181)
mapdl.type(1)
mapdl.esize(0.01)
mapdl.mshkey(key=1)
mapdl.mshape(key=2, dimension='2D')
mapdl.amap(area=a1, kp1=k1, kp2=k2, kp3=k3, kp4=k6)
mapdl.amap(area=a2, kp1=k3, kp2=k7, kp3=k4, kp4=k8)
mapdl.amap(area=a3, kp1=k7, kp2=k6, kp3=k8, kp4=k5)
mapdl.amesh('ALL')
mapdl.sectype(1, "SHELL")
mapdl.secdata(0.00115)
mapdl.secoffset('MID')
# mapdl.eplot(show_bounds=True, show_node_numbering=True, cpos='ISO')
# mapdl.eplot(show_bounds=True, cpos='ISO')

''' Material Properties '''
mapdl.mp('EX', 1, 7.1e10)
mapdl.mp('NUXY', 1, 0.33)
mapdl.mp('DENS', 1, 2.83e3)

''' Boundary Conditions '''
mapdl.nsel('S', 'LOC', 'X', 0)
mapdl.d("all", "all")
mapdl.nsel('S', 'LOC', 'X', 0.28)
assert np.allclose(mapdl.mesh.nodes[:, 0], 0.28)

# start = time.clock()
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

''' Post-Processing '''
mapdl.run('/POST1')
results_selected_nodes_dict = {}
result = mapdl.result
for _i, _dx in enumerate([0.06, 0.14, 0.21, 0.28]):
    mapdl.nsel('S', 'LOC', 'X', _dx)
    mapdl.nsel('R', 'LOC', 'Y', 0.025)
    mapdl.get(par='n_numb', entity='NODE', item1='NUM', it1num='MIN')
    mapdl.run('n_rot_y=ROTY(n_numb)')

    results_selected_nodes_dict[int(mapdl.parameters['n_numb'])] = mapdl.parameters['n_rot_y'] * 180 / np.pi
    # nnum1, displacement = result.nodal_displacement(rnum=0, nodes=[int(mapdl.parameters['n_numb'])])

print(results_selected_nodes_dict)

result = mapdl.result
result.plot_principal_nodal_stress(0, 'SEQV', lighting=False,
                                   cpos='iso', background='w',
                                   text_color='k', add_text=False,
                                   show_edges=True, show_displacement=True)
