import pyvista as pv
from pyvistaqt import MultiPlotter

mp = MultiPlotter(nrows=2, ncols=2)
mp[0, 0].add_mesh(pv.Sphere())
mp[0, 1].add_mesh(pv.Cylinder())
mp[1, 0].add_mesh(pv.Cube())
mp[1, 1].add_mesh(pv.Cone())