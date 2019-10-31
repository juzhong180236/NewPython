import numpy as np
import pykrige.kriging_tools as kt
from pykrige.ok import OrdinaryKriging
data = np.array([[0.3, 1.2, 0.47],
[1.9, 0.6, 0.56],
[1.1, 3.2, 0.74],
[3.3, 4.4, 1.47],
[4.7, 3.8, 1.74]])
gridx = np.arange(0.0, 5.5, 0.5)
gridy = np.arange(0.0, 5.5, 0.5)
OK = OrdinaryKriging(data[:, 0], data[:, 1], data[:, 2], variogram_model='linear',
verbose=False, enable_plotting=False)
z, ss = OK.execute('grid', gridx, gridy)
kt.write_asc_grid(gridx, gridy, z, filename="output.asc")