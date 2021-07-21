import ansys.mapdl.core as pymapdl

inputfile = 'ansys_inputfile.inp'
pyscript = 'pyscript.py'
pymapdl.convert_script(inputfile, pyscript)
