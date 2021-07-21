'''
2021.07.18
ansys.mapdl默认根据环境变量来获取到mapdl库的位置，如果安装有多个ansys，
可以明确指定某个ansys的路径，以获取到所需版本的ansys。
'''
from ansys.mapdl.core import launch_mapdl

exec_loc = r'C:\Program Files\ANSYS Inc\v211\ansys\bin\winx64\ANSYS211.exe'
mapdl = launch_mapdl(exec_loc, nproc=4)
