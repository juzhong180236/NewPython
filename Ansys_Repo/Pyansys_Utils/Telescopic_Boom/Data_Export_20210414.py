from ansys.mapdl.core import launch_mapdl
import numpy as np

apdl = launch_mapdl()


def read_elements_data(_list, _path_write):
    for i, _name in enumerate(_list):
        with apdl.non_interactive:
            apdl.run(r"FINISH")
            apdl.run(r"/CLEAR")
            apdl.run(r"/NOPR")

            apdl.run(r"inner_cycle_times=1")
            apdl.run(r"point_quantity=4")

            apdl.run(r"*DIM,path_write,STRING,128,1")
            apdl.run(r"*DIM,path_read,STRING,128,1")
            apdl.run(r"*DIM,str_named_selection,STRING,128,point_quantity")

            apdl.run(r"path_write(1,1)='" + _path_write + r"\'")
            apdl.run(
                r"path_read(1,1)='D:\Alai\ansys_Alai\Telescopic_Boom\70_files\dp0\SYS-" + str(_name) + r"\MECH\file'")

            apdl.run(r"str_named_selection(1,1)='C_1'")
            apdl.run(r"str_named_selection(1,2)='C_2'")
            apdl.run(r"str_named_selection(1,3)='C_3'")
            apdl.run(r"str_named_selection(1,4)='C_4'")

            apdl.run(r"file_name_middle='_'")

            apdl.run(r"/POST1")
            apdl.run(r"/MKDIR,path_write(1,1)")
            apdl.run(r"/CWD,path_write(1,1)")

            apdl.run(r"FILE,path_read(1,1),'rst'")
            apdl.run(r"INRES,ALL")
            apdl.run(r"file_name_out=CHRVAL(" + str(i + 1) + r")")

            apdl.run(r"*DO,j,1,inner_cycle_times,1")

            apdl.run(r"SET,j")
            apdl.run(r"file_name=CHRVAL(j)")
            apdl.run(r"*CFOPEN,%file_name_out%%file_name_middle%%file_name%,txt")

            apdl.run(r"*DO,h,1,point_quantity,1")
            apdl.run(r"ESEL,S,ENAME,,187")
            apdl.run(r"CMSEL,S,str_named_selection(1,h)")
            apdl.run(r"NSLE,S,CORNER")
            apdl.run(r"*GET,ele_num_min,ELEM,,NUM,MIN")
            apdl.run(r"*GET,ele_count,ELEM,0,COUNT")
            apdl.run(r"*IF,h,NE,1,THEN")
            apdl.run(r"*VWRITE,'C'")
            apdl.run(r"(A1)")
            apdl.run(r"*ENDIF")
            apdl.run(r"*DO,i,1,ele_count,1")
            apdl.run(r"e_node_1=CHRVAL(NELEM(ele_num_min,1))")
            apdl.run(r"e_node_2=CHRVAL(NELEM(ele_num_min,2))")
            apdl.run(r"e_node_3=CHRVAL(NELEM(ele_num_min,3))")
            apdl.run(r"e_node_4=CHRVAL(NELEM(ele_num_min,4))")
            apdl.run(r"e_node_5=CHRVAL(NELEM(ele_num_min,5))")
            apdl.run(r"e_node_6=CHRVAL(NELEM(ele_num_min,6))")
            apdl.run(r"e_node_7=CHRVAL(NELEM(ele_num_min,7))")
            apdl.run(r"e_node_8=CHRVAL(NELEM(ele_num_min,8))")
            apdl.run(
                r"*VWRITE,CHRVAL(ele_num_min),e_node_1,e_node_2,e_node_3,e_node_4,e_node_5,e_node_6,e_node_7,e_node_8")
            apdl.run(r"(A9,A9,A9,A9,A9,A9,A9,A9,A9)")
            apdl.run(r"ele_num_min=ELNEXT(ele_num_min)")
            apdl.run(r"*ENDDO")
            apdl.run(r"*ENDDO")
            apdl.run(r"*CFCLOSE")
            apdl.run(r"*ENDDO")

            apdl.run(r"/GOPR")
            apdl.run(r"FINISH")
            apdl.run(r"/CLEAR")


