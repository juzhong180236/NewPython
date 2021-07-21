from ansys.mapdl.core import launch_mapdl
import numpy as np

apdl = launch_mapdl()


def read_stresses_data(_list, _path_write):
    # for i, _name in enumerate(_list):
    with apdl.non_interactive:
        apdl.run(r"FINISH")
        apdl.run(r"/CLEAR")
        apdl.run(r"/NOPR")

        apdl.run(r"inner_cycle_times=14")

        apdl.run(r"*DIM,path_write,STRING,128,1")
        apdl.run(r"*DIM,path_read,STRING,128,1")

        apdl.run(r"path_write(1,1)='" + _path_write + r"\'")
        apdl.run(
            r"path_read(1,1)='D:\Alai\ansys_Alai\Crane\Crane_Parts_v2.0\truss_low_fidelity_20210629_150\20191220_files\dp0\SYS-3\MECH\file'")
        apdl.run(r"file_name_middle='_'")

        apdl.run(r"/POST1")
        apdl.run(r"/MKDIR,path_write(1,1)")
        apdl.run(r"/CWD,path_write(1,1)")

        apdl.run(r"FILE,path_read(1,1),'rst'")
        apdl.run(r"INRES,ALL")
        apdl.run(r"file_name_out=CHRVAL(1)")

        apdl.run(r"*DO,j,1,inner_cycle_times,1")

        apdl.run(r"SET,j")
        apdl.run(r"file_name=CHRVAL(j)")
        apdl.run(r"*CFOPEN,%file_name_out%%file_name_middle%%file_name%,txt")

        apdl.run(r"ESEL,S,ENAME,,188")
        apdl.run(r"*GET,e_count,ELEM,0,COUNT")
        apdl.run(r"*GET,e_current,ELEM,,NUM,MIN")

        apdl.run(r"*DO,i,1,e_count,1")
        apdl.run(r"*GET,sercstress,SECR,e_current,S,EQV,MAX")
        apdl.run(r"*VWRITE,CHRVAL(e_current),sercstress")
        apdl.run(r"(A9,E16.8)")
        apdl.run(r"e_current=ELNEXT(e_current)")
        apdl.run(r"*ENDDO")
        apdl.run(r"*ENDDO")
        apdl.run(r"*CFCLOSE")

        apdl.run(r"/GOPR")
        apdl.run(r"FINISH")
        apdl.run(r"/CLEAR")


rst_files_num = 1
_list = np.array([3]) + list(range(rst_files_num))

save_folder_name = "200"

path_read = r"D:\Alai\ansys_Alai\Crane\Crane_Parts_v2.0\truss_low_fidelity_20210629_150\20191220_files\dp0"
path_write_elements = r"C:\Users\asus\Desktop\\" + save_folder_name + r"\elements"
path_write_coordinates = r"C:\Users\asus\Desktop\\" + save_folder_name + r"\coordinates"
path_write_stresses = r"C:\Users\asus\Desktop\\" + save_folder_name + r"\stresses"
path_write_displacement = r"C:\Users\asus\Desktop\\" + save_folder_name + r"\displacement"

# read_elements_data(_list, path_write_elements)
# read_coordinates_data(_list, path_write_coordinates)
read_stresses_data(_list, path_write_stresses)
# read_displacement_data(_list, path_write_displacement)
