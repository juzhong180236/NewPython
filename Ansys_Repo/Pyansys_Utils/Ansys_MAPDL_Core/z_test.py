from ansys.mapdl.core import launch_mapdl
# from ansys.mapdl.core import Mapdl
# import os
# import sys
#
# # mapdl = Mapdl()
# # print(mapdl)
# # path = os.getcwd()
# exec_loc = r'C:\Program Files\ANSYS Inc\v211\ansys\bin\winx64\ANSYS211.exe'
# # mapdl = launch_mapdl(exec_loc, nproc=4, run_location=path)
mapdl = launch_mapdl(nproc=4)
# # mapdl.mute = True # 这个去掉就不会报错了
# mapdl.finish()
# mapdl.clear()
# mapdl.prep7()
# mapdl.k(1, 0, 0, 0)
# mapdl.k(2, 1, 0, 0)
# mapdl.k(3, 1, 1, 0)
# mapdl.k(4, 0, 1, 0)
# mapdl.l(1, 2)
# mapdl.l(2, 3)
# mapdl.l(3, 4)
# mapdl.l(4, 1)
# mapdl.al(1, 2, 3)
# # print(mapdl)
# # mapdl.clear()
# import ansys.mapdl.core as pymapdl
# new_path = r'C:\Program Files\ANSYS Inc\v211\ANSYS\bin\winx64\ansys211.exe'
# pymapdl.change_default_ansys_path(new_path)