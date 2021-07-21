'''
2021.07.18
post_processing or we can use ansys-dpf-core library.
'''
import os
import numpy as np
from ansys.mapdl.core import launch_mapdl

'''
Script Initialization
'''
mapdl = launch_mapdl()
# define cylinder and mesh parameters
torque = 100
radius = 2
h_tip = 2
height = 20
elemsize = 0.5
pi = np.pi
force = 100 / radius
pressure = force / (h_tip * 2 * np.pi * radius)

'''
Model Creation
'''
# Define higher-order SOLID186
# Define surface effect elements SURF154 to apply torque
# as a tangential pressure
mapdl.prep7()
mapdl.et(1, 186)  # mapdl.et(1, 'SOLID186')
mapdl.et(2, 154)
mapdl.r(1)
mapdl.r(2)

# Aluminum properties (or something)
mapdl.mp('ex', 1, 10e6)
mapdl.mp('nuxy', 1, 0.3)
mapdl.mp('dens', 1, 0.1 / 386.1)
mapdl.mp('dens', 2, 0)

# Simple cylinder
for i in range(4):
    mapdl.cylind(radius, '', '', height, 90 * (i - 1), 90 * i)

mapdl.nummrg('kp')

# interactive volume plot (optional)
# mapdl.vplot()

# mesh cylinder
mapdl.lsel('s', 'loc', 'x', 0)
mapdl.lsel('r', 'loc', 'y', 0)
mapdl.lsel('r', 'loc', 'z', 0, height - h_tip)
mapdl.lesize('all', elemsize * 2)
mapdl.mshape(0)
mapdl.mshkey(1)
mapdl.esize(elemsize)
mapdl.allsel('all')
mapdl.vsweep('ALL')
mapdl.csys(1)
mapdl.asel('s', 'loc', 'z', '', height - h_tip + 0.0001)
mapdl.asel('r', 'loc', 'x', radius)
mapdl.local(11, 1)
mapdl.csys(0)
mapdl.aatt(2, 2, 2, 11)
mapdl.amesh('all')
mapdl.finish()

# plot elements
mapdl.eplot()

'''
Solution
'''
# new solution
mapdl.slashsolu()  # Using Slash instead of / due to duplicate SOLU command
# ansys('/solu')  # could also use this line
mapdl.antype('static', 'new')
mapdl.eqslv('pcg', 1e-8)

# Apply tangential pressure
mapdl.esel('s', 'type', '', 2)
mapdl.sfe('all', 2, 'pres', '', pressure)

# Constrain bottom of cylinder/rod
mapdl.asel('s', 'loc', 'z', 0)
mapdl.nsla('s', 1)

mapdl.d('all', 'all')
mapdl.allsel()
mapdl.psf('pres', '', 2)
mapdl.pbc('u', 1)
mapdl.solve()

# access the result from the mapdl result
result = mapdl.result

# alternatively, open the result file using the path used in MAPDL
# from ansys.mapdl import reader as pymapdl_reader
# resultfile = os.path.join(mapdl.path, 'file.rst')
# result = pymapdl_reader.read_binary(resultfile)

# access element results as arrays
nnum, stress = result.nodal_stress(0)
element_stress, elemnum, enode = result.element_stress(0)
nodenum, stress1 = result.nodal_stress(0)

# plot interactively
result.plot_nodal_solution(0, cmap='bwr')
result.plot_nodal_stress(0, 'X', cmap='bwr')
result.plot_principal_nodal_stress(0, 'SEQV', cmap='bwr')

# plot and save non-interactively
# (cpos was output from ``cpos = result.plot()`` and setting up
# the correct camera angle)
# cpos = [(20.992831318277517, 9.78629316586435, 31.905115108541928),
#         (0.35955395443745797, -1.4198191001571547, 10.346158032932495),
#         (-0.10547549888485548, 0.9200673323892437, -0.377294345312956)]
#
# result.plot_nodal_displacement(0, cpos=cpos, savefig='cylinder_disp.png')
# result.plot_nodal_stress(0, 'Sx', cmap='bwr', cpos=cpos, screenshot='cylinder_sx.png')
# result.plot_principal_nodal_stress(0, 'SEQV', cmap='bwr', cpos=cpos, screenshot='cylinder_vonmises.png')

disp_x = mapdl.post_processing.nodal_displacement('X')
print(disp_x)
mapdl.post_processing.plot_nodal_displacement('X')

# 展示选择的节点或单元的后处理结果
mapdl.nsel('S', 'NODE', vmin=1, vmax=2000)
mapdl.esel('S', 'ELEM', vmin=500, vmax=2000)
mask = mapdl.post_processing.selected_nodes
mapdl.post_processing.plot_nodal_displacement('X')