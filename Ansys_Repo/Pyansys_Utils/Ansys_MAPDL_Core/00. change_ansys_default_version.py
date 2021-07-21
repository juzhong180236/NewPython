'''
2021.07.18
ansys.mapdl默认根据环境变量来获取到mapdl库的位置，如果安装有多个ansys，可以明确指定某个ansys的路径，
以获取到所需版本的ansys。此外还可以用以下的代码直接更改默认的路径，从而可以在此后的代码书写中省略路径。
'''
import ansys.mapdl.core as pymapdl

new_path = r'C:\Program Files\ANSYS Inc\v211\ANSYS\bin\winx64\ansys211.exe'
pymapdl.change_default_ansys_path(new_path)
