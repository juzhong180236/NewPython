'''
2021.07.18
Mesh Geometry
'''
from ansys.mapdl.core import launch_mapdl
import numpy as np

mapdl = launch_mapdl()
# create a rectangle with a few holes
mapdl.prep7()
rect_anum = mapdl.blc4(width=1, height=0.2)
# create several circles in the middle in the rectangle
for x in np.linspace(0.1, 0.9, 8):
    mapdl.cyl4(x, 0.1, 0.025)
plate_holes = mapdl.asba(rect_anum, 'all')
mapdl.vext(plate_holes, dz=0.1)
mapdl.et(1, 'SOLID186')
mapdl.vsweep('ALL')
mapdl.esize(0.1)
# mapdl.eplot()
print(mapdl.mesh.nodes.shape)
print(mapdl.mesh)
print(mapdl.geometry)
