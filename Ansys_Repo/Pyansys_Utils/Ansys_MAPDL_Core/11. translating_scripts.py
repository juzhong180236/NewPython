'''
2021.07.18

'''
from ansys.mapdl.core import launch_mapdl
import numpy as np

mapdl = launch_mapdl()

# 这个也可以用mapdl.core，比如下面
import pyansys

inputfile = 'ansys_inputfile.inp'
pyscript = 'pyscript.py'
pyansys.convert_script(inputfile, pyscript)

# 用mapdl.core
import ansys.mapdl.core as pymapdl

pymapdl.convert_script(pymapdl.examples.vmfiles['vm1'], 'vm1.py')
# mapdl.get('DEF_Y', 'NODE', 2, 'U', 'Y')
# m1 = mapdl.parameters['DEF_Y']
# print(m1)
# m2 = mapdl.get_value('NODE', 2, 'U', 'Y')

mapdl.parameters['MY_ARRAY'] = np.arange(10000)
print(mapdl.parameters['MY_ARRAY'])

mapdl.parameters['MY_STRING'] = "helloworld"
print(mapdl.parameters['MY_STRING'])

print(mapdl.parameters.routine)
print(mapdl.parameters)
