import os
import sys
import pyansys as py
import numpy as np
from pyansys import examples


def create_dir_in_current(dirname):
    path = sys.path[0] + '\\' + dirname
    if os.path.exists(path):
        print(path + ' 目录已存在')
        return path
    else:
        os.mkdir(path)
        print(path + ' 创建成功')
        return path


rst_file_path = r'D:\Alai\ansys_Alai\Crane\Crane_Parts_v2.0\truss\20191220_files\dp0\SYS-3\MECH\file'
save_file_path = r'C:\Users\asus\Desktop\History\History_ansys\ANSYS WorkDir\equivalent_stress\\'
path = create_dir_in_current('test_first')
ansys = py.Mapdl(run_location=path, nproc=6, loglevel='INFO')
# loglevel（str ，可选）–设置将哪些消息打印到控制台。
# 默认的“INFO”打印出所有ANSYS消息
# “ WARNING”仅打印包含ANSYS警告的消息
# “ ERROR”仅打印错误消息。

# ansys.run('/PREP7')  # 进入前处理器
ansys.run('FINISH')  # 退出当前处理器
ansys.run('/CLEAR')  # 清除当前ANSYS数据库文件，并开始一个新的启动
# ansys.run('/ALLSEL,ALL')  # 选择所有的实体

# ansys.run('/TITLE,Result From File xx')#
ansys.run('*DIM,rst_path_,STRING,128,2')  # 定义数组rst_path_存储结果文件路径字符串，最大长度为128个字符

# ansys.run('/INQUIRE,path_,LOGIN')  # 默认工作目录名
# ansys.run('/INQUIRE,path_,DOCU')  # 返回ANSYS的文件目录的路径名
# ansys.run('/INQUIRE,path_,APDL')  # 返回ANSYS的apdl路径名
# ansys.run('/INQUIRE,path_,PROG')  # 返回ANSYS的apdl路径名
# ansys.run('/INQUIRE,path_,JOBNAME')  # 返回当前工作文件名
# ansys.run('/INQUIRE,path_,RSTDIR')  # 返回结果目录
# ansys.run('/INQUIRE,path_,RSTFILE')  # 返回结果文件名
# ansys.run('/INQUIRE,path_,RSTEXT')  # 返回结果扩展名
ansys.run('*STATUS,PRM_')
ansys.run("rst_path_(1,1)='" + rst_file_path + "'")  # 将结果路径字符串赋值给rst_path_数组的第一个元素
ansys.run("rst_path_(1,2)='" + save_file_path + "'")  # 将结果路径字符串赋值给rst_path_数组的第一个元素
# ansys.run("rst_path_(1)='" + rst_file_path + "'")  # 将结果路径字符串赋值给rst_path_数组的第一个元素
ansys.run('/POST1')  # 进入后处理器
ansys.run("/MKDIR,rst_path_(1,2)")
ansys.run("/CWD,rst_path_(1,2)")
ansys.run("FILE,rst_path_(1,1),RST")  # 指定读入ansys中的结果文，FILE
ansys.run("INRES,ALL")  # 从读入的结果文件中读出指定类型的数据，INRES
with ansys.non_interactive:
    ansys.run('*DO,j,1,1,1')
    ansys.run("SET,j")  # 从结果文件中读出所指定的数据集
    ansys.run("PRITER")  # 列表出结果的汇总数据
    # ansys.run("PRNSOL,U,X")  # 列表出结果的汇总数据
    # ansys.run('*CREATE,temp')
    ansys.run('file_name=CHRVAL(j)')
    ansys.run('*CFOPEN,%file_name%,txt')
    ansys.run('ALLS,ALL')
    ansys.run('*GET,nmax,NODE,,NUM,MAX')
    ansys.run('*GET,nmin,NODE,,NUM,MIN')
    ansys.run('*DO,i,nmin,nmax,1')
    ansys.run('n_coord_x = UX(i)+UX(i)')
    ansys.run('n_coord_y = UY(i)')
    ansys.run('n_coord_z = UZ(i)')
    ansys.run('*VWRITE,CHRVAL(i),n_coord_x,n_coord_y,n_coord_z')
    ansys.run("(A6,F20.6,F20.6,F20.6)")
    ansys.run('*ENDDO')
    ansys.run('*CFCLOSE')
    ansys.run('*ENDDO')
# ansys.run('*/INPUT,temp')
# ansys.run('*fini')

# ansys.run('*STATUS')
# ansys.run('*STATUS,PRM_')

# ansys.run('/EXIT,ALL')  # 退出ANSYS

"""字符串、数值"""
# CHRVAL(dp) 将dp表示的双精度数值转化为一个字符串（最多为8个字符）
# CHROCT(dp) 将dp表示的整数值转化为一个字符串（最多为8个字符）
# VALCHR(ab) 将ab表示的字符串转化为一个十进制数
"""节点"""
# NDNEXT(N) #节点编号大于N的下一个被选节点
# NX(N) 节点N在激活坐标系统中的X坐标值 UX(N) 节点N的UX值 ROTX(N) 节点N的ROTX
# NY(N) 节点N在激活坐标系统中的Y坐标值 UY(N) 节点N的UY值 ROTY(N) 节点N的ROTY
# NZ(N) 节点N在激活坐标系统中的Z坐标值 UZ(N) 节点N的UZ值 ROTZ(N) 节点N的ROTZ
# PRES(N) 节点N处的压力值
# VX(N) VY(N) VZ(N) 流体速度VX,VY,VZ
# NODE(X,Y,Z) 被选节点中最靠近X,Y,Z位置的节点编号

"""单元"""
# ELNEXT(E) #单元编号大于E的下一个被选单元

"""关键点"""
# KX(N) 关键点N在激活坐标系统中的X坐标值
# KY(N) 关键点N在激活坐标系统中的Y坐标值
# KZ(N) 关键点N在激活坐标系统中的Z坐标值
# KP(X,Y,Z) 被选节点中最靠近X,Y,Z位置的关键点编号

"""字符格式"""
# A9
# F16.8
# E16.8
# D16.8
# 2X