def read_coordinate_data(_list, _path_write):
    for i, _name in enumerate(_list):
        with apdl.non_interactive:
            apdl.run(r"FINISH")
            apdl.run(r"/CLEAR")
            apdl.run(r"/NOPR")

            apdl.run(r"inner_cycle_times=1")
            apdl.run(r"point_quantity=4")

            apdl.run(r"*DIM,path_write,STRING,128,1")
            apdl.run(r"*DIM,path_read,STRING,128,1")
            apdl.run(r"*DIM,str_named_selection,STRING,128,point_quantity")

            apdl.run(r"path_write(1,1)='" + _path_write + r"\'")
            apdl.run(
                r"path_read(1,1)='D:\Alai\ansys_Alai\Telescopic_Boom\70_files\dp0\SYS-" + str(_name) + r"\MECH\file'")

            apdl.run(r"str_named_selection(1,1)='C_1'")
            apdl.run(r"str_named_selection(1,2)='C_2'")
            apdl.run(r"str_named_selection(1,3)='C_3'")
            apdl.run(r"str_named_selection(1,4)='C_4'")

            apdl.run(r"file_name_middle='_'")

            apdl.run(r"/POST1")
            apdl.run(r"/MKDIR,path_write(1,1)")
            apdl.run(r"/CWD,path_write(1,1)")

            apdl.run(r"FILE,path_read(1,1),'rst'")
            apdl.run(r"INRES,ALL")
            apdl.run(r"file_name_out=CHRVAL(" + str(i + 1) + r")")

            apdl.run(r"*DO,j,1,inner_cycle_times,1")

            apdl.run(r"SET,j")
            apdl.run(r"file_name=CHRVAL(j)")
            apdl.run(r"*CFOPEN,%file_name_out%%file_name_middle%%file_name%,txt")

            apdl.run(r"*DO,h,1,point_quantity,1")
            apdl.run(r"ESEL,S,ENAME,,187")
            apdl.run(r"CMSEL,S,str_named_selection(1,h)")
            apdl.run(r"NSLE,S,CORNER")
            apdl.run(r"*GET,node_num_min,NODE,,NUM,MIN")
            apdl.run(r"*GET,node_count,NODE,0,COUNT")
            apdl.run(r"*IF,h,NE,1,THEN")
            apdl.run(r"*VWRITE,'C'")
            apdl.run(r"(A1)")
            apdl.run(r"*ENDIF")
            apdl.run(r"*DO,i,1,node_count,1")
            apdl.run(r"n_coord_x = NX(node_num_min)")
            apdl.run(r"n_coord_y = NY(node_num_min)")
            apdl.run(r"n_coord_z = NZ(node_num_min)")
            apdl.run(r"*VWRITE,CHRVAL(node_num_min),n_coord_x,n_coord_y,n_coord_z")
            apdl.run(r"(A9,E16.8,E16.8,E16.8)")
            apdl.run(r"node_num_min=NDNEXT(node_num_min)")
            apdl.run(r"*ENDDO")
            apdl.run(r"*ENDDO")
            apdl.run(r"*CFCLOSE")
            apdl.run(r"*ENDDO")

            apdl.run(r"/GOPR")
            apdl.run(r"FINISH")
            apdl.run(r"/CLEAR")


def read_stresses_data(_list, _path_write):
    for i, _name in enumerate(_list):
        with apdl.non_interactive:
            apdl.run(r"FINISH")
            apdl.run(r"/CLEAR")
            apdl.run(r"/NOPR")

            apdl.run(r"inner_cycle_times=1")
            apdl.run(r"point_quantity=4")

            apdl.run(r"*DIM,path_write,STRING,128,1")
            apdl.run(r"*DIM,path_read,STRING,128,1")
            apdl.run(r"*DIM,str_named_selection,STRING,128,point_quantity")

            apdl.run(r"path_write(1,1)='" + _path_write + r"\'")
            apdl.run(
                r"path_read(1,1)='D:\Alai\ansys_Alai\Telescopic_Boom\70_files\dp0\SYS-" + str(_name) + r"\MECH\file'")

            apdl.run(r"str_named_selection(1,1)='C_1'")
            apdl.run(r"str_named_selection(1,2)='C_2'")
            apdl.run(r"str_named_selection(1,3)='C_3'")
            apdl.run(r"str_named_selection(1,4)='C_4'")

            apdl.run(r"file_name_middle='_'")

            apdl.run(r"/POST1")
            apdl.run(r"/MKDIR,path_write(1,1)")
            apdl.run(r"/CWD,path_write(1,1)")

            apdl.run(r"FILE,path_read(1,1),'rst'")
            apdl.run(r"INRES,ALL")
            apdl.run(r"file_name_out=CHRVAL(" + str(i + 1) + r")")

            apdl.run(r"*DO,j,1,inner_cycle_times,1")

            apdl.run(r"SET,j")
            apdl.run(r"file_name=CHRVAL(j)")
            apdl.run(r"*CFOPEN,%file_name_out%%file_name_middle%%file_name%,txt")

            apdl.run(r"*DO,h,1,point_quantity,1")
            apdl.run(r"ESEL,S,ENAME,,187")
            apdl.run(r"CMSEL,S,str_named_selection(1,h)")
            apdl.run(r"NSLE,S,CORNER")
            apdl.run(r"*GET,node_num_min,NODE,,NUM,MIN")
            apdl.run(r"*GET,node_count,NODE,0,COUNT")
            apdl.run(r"*IF,h,NE,1,THEN")
            apdl.run(r"*VWRITE,'C'")
            apdl.run(r"(A1)")
            apdl.run(r"*ENDIF")
            apdl.run(r"*DO,i,1,node_count,1")
            apdl.run(r"*GET,s_eqv,NODE,node_num_min,S,EQV")
            apdl.run(r"*VWRITE, CHRVAL(node_num_min), s_eqv")
            apdl.run(r"(A9,E16.8)")
            apdl.run(r"node_num_min=NDNEXT(node_num_min)")
            apdl.run(r"*ENDDO")
            apdl.run(r"*ENDDO")
            apdl.run(r"*CFCLOSE")
            apdl.run(r"*ENDDO")

            apdl.run(r"/GOPR")
            apdl.run(r"FINISH")
            apdl.run(r"/CLEAR")


