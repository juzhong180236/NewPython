# sphinx_gallery_thumbnail_number = 3

import matplotlib.pyplot as plt
import numpy as np

from ansys.mapdl.core import launch_mapdl

mapdl = launch_mapdl()

''' Element Type and Material Properties '''
mapdl.prep7()
mapdl.units('SI')  # SI - International system (m, kg, s, K).

# define a PLANE183 element type with thickness
mapdl.et(1, "PLANE183", kop3=3)
mapdl.r(1, 0.001)  # thickness of 0.001 meters)

# Define a material (nominal steel in SI)
mapdl.mp('EX', 1, 210E9)  # Elastic moduli in Pa (kg/(m*s**2))
mapdl.mp('DENS', 1, 7800)  # Density in kg/m3
mapdl.mp('NUXY', 1, 0.3)  # Poisson's Ratio

# list currently defined material properties
print(mapdl.mplist())

''' Geometry '''
length = 0.4
width = 0.1

ratio = 0.3  # diameter/width
diameter = width * ratio
radius = diameter * 0.5

# create the rectangle
rect_anum = mapdl.blc4(width=length, height=width)

# create a circle in the middle of the rectangle
circ_anum = mapdl.cyl4(length / 2, width / 2, radius)

# Note how pymapdl parses the output and returns the area numbers
# created by each command.  This can be used to execute a boolean
# operation on these areas to cut the circle out of the rectangle.
plate_with_hole_anum = mapdl.asba(rect_anum, circ_anum)

# finally, plot the lines of the plate
_ = mapdl.lplot(cpos='xy', line_width=3, font_size=26,
                color_lines=True, background='w')

''' Meshing '''
# ensure there are at 50 elements around the hole
hole_esize = np.pi * diameter / 50  # 0.0002
plate_esize = 0.01

# increased the density of the mesh at the center
mapdl.lsel('S', 'LINE', vmin=5, vmax=8)
mapdl.lesize('ALL', hole_esize, kforc=1)
mapdl.lsel('ALL')

# Decrease the area mesh expansion.  This ensures that the mesh
# remains fine nearby the hole
mapdl.mopt('EXPND', 0.7)  # default 1

mapdl.esize(plate_esize)
mapdl.amesh(plate_with_hole_anum)
_ = mapdl.eplot(vtk=True, cpos='xy', show_edges=True, show_axes=False,
                line_width=2, background='w')

''' Boundary Conditions '''
# Fix the left-hand side.
mapdl.nsel('S', 'LOC', 'X', 0)
mapdl.d('ALL', 'UX')

# Fix a single node on the left-hand side of the plate in the Y
# direction.  Otherwise, the mesh would be allowed to move in the y
# direction and would be an improperly constrained mesh.
mapdl.nsel('R', 'LOC', 'Y', width / 2)
assert mapdl.mesh.n_node == 1
mapdl.d('ALL', 'UY')

# Apply a force on the right-hand side of the plate.  For this
# example, we select the nodes at the right-most side of the plate.
mapdl.nsel('S', 'LOC', 'X', length)

# Verify that only the nodes at length have been selected:
assert np.allclose(mapdl.mesh.nodes[:, 0], length)

# Next, couple the DOF for these nodes.  This lets us provide a force
# to one node that will be spread throughout all nodes in this coupled
# set.
mapdl.cp(5, 'UX', 'ALL')

# Select a single node in this set and apply a force to it
# We use "R" to re-select from the current node group
mapdl.nsel('R', 'LOC', 'Y', width / 2)
mapdl.f('ALL', 'FX', 1000)

# finally, be sure to select all nodes again to solve the entire solution
_ = mapdl.allsel()

mapdl.run('/SOLU')
mapdl.antype('STATIC')
output = mapdl.solve()
print(output)

# grab the result from the ``mapdl`` instance
result = mapdl.result
result.plot_principal_nodal_stress(0, 'SEQV', lighting=False,
                                   cpos='xy', background='w',
                                   text_color='k', add_text=False)

nnum, stress = result.principal_nodal_stress(0)
von_mises = stress[:, -1]  # von-Mises stress is the right most column

# Must use nanmax as stress is not computed at mid-side nodes
max_stress = np.nanmax(von_mises)
