from element_data import ElementData
from coordinate_data import CoordinateData
from displacement_data import DispalcementData
from stress_data import StressData
from surface_data_process import SurfaceData
import text_file_create as tfc

path_1 = r"C:\Users\asus\Desktop\ansys_0518\excavator\gear_pre\ele\\"
path_2 = r"C:\Users\asus\Desktop\ansys_0518\excavator\gear_pre\dopAndCoord\\"
path_3 = r"C:\Users\asus\Desktop\ansys_0518\excavator\gear_pre\equivalent_stress\\"
path_read = r"C:\Users\asus\Desktop\ansys_0518\excavator\\"
path_save = r"C:\Users\asus\Desktop\ansys_0518\excavator\\"
ed = ElementData(path_1, geometry_type='3D4_L')
# # print(len(ed.allEle_Sequence()))
# # print(ed.surfaceEle_Sequence())
# cd = CoordinateData(path_2, ed)
# # print(cd.surfaceCoord_To_List())
# dd = DispalcementData(path_2, ed, cd)
# # print(dd.surface_DopCoords_DopSum_Dcolor())
# sd = StressData(path_3, ed)
# sd.surface_Stress_Scolor_Bysorted()
sfd = SurfaceData(path_read, '3D4_L')
ele = sfd.get_Ele_Data()
coordinate = sfd.get_Coord_Data()
# d_color = sfd.get_Dcolor()
# s_color = sfd.get_Scolor()

tfc.text_Create(path_save, "ele", ele)
tfc.text_Create(path_save, "coords", coordinate)
# tfc.text_Create(path_save, "d_color", d_color)
# tfc.text_Create(path_save, "s_color", s_color)
