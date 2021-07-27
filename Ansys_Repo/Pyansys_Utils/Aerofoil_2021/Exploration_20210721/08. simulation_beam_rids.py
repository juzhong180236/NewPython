'''
2021.07.24
去掉了横向排布的几根梁
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

l1 = mapdl.l(k1, k2)
l2 = mapdl.l(k2, k3)
l3 = mapdl.l(k3, k4)
l4 = mapdl.l(k4, k5)
l5 = mapdl.l(k5, k6)
l6 = mapdl.l(k6, k1)

k7 = mapdl.kl(l1, 0.5)
k8 = mapdl.kl(l2, 0.5)
# k9 = mapdl.kfill(k3, k4, 3)
k9 = mapdl.kl(l3, 0.25)
k10 = mapdl.kl(l3, 0.5)
k11 = mapdl.kl(l3, 0.75)

k12 = mapdl.k("", 0.28, 0.025, 0)
l7 = mapdl.l(k7, k12)
# k13 = mapdl.kl(l5, 0.25)
# k14 = mapdl.kl(l5, 0.5)
# k15 = mapdl.kl(l5, 0.75)
#
# k16 = mapdl.kl(l6, 0.5)
#
# # l7 = mapdl.l(k7, k12)
# l8 = mapdl.l(k8, k16)
# l9 = mapdl.l(k3, k6)
# l10 = mapdl.l(k9, k15)
# l11 = mapdl.l(k10, k14)
# l12 = mapdl.l(k11, k13)
#
# k17 = mapdl.kl(l8, 0.5)
# k18 = mapdl.kl(l9, 0.5)
# k19 = mapdl.kl(l10, 0.5)
# k20 = mapdl.kl(l11, 0.5)
# k21 = mapdl.kl(l12, 0.5)
#
# l7 = mapdl.l(k7, k17)
# l13 = mapdl.l(k17, k18)
# l14 = mapdl.l(k18, k19)
# l15 = mapdl.l(k19, k20)
# l16 = mapdl.l(k20, k21)
# l17 = mapdl.l(k21, k12)

# mapdl.kplot(show_keypoint_numbering=True,
#             background='black',
#             show_bounds=True,
#             font_size=26)
mapdl.lplot(show_keypoint_numbering=True,
            color_lines=True,
            show_line_numbering=False,
            background='black',
            show_bounds=True,
            line_width=5,
            cpos='xy',
            font_size=26)

''' Meshing '''
mapdl.et(1, 188)
mapdl.type(1)
mapdl.lesize('ALL', 0.005)
mapdl.lmesh('ALL')

# for node in mapdl.mesh.nnum[:-1]:
#     mapdl.e(node, node + 1)

mapdl.sectype(1, "BEAM", "RECT")
beam_info = mapdl.secdata(0.00115, 0.00115)
mapdl.secoffset('CENT')
#
# mapdl.aplot(show_lines=True, line_width=5, show_bounds=True, cpos='xy')
# mapdl.eplot(show_bounds=True, show_node_numbering=True, cpos='iso')
mapdl.eplot(show_bounds=True, cpos='iso')

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
start = time.clock()
mapdl.d("ALL", "UZ", 0.1)

# _ = mapdl.allsel()
mapdl.finish()  # 退出prep7处理器

''' Solve '''
mapdl.slashsolu()
mapdl.antype(antype='STATIC')
mapdl.eqslv(lab='SPARSE', keepfile=1)
mapdl.nlgeom(key='ON')
mapdl.solve()
output = mapdl.finish()
end = time.clock()
print(end - start)
#
''' Post-Processing '''
# grab the result from the ``mapdl`` instance
result = mapdl.result

# result.plot_principal_nodal_stress(0, 'SEQV', lighting=False,
#                                    cpos='ISO', background='w',
#                                    text_color='k', add_text=False,
#                                    show_edges=True, show_displacement=True)
result.plot_nodal_displacement(0, 'UZ', lighting=False,
                               cpos='XY', background='w',
                               text_color='k', add_text=False,
                               show_edges=True, show_displacement=True)
# nnum, stress = result.nodal_stress(0)
# nnum1, displacement = result.nodal_displacement(0)
# element_stress, elemnum, enode = result.element_stress(0)
