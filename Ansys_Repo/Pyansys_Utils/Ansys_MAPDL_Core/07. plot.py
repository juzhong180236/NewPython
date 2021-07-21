'''
2021.07.18
KPLOT, LPLOT, APLOT, EPLOT
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
# Generate a line plot
# cpos控制摄像机的位置 xy平面
mapdl.lplot(color_lines=True, cpos='xy')
# mapdl.lplot(screenshot('aplot.png'))

plate_holes = mapdl.asba(rect_anum, 'all')

# extrude this area
mapdl.vext(plate_holes, dz=0.1)
mapdl.vplot()

mapdl.et(1, 'SOLID186')
mapdl.vsweep('ALL')
mapdl.esize(0.1)
mapdl.eplot()
'''
用matplotlib画图
'''
# # create a square area using keypoints
# mapdl.prep7()
# mapdl.k(1, 0, 0, 0)
# mapdl.k(2, 1, 0, 0)
# mapdl.k(3, 1, 1, 0)
# mapdl.k(4, 0, 1, 0)
# mapdl.l(1, 2)
# mapdl.l(2, 3)
# mapdl.l(3, 4)
# mapdl.l(4, 1)
# mapdl.al(1, 2, 3, 4)
#
# # sets the view to "isometric"
# mapdl.view(1, 1, 1, 1)
# mapdl.pnum('kp', 1)  # enable keypoint numbering
# mapdl.pnum('line', 1)  # enable line numbering
#
# # each of these will create a matplotlib figure and pause execution
# mapdl.aplot(vtk=False)
# mapdl.lplot(vtk=False)
# mapdl.kplot(vtk=False)