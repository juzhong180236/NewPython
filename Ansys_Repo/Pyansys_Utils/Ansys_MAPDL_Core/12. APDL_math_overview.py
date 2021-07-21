import re
import numpy as np
from ansys.mapdl.core import launch_mapdl

mapdl = launch_mapdl()

# setup the full file
mapdl.prep7()
mapdl.block(0, 1, 0, 1, 0, 1)
mapdl.et(1, 186)
mapdl.esize(0.5)
mapdl.vmesh('all')

# Define a material (nominal steel in SI)
mapdl.mp('EX', 1, 210E9)  # Elastic moduli in Pa (kg/(m*s**2))
mapdl.mp('DENS', 1, 7800)  # Density in kg/m3
mapdl.mp('NUXY', 1, 0.3)  # Poisson's Ratio

# solve first 10 non-trivial modes
out = mapdl.modal_analysis(nmode=10, freqb=1)

# store the first 10 natural frequencies
mapdl.post1()
resp = mapdl.set('LIST')
w_n = np.array(re.findall(r'\s\d*\.\d\s', resp), np.float32)
print(w_n)

mm = mapdl.math

# load by default from file.full
k = mm.stiff()
m = mm.mass()

# convert to numpy
k_py = k.asarray()
m_py = m.asarray()
# These matrices are now solely stored within Python now that we’ve cleared mapdl.
mapdl.clear()
print(k_py)

my_stiff = mm.matrix(k_py, triu=True)
my_mass = mm.matrix(m_py, triu=True)

# solve for the first 10 modes above 1 Hz
nmode = 10
mapdl_vec = mm.eigs(nmode, my_stiff, my_mass, fmin=1)
eigval = mapdl_vec.asarray()
print(eigval)
# The MAPDL Math matrix eigvec now contains the eigenvectors for the solution.
eigvec = mm.zeros(my_stiff.nrow, nmode)  # for eigenvectors
val = mm.eigs(nmode, my_stiff, my_mass, fmin=1)
print(eigvec)
print(val)