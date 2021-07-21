import pyvista as pv
import pyvistaqt as pvqt
from pyvista import examples

dataset = examples.load_hexbeam()

p = pvqt.BackgroundPlotter()

p.add_mesh(dataset)

p.show_bounds(grid=True, location='back')