'''
2021.07.18
设置ansys运行时所产生临时文件的位置。
'''
from ansys.mapdl.core import launch_mapdl
import os

path = os.getcwd()
exec_loc = r'C:\Program Files\ANSYS Inc\v211\ansys\bin\winx64\ANSYS211.exe'
mapdl = launch_mapdl(exec_loc, nproc=4, run_location=path)
