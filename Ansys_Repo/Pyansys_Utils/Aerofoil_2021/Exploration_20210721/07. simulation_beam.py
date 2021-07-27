'''
2021.07.24
单独一根梁
'''
import numpy as np
from ansys.mapdl.core import launch_mapdl
import time

mapdl = launch_mapdl()
mapdl.clear()

''' Geometry '''
mapdl.prep7()
mapdl.units('SI')

n1 = mapdl.n(1, 0, 0.025, 0)
n12 = mapdl.n(12, 0.14, 0.025, 0)
n23 = mapdl.n(23, 0.28, 0.025, 0)
mapdl.fill(n1, n12, 10)
mapdl.fill(n12, n23, 10)

# ''' Meshing '''
mapdl.et(1, 188)
for node in mapdl.mesh.nnum[:-1]:
    mapdl.e(node, node + 1)
mapdl.sectype(1, "BEAM", "RECT")
beam_info = mapdl.secdata(0.05, 0.00115)
mapdl.secoffset('CENT')
#
# mapdl.aplot(show_lines=True, line_width=5, show_bounds=True, cpos='xy')
# mapdl.eplot(show_bounds=True, cpos='iso')

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

mapdl.d("ALL", "UZ", 0.08)

# _ = mapdl.allsel()
mapdl.finish()  # 退出prep7处理器

''' Solve '''
mapdl.slashsolu()
mapdl.antype(antype='STATIC')
mapdl.eqslv(lab='SPARSE', keepfile=1)
mapdl.nlgeom(key='ON')
mapdl.solve()
output = mapdl.finish()
#
''' Post-Processing '''
# grab the result from the ``mapdl`` instance
result = mapdl.result
end = time.clock()
print(end - start)
# result.plot_principal_nodal_stress(0, 'SEQV', lighting=False,
#                                    cpos='ISO', background='w',
#                                    text_color='k', add_text=False,
#                                    show_edges=True, show_displacement=True)
# result.plot_nodal_displacement(0, 'UZ', lighting=False,
#                                cpos='XZ', background='w',
#                                text_color='k', add_text=False,
#                                show_edges=True, show_displacement=True)
# nnum, stress = result.nodal_stress(0)
# nnum1, displacement = result.nodal_displacement(0)
# element_stress, elemnum, enode = result.element_stress(0)
