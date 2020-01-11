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


# path = r'D:\Alai\ansys_Alai\Crane\Crane_Parts_v2.0\rod\20191223 wanggedi_files\dp0\SYS-6\MECH\file.rst'
# result = py.read_binary(path)
# nn = result.principal_nodal_stress(0)

# examples.ansys_cylinder_demo()
path = create_dir_in_current('test_first')
ansys = py.Mapdl(run_location=path)
ansys.run('/PREP7')
ansys.run('K, 1, 0, 0, 0')
ansys.run('K, 2, 1, 0, 0')
ansys.run('K, 3, 1, 1, 0')
ansys.run('K, 4, 0, 1, 0')
ansys.run('L, 1, 2')
ansys.run('L, 2, 3')
ansys.run('L, 3, 4')
ansys.run('L, 4, 1')
ansys.run('AL, 1, 2, 3, 4')
# clear existing geometry
ansys.finish()
ansys.clear()

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
# clear existing geometry
ansys.finish()
ansys.clear()
# make 10 random keypoints in ANSYS
points = np.random.random((10, 3))
ansys.prep7()
for i, (x, y, z) in enumerate(points):
    ansys.k(i + 1, x, y, z)
ansys.get('DEF_Y', 'NODE', 2, 'U', 'Y')
ansys.load_parameters()
ansys.finish()
ansys.clear()
ansys.allow_ignore = True
ansys.k()  # error ignored
