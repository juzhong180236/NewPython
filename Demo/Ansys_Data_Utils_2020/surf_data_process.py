from ele_data import ElementData
from coords_data import CoordinateData
from disp_data import DispalcementData
from stre_data import StressData


class SurfaceData(object):
    def __init__(self, path_pre=None, geometry_type=None):
        self.path_pre = path_pre
        self.geometry_type = geometry_type
        self.ed = None
        self.cd = None
        pass

    def get_Ele_Data(self):
        """
        :return: 返回可与Three.js机制相结合的表面各节点的索引值数据
        """
        self.ed = ElementData(self.path_pre + '/ele/', self.geometry_type)
        return self.ed.surfaceEle_Real_Sequence(self.path_pre + '/dopAndCoord/')

    def get_Coord_Data(self, whichAxis='xyz'):
        """
        :return:返回表面各节点的初始坐标数据
        """
        if not self.ed:
            print('ElementData对象为空，先执行AnsysSurfaceData对象的get_Ele_Data方法！')
            return
        self.cd = CoordinateData(self.path_pre + '/dopAndCoord/', self.ed)
        return ','.join(self.cd.surfaceCoord_To_List(whichAxis))

    def get_DopCoord_DopSum_DStepandMin(self):
        """
        :return:返回表面各节点加位移后的坐标数据、和位移数据（最后一行是分为n（9）段的Step）、和位移分为n（21）段的Step和最小值
        """
        if not self.ed:
            print('ElementData对象为空，先执行AnsysSurfaceData对象的get_Ele_Data方法！')
            return
        if not self.cd:
            print('CoordinateData对象为空，先执行AnsysSurfaceData对象的get_Coord_Data方法！')
            return
        dd = DispalcementData(self.path_pre + '/dopAndCoord/', self.ed, self.cd)
        str_dopcoord, str_dopSum, str_Dcolor, str_D_StepandMin = dd.surface_DopCoords_DopSum_Dcolor()
        return str_dopcoord, str_dopSum, str_D_StepandMin

    def get_Displacement_DopSum_Dcolor(self):
        """
        :return:返回表面各节点位移数据（最后一行是分为n（9）段的Step）、和位移分为n（21）段的Step和最小值
        """
        if not self.ed:
            print('ElementData对象为空，先执行AnsysSurfaceData对象的get_Ele_Data方法！')
            return
        if not self.cd:
            print('CoordinateData对象为空，先执行AnsysSurfaceData对象的get_Coord_Data方法！')
            return
        dd = DispalcementData(self.path_pre + '/dopAndCoord/', self.ed, self.cd)
        str_displacement, str_dopSum, str_Dcolor, str_D_StepandMin = dd.surface_Displacement_DopSum_Dcolor()
        return str_displacement, str_dopSum, str_D_StepandMin

    def get_Displacement_DopSum_Dcolor_Bysorted(self):
        """
        :return:返回表面各节点位移数据（最后一行是分为n（9）段的Step）、和位移分为n（21）段的Step和最小值
        """
        if not self.ed:
            print('ElementData对象为空，先执行AnsysSurfaceData对象的get_Ele_Data方法！')
            return
        if not self.cd:
            print('CoordinateData对象为空，先执行AnsysSurfaceData对象的get_Coord_Data方法！')
            return
        dd = DispalcementData(self.path_pre + '/dopAndCoord/', self.ed, self.cd)
        str_displacement, str_dopSum, str_Dcolor, str_D_StepandMin = dd.surface_Displacement_DopSum_Dcolor_Bysorted()
        return str_displacement, str_dopSum, str_D_StepandMin

    def get_Dcolor(self):
        """
        :return:返回表面各节点位移数据对应的颜色数据
        """
        if not self.ed:
            print('ElementData对象为空，先执行AnsysSurfaceData对象的get_Ele_Data方法！')
            return
        if not self.cd:
            print('CoordinateData对象为空，先执行AnsysSurfaceData对象的get_Coord_Data方法！')
            return
        dd = DispalcementData(self.path_pre + '/dopAndCoord/', self.ed, self.cd)
        str_dopcoord, str_dopSum, str_Dcolor, str_D_StepandMin = dd.surface_DopCoords_DopSum_Dcolor()
        return str_Dcolor

    def get_Stress_SStepandMin(self):
        """
        :return:返回表面各节点应力数据（最后一行是分为n（9）段的Step）、应力分为n（21）段的Step和最小值
        """
        if not self.ed:
            print('ElementData对象为空，先执行AnsysSurfaceData对象的get_Ele_Data方法！')
            return
        sd = StressData(self.path_pre + '/equivalent_stress/', self.ed)
        str_stress, str_Scolor, str_S_StepandMin = sd.surface_Stress_Scolor()
        return str_stress, str_S_StepandMin

    def get_Stress_SStepandMin_Bysorted(self):
        """
        :return:返回表面各节点应力数据（最后一行是分为n（9）段的Step）、应力分为n（21）段的Step和最小值
        """
        if not self.ed:
            print('ElementData对象为空，先执行AnsysSurfaceData对象的get_Ele_Data方法！')
            return
        sd = StressData(self.path_pre + '/equivalent_stress/', self.ed)
        str_stress, str_Scolor, str_S_StepandMin = sd.surface_Stress_Scolor_Bysorted()
        return str_stress, str_S_StepandMin
    def get_Scolor(self):
        """
        :return:返回表面各节点应力数据对应的颜色数据
        """
        if not self.ed:
            print('ElementData对象为空，先执行AnsysSurfaceData对象的get_Ele_Data方法！')
            return
        sd = StressData(self.path_pre + '/equivalent_stress/', self.ed)
        str_stress, str_Scolor, str_S_StepandMin = sd.surface_Stress_Scolor()
        return str_Scolor
