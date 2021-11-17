from ansys.mapdl.core import launch_mapdl

apdl = launch_mapdl()
for i in range(1, 17):
    with apdl.non_interactive:
        apdl.run(r"FINISH")
        apdl.run(r"/CLEAR")
        apdl.run(r"/NOPR")

        apdl.run(r"outter_cycle_times=1")
        apdl.run(r"inner_cycle_times=1")
        apdl.run(r"point_quantity=4")

        apdl.run(r"*DIM,path_write,STRING,128,1")
        apdl.run(r"*DIM,path_read,STRING,128,outter_cycle_times")
        apdl.run(r"*DIM,str_named_selection,STRING,128,point_quantity")

        apdl.run(r"path_write(1,1)='C:\Users\asus\Desktop\coordinates_1\'")

        apdl.run(r"path_read(1,1)='D:\Alai\ansys_Alai\Telescopic_Boom\70_files\dp0\SYS-" + str(59 + i) + r"\MECH\file'")
        # apdl.run(r"path_read(1,2)='D:\Alai\ansys_Alai\Telescopic_Boom\70_files\dp0\SYS-61\MECH\file'")
        # apdl.run(r"path_read(1,3)='D:\Alai\ansys_Alai\Telescopic_Boom\70_files\dp0\SYS-62\MECH\file'")

        apdl.run(r"str_named_selection(1,1)='C_1'")
        apdl.run(r"str_named_selection(1,2)='C_2'")
        apdl.run(r"str_named_selection(1,3)='C_3'")
        apdl.run(r"str_named_selection(1,4)='C_4'")

        apdl.run(r"file_name_middle='_'")

        apdl.run(r"/POST1")
        apdl.run(r"/MKDIR,path_write(1,1)")
        apdl.run(r"/CWD,path_write(1,1)")

        apdl.run(r"*DO,s,1,outter_cycle_times,1")
        apdl.run(r"FILE,path_read(1,s),'rst'")
        apdl.run(r"INRES,ALL")
        apdl.run(r"file_name_out=CHRVAL(" + str(i) + r")")
        # apdl.run(r"SAVE,path_db(1,1),'db',,ALL")

        apdl.run(r"*DO,j,1,inner_cycle_times,1")
        apdl.run(r"SET,j")
        apdl.run(r"*IF,s,EQ,1,AND,j,EQ,1,THEN")
        apdl.run(r"*DO,n,1,2,1")
        apdl.run(r"*IF,n,EQ,1,THEN")
        apdl.run(r"file_name=CHRVAL(0)")
        apdl.run(r"*CFOPEN,%file_name%,txt")
        apdl.run(r"*ELSE")
        apdl.run(r"file_name=CHRVAL(j)")
        apdl.run(r"*CFOPEN,%file_name_out%%file_name_middle%%file_name%,txt")
        apdl.run(r"*ENDIF")
        apdl.run(r"*DO,h,1,point_quantity,1")
        apdl.run(r" ESEL,S,ENAME,,187")
        apdl.run(r"CMSEL,S,str_named_selection(1,h)")
        apdl.run(r" NSLE,S,CORNER")
        apdl.run(r"*GET,node_num_min,NODE,,NUM,MIN")
        apdl.run(r"*GET,node_num_max,NODE,,NUM,MAX")
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
        apdl.run(r"*ENDDO")
        apdl.run(r"*ELSE")
        apdl.run(r"file_name=CHRVAL(j)")
        apdl.run(r"*CFOPEN,%file_name_out%%file_name_middle%%file_name%,txt")
        apdl.run(r"*DO,h,1,point_quantity,1")
        apdl.run(r"ESEL,S,ENAME,,187")
        apdl.run(r"CMSEL,S,str_named_selection(1,h)")
        apdl.run(r"NSLE, S, CORNER         ")
        apdl.run(r"*GET,node_num_min,NODE,,NUM,MIN")
        apdl.run(r"*GET,node_num_max,NODE,,NUM,MAX")
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
        apdl.run(r"*ENDIF")
        apdl.run(r"*CFCLOSE")
        apdl.run(r"RESET")
        apdl.run(r"*ENDDO")
        apdl.run(r"*ENDDO")
        apdl.run(r"/GOPR")
        apdl.run(r"FINISH")
        apdl.run(r"/CLEAR")
        apdl.run(r"/DELETE,file,page")
        apdl.run(r"/DELETE,RPCRequestTmp,out")
        apdl.run(r"/DELETE,CHRVAL(0),txt")