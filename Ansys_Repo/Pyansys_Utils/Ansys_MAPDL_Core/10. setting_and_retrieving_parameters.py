'''
2021.07.18
Customized parameters, like arrays, variables and so on.
'''
from ansys.mapdl.core import launch_mapdl
import numpy as np

mapdl = launch_mapdl()
# mapdl.get('DEF_Y', 'NODE', 2, 'U', 'Y')
# m = mapdl.parameters['DEF_Y']
# print(m)
mapdl.parameters['MY_ARRAY'] = np.arange(10000)
print(mapdl.parameters['MY_ARRAY'])

mapdl.parameters['MY_STRING'] = "helloworld"
print(mapdl.parameters['MY_STRING'])

print(mapdl.parameters.routine)
