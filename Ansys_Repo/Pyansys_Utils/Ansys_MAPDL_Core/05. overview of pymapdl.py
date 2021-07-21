'''
2021.07.18
pymapdl的概况
'''
from ansys.mapdl.core import launch_mapdl

exec_loc = r'C:\Program Files\ANSYS Inc\v211\ansys\bin\winx64\ANSYS211.exe'
mapdl = launch_mapdl(exec_loc, nproc=4)
mapdl.mute = True  # 会阻断apdl向python传输的信息，甚至不会报错

# ESEL, S, TYPE, , 1
mapdl.esel('s', 'type', '', 1)
# or
mapdl.esel('s', 'type', vmin=1)

# 有时候用run反而更方便
mapdl.run('/SOLU')
mapdl.solve()

# non-interactively
with mapdl.non_interactive:
    mapdl.run("*VWRITE,LABEL(1),VALUE(1,1),VALUE(1,2),VALUE(1,3)")
    mapdl.run("(1X,A8,'   ',F10.1,'  ',F10.1,'   ',1F5.3)")

# If you have an existing input file with a macro,
# it can be converted using the convert_script function and setting macros_as_functions=True:
# import ansys.mapdl.core as pymapdl
# pymapdl.convert_script(apdl_inputfile, pyscript, macros_as_functions=True)

# 运行一大段apdl
cmd = ''' 这里是一大段apdl '''
resp = mapdl.run_multiline(cmd)
# 或者直接运行ds.dat文件
resp1 = mapdl.input("ds.dat")

# 使用*IF、*DO、*DOWHILE时，要不用non-interactive模式，要不就用python的if实现
# MAPDL parameters can be obtained using load_parameters
# mapdl.load_parameters()

# Errors are handled pythonically. For example:
try:
    mapdl.solve()
except:
    # do something else with MAPDL
    pass
# 在APDL中被忽略的命令是以警告的方式告知，而MAPDL中则是以错误提醒。
# 使用如下的代码可以在MAPDL中不弹出因忽略命令而导致的错误。
mapdl.allow_ignore = True
mapdl.k()  # error ignored

# 以下代码可以将mapdl运行的语句以APDL的方式记录在log中。
ansys = launch_mapdl(log_apdl='apdl.log')

# open up the gui # it resumes where you left off
mapdl.open_gui()

# Exit MAPDL
mapdl.exit()

# Chaining Commands in MAPDL
import numpy as np

xloc = np.linspace(0, 1, 1000)
for x in xloc:
    mapdl.k(x=x)

xloc1 = np.linspace(0, 1, 1000)
with mapdl.chain_commands:
    for x in xloc1:
        mapdl.k(x=x)

# 数组传递，将numpy的ndarray或python的list传递到MAPDL
# It uses *VREAD behind the scenes and
# will be replaced with a faster interface in the future.
import numpy as np

mapdl = launch_mapdl()
arr = np.random.random((5, 3))
mapdl.parameters['MYARR'] = arr
# 可以通过这句话来确定是否传递成功
array_from_mapdl = mapdl.parameters['MYARR']

# Downloading a Remote MAPDL File
remote_files = mapdl.list_files()
# ensure the result file is one of the remote files
assert 'file.rst' in remote_files
# download the remote result file
mapdl.download('file.rst')
# Uploading a Local MAPDL File
# upload a local file
mapdl.upload('sample.db')
# ensure the uploaded file is one of the remote files
remote_files = mapdl.list_files()
assert 'sample.db' in remote_files