def read_displacement_data(_list, _path_write):
    for i, _name in enumerate(_list):
        with apdl.non_interactive:
            apdl.run(r"FINISH")
            apdl.run(r"/CLEAR")
            apdl.run(r"/NOPR")

            apdl.run(r"inner_cycle_times=1")
            apdl.run(r"point_quantity=4")

            apdl.run(r"*DIM,path_write,STRING,128,1")
            apdl.run(r"*DIM,path_read,STRING,128,1")
            apdl.run(r"*DIM,str_named_selection,STRING,128,point_quantity")

            apdl.run(r"path_write(1,1)='" + _path_write + r"\'")
            apdl.run(
                r"path_read(1,1)='D:\Alai\ansys_Alai\Telescopic_Boom\70_files\dp0\SYS-" + str(_name) + r"\MECH\file'")

            apdl.run(r"str_named_selection(1,1)='C_1'")
            apdl.run(r"str_named_selection(1,2)='C_2'")
            apdl.run(r"str_named_selection(1,3)='C_3'")
            apdl.run(r"str_named_selection(1,4)='C_4'")

            apdl.run(r"file_name_middle='_'")

            apdl.run(r"/POST1")
            apdl.run(r"/MKDIR,path_write(1,1)")
            apdl.run(r"/CWD,path_write(1,1)")

            apdl.run(r"FILE,path_read(1,1),'rst'")
            apdl.run(r"INRES,ALL")
            apdl.run(r"file_name_out=CHRVAL(" + str(i + 1) + r")")

            apdl.run(r"*DO,j,1,inner_cycle_times,1")

            apdl.run(r"SET,j")
            apdl.run(r"file_name=CHRVAL(j)")
            apdl.run(r"*CFOPEN,%file_name_out%%file_name_middle%%file_name%,txt")

            apdl.run(r"*DO,h,1,point_quantity,1")
            apdl.run(r"ESEL,S,ENAME,,187")
            apdl.run(r"CMSEL,S,str_named_selection(1,h)")
            apdl.run(r"NSLE,S,CORNER")
            apdl.run(r"*GET,node_num_min,NODE,,NUM,MIN")
            apdl.run(r"*GET,node_count,NODE,0,COUNT")
            apdl.run(r"*IF,h,NE,1,THEN")
            apdl.run(r"*VWRITE,'C'")
            apdl.run(r"(A1)")
            apdl.run(r"*ENDIF")
            apdl.run(r"*DO,i,1,node_count,1")
            apdl.run(r"*GET,n_disp_sum,NODE,node_num_min,U,SUM")
            apdl.run(r"*VWRITE,CHRVAL(node_num_min),n_disp_sum")
            apdl.run(r"(A9,E16.8)")
            apdl.run(r"node_num_min=NDNEXT(node_num_min)")
            apdl.run(r"*ENDDO")
            apdl.run(r"*ENDDO")
            apdl.run(r"*CFCLOSE")
            apdl.run(r"*ENDDO")

            apdl.run(r"/GOPR")
            apdl.run(r"FINISH")
            apdl.run(r"/CLEAR")


rst_files_num = 16
_list = np.array([60]) + list(range(rst_files_num))
rst_file_path = ""
path_write_stresses = r"C:\Users\asus\Desktop\stresses"
path_write_displacement = r"C:\Users\asus\Desktop\displacement"

read_stresses_data(_list, path_write_stresses)
read_displacement_data(_list, path_write_displacement)
