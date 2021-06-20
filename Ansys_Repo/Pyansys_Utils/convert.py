# import pyansys

# pyansys.convert_script('../APDL/apdl_disp_pump_bytime.txt', 'pump.py')

from ansys.mapdl.core import launch_mapdl

exec_loc = r'C:\Program Files\ANSYS Inc\v211\ansys\bin\winx64\ANSYS211.exe'
mapdl = launch_mapdl(exec_loc)
print(mapdl)