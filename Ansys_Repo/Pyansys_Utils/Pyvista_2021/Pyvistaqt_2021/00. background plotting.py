import pyvista as pv
from pyvistaqt import BackgroundPlotter
import time

sphere = pv.Sphere()

plotter = BackgroundPlotter(title='Digital twin of aerofoil')
plotter.add_mesh(sphere)

# can now operate on the sphere and have it updated in the background
sphere.points *= 0.5
