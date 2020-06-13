import os
import sys
import pyansys as py
import numpy as np
from pyansys import examples


def create_dir_in_current(dirname):
    path = sys.path[0] + '\\' + dirname
    if os.path.exists(path):
        print(path + ' 目录已存在')
        return path
    else:
        os.mkdir(path)
        print(path + ' 创建成功')
        return path


path = create_dir_in_current('test_second')
# run ansys with interactive plotting enabled
ansys = py.Mapdl(interactive_plotting=True, run_location=path)

# create a square area using keypoints
ansys.prep7()
ansys.k(1, 0, 0, 0)
ansys.k(2, 1, 0, 0)
ansys.k(3, 1, 1, 0)
ansys.k(4, 0, 1, 0)
ansys.l(1, 2)
ansys.l(2, 3)
ansys.l(3, 4)
ansys.l(4, 1)
ansys.al(1, 2, 3, 4)

# # sets the view to "isometric"
# ansys.view(1, 1, 1, 1)
# ansys.pnum('kp', 1)  # enable keypoint numbering
# ansys.pnum('line', 1)  # enable line numbering
#
# # each of these will create a matplotlib figure and pause execution
# ansys.aplot()
# ansys.lplot()
# ansys.kplot()
# # open up the gui
# ansys.open_gui()
#
# # it resumes where you left off...
# ansys.et(1, 'MESH200', 6)
# ansys.amesh('all')
# ansys.eplot()
