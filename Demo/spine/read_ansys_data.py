from element_data import ElementData
from coordinate_data import CoordinateData
from displacement_data import DispalcementData
from stress_data import StressData
import text_file_create as tfc

part_type = 'spine'

# 读取路径@@@@@@@@@@@@@@@@@@@@@(读pre)
path_four_read = r"C:\Users\asus\Desktop\DT_Crane_v2.0\APP_models\\" + part_type + r"\\"

path_four_read_dopAndCoord = path_four_read + r'dopAndCoord\\'  # coord、dispalcement
path_four_read_ele = path_four_read + r'ele\\'  # ele
# path_four_read_ele = r'C:\Users\asus\Desktop\\'  # ele
path_four_read_equivalentStress = path_four_read + r'equivalent_stress\\'  # stress
path_four_write = r"C:\Users\asus\Desktop\DT_Crane_v2.0\APP_models\post\\"


# ele_data
def read_ed():
    ed = ElementData(path_four_read_ele, ['3D4_P'])
    print(len(ed.set_SurfaceEle()))
    txt_ed = ed.surfaceEle_Real_Sequence(path_four_read_dopAndCoord)
    # # txt_all = ','.join(map(str, ed.aa()))
    # tfc.text_Create(path_four_write, 'ele', txt_ed)
    # # tfc.text_Create(r"C:\Users\asus\Desktop\Demo_DT_Crane\APP_models\\" + path_switch + r"\mid\\", 'ele_all', txt_all)
    return ed


# tfc.text_Create(path_four_write, 'ele_ed', txt_ed)

# coord_data
def read_cd(ed):
    cd = CoordinateData(path_four_read_dopAndCoord, ed)

    cd_list = cd.surfaceCoord_To_List()
    tfc.text_Create(path_four_write, part_type + '_coord', ','.join(cd_list))
    return cd


# displacement_data
def read_dd(ed, cd):
    dd = DispalcementData(path_four_read_dopAndCoord, ed, cd)
    str_dopcoord, str_dopSum, str_Dcolor, str_D_StepandMin = dd.surface_DopCoords_DopSum_Dcolor()
    tfc.text_Create(r"C:\Users\asus\Desktop\DT_Crane_v1.0\APP_models\mid\\", 'dopCoords',
                    str_dopcoord)


def read_sd(ed):
    # stress_data
    sd = StressData(path_four_read_equivalentStress, ed)
    str_stress, str_Scolor, str_S_StepandMin = sd.surface_Stress_Scolor()
    # print(len(str_stress.split('\n')[0].split(',')))


ed_outer = read_ed()
cd_outer = read_cd(ed_outer)
# read_dd(ed_outer, cd_outer)
# read_sd(ed_outer)
