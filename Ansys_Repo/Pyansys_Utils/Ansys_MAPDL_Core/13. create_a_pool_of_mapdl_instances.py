from ansys.mapdl.core import launch_mapdl
from ansys.mapdl.core import LocalMapdlPool

import os

my_path = os.getcwd()
# # mapdl = launch_mapdl()
pool = LocalMapdlPool(10, nproc=1, run_location=my_path)
from ansys.mapdl.core import examples

files = [examples.vmfiles['vm%d' % i] for i in range(1, 21)]
outputs = pool.run_batch(files)
len(outputs)
