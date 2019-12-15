from element_data import ElementData
from coordinate_data import CoordinateData
from displacement_data import DispalcementData
import text_file_create as tfc

path_switch = 'pulley'
# 读取路径@@@@@@@@@@@@@@@@@@@@@(读pre)
path_four_read = r"C:\Users\asus\Desktop\Demo_DT_Crane\APP_models\\" + path_switch + r"\pre\\"

path_four_read_dopAndCoord = path_four_read + r'dopAndCoord\\'  # coord、dispalcement
path_four_read_ele = path_four_read + r'ele\\'  # ele
path_four_read_equivalentStress = path_four_read + r'equivalent_stress\\'  # stress
path_four_write = r"C:\Users\asus\Desktop\Demo_DT_Crane\APP_models\\" + path_switch + r"\mid\\"

# ele_data
ed = ElementData(path_four_read_ele, ['3D4'])
txt_ed = ed.surfaceEle_Real_Sequence(path_four_read_dopAndCoord)
tfc.text_Create(path_four_write, 'ele_ed', txt_ed)
# coord_data
cd = CoordinateData(path_four_read_dopAndCoord, ed)
# print(len(cd.surfaceCoord_To_List()))
# displacement_data
dd = DispalcementData(path_four_read_dopAndCoord, ed, cd)
str_dopcoord, str_dopSum, str_Dcolor, str_DStepandMin = dd.surface_DopCoords_DopSum_Dcolor()
print(len(str_dopcoord.split('\n')[1]))
# tfc.text_Create(path_four_write, 'dopcoord_dd', str_dopcoord)

# tfc.text_Create(path_four_write, 'coord_xyz', txt_ed)

# tfc.text_Create(path_four_save, 'elee', txt)
# print(ed.allEle_Sequence(path_four_read, ['3D4']))

# eleFile = open(path_four_read, "rt")
# txt = eleFile.read()
# print(len(txt.split(',')))
# eleFile.close()
