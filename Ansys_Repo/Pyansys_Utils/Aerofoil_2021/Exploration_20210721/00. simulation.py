'''
2021.07.24
映射的壳单元组成的机翼结构
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

# k7 = mapdl.k("", 0.06, 0.025, 0)
# k8 = mapdl.k("", 0.14, 0.025, 0)
# k9 = mapdl.k("", 0.21, 0.025, 0)

l1 = mapdl.l(k1, k2)
l2 = mapdl.l(k2, k3)
l3 = mapdl.l(k3, k4)
l4 = mapdl.l(k4, k5)
l5 = mapdl.l(k5, k6)
l6 = mapdl.l(k6, k1)

anum = mapdl.al(l1, l2, l3, l4, l5, l6)

# mapdl.kplot(show_keypoint_numbering=True,
#             background='black',
#             show_bounds=True,
#             font_size=26)
# mapdl.lplot(show_keypoint_numbering=True,
#             color_lines=True,
#             show_line_numbering=False,
#             background='black',
#             show_bounds=True,
#             line_width=5,
#             cpos='xy',
#             font_size=26)
''' Meshing '''
mapdl.et(1, 181)
mapdl.type(1)
# mapdl.r(1, 0.00115)
mapdl.esize(0.005)
mapdl.mshkey(key=1)
mapdl.mshape(key=2, dimension='2D')
mapdl.amap(area=1, kp1=k1, kp2=k2, kp3=k4, kp4=k5)
# mapdl.etcontrol('set')
mapdl.amesh('ALL')
mapdl.sectype(1, "SHELL")
mapdl.secdata(0.00115)
mapdl.secoffset('MID')
# print(list(map(lambda x: x[-4:], mapdl.mesh.elem)))
# mapdl.nplot(cpos='ISO')

# mapdl.nsel('S', 'LOC', 'X', 0.07, 0.08, 0.01)
# aa = mapdl.nsel('R', 'LOC', 'Y', 0.025)
# print(aa)
# mapdl.cm()

# mapdl.aplot(show_lines=True, line_width=5, show_bounds=True, cpos='xy')
mapdl.eplot(show_bounds=True, show_node_numbering=True, cpos='ISO')
# mapdl.eplot(show_bounds=True, cpos='ISO')
''' Material Properties '''
mapdl.mp('EX', 1, 7.1e10)
mapdl.mp('NUXY', 1, 0.33)
mapdl.mp('DENS', 1, 2.83e3)

''' Boundary Conditions '''
# Fix the left-hand side of the aerofoil.
mapdl.nsel('S', 'LOC', 'X', 0)
mapdl.d("all", "all")
# Apply a force on the right-hand side of the aerofoil.
mapdl.nsel('S', 'LOC', 'X', 0.28)
assert np.allclose(mapdl.mesh.nodes[:, 0], 0.28)
# mapdl.cp(5, 'UZ', 'ALL')
# mapdl.nsel('R', 'LOC', 'Y', 0.008)
# start = time.clock()
mapdl.d("ALL", "UZ", 0.08)
# mapdl.nsel("ALL")

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
n_selected_list = []
n_selected_result_list = []
n_selected_result_list1 = []
result = mapdl.result

for _dx in [0.06, 0.14, 0.21, 0.28]:
    mapdl.parameters['mdx'] = _dx
    mapdl.nsel('S', '', '', 'NODE(mdx,0.025,0)')
    # mapdl.nsel('R', 'LOC', 'Y', 0.025)
    # mapdl.run('rot_x=ROTX(NODE(' + str(_dx) + ',0.025,0))')
    mapdl.get(par='n_numb', entity='NODE', item1='NUM', it1num='MIN')
    n_selected_list.append(mapdl.parameters['n_numb'])
    nnum1, displacement = result.nodal_displacement(rnum=0, nodes=[int(mapdl.parameters['n_numb'])])
    # n_selected_result_list.append(mapdl.post_processing.nodal_rotation(component='X'))
    n_selected_result_list.append(displacement)
    # n_selected_result_list1.append(mapdl.parameters['rot_x'])
    print(nnum1)
    # mapdl.cm(cname='N_' + str(_i + 1), entity='NODE')
print(n_selected_list)
print(n_selected_result_list)
print(n_selected_result_list1)

# grab the result from the ``mapdl`` instance
# result = mapdl.result
# result.nodal_solution(0)
# print(result.nodal_solution(0))
# m = mapdl.post_processing
# nnum1, displacement = result.nodal_displacement(rnum=0, nodes=[1])
# print(nnum1)
# print(displacement)
# end = time.clock()
# print(end - start)
# result.plot_principal_nodal_stress(0, 'SEQV', lighting=False,
#                                    cpos='iso', background='w',
#                                    text_color='k', add_text=False,
#                                    show_edges=True, show_displacement=True)
# mapdl.post_processing.plot_nodal_displacement('Z')
# result.plot_nodal_displacement(0, 'UZ')
# nnum, stress = result.nodal_stress(0)
# nnum1, displacement = result.nodal_displacement(0)
# element_stress, elemnum, enode = result.element_stress(0)
# # print(nnum)
# print(stress)
# # print(nnum1)
# print(displacement)
# print('\n'.join(map(str, displacement)))