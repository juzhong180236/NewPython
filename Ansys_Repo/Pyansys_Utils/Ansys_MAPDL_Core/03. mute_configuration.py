'''
2021.07.18
屏蔽apdl向python发送的信息。
'''
from ansys.mapdl.core import launch_mapdl

exec_loc = r'C:\Program Files\ANSYS Inc\v211\ansys\bin\winx64\ANSYS211.exe'
mapdl = launch_mapdl(exec_loc, nproc=4)
mapdl.mute = True  # 会阻断apdl向python传输的信息，甚至不会报错
# 或者对特定的语句mute
# mapdl.run('/PREP7', mute=True)
# mapdl.prep7(mute=True)
# 对特定的语句verbose
# mapdl.solve(verbose=True)
mapdl.finish()
mapdl.clear()
mapdl.prep7()
mapdl.k(1, 0, 0, 0)
mapdl.k(2, 1, 0, 0)
mapdl.k(3, 1, 1, 0)
mapdl.k(4, 0, 1, 0)
mapdl.l(1, 2)
mapdl.l(2, 3)
mapdl.l(3, 4)
mapdl.l(4, 1)
mapdl.al(1, 2, 3)
