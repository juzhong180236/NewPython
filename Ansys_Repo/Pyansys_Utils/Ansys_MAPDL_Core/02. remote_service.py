'''
2021.07.18
远程访问，可能需要服务器许可证。
'''
from ansys.mapdl.core import Mapdl

mapdl = Mapdl()  # listening 0.0.0.0:50052
# or
# mapdl1 = Mapdl('192.168.0.1', port=50052)
print(mapdl)
