class CoordinateData(object):
    def __init__(self, path_coord=None, ed=None, data_list=None):
        if path_coord is not None:
            self.path_coord = path_coord
        else:
            self.path_coord = None
        self.ed = ed
        self.data_list = data_list

    def surfaceCoord_To_List(self, whichAxis='xyz'):
        set_surface_ele = self.ed.surface_int_set()
        list_coords = []  # 获取该文件夹下面的节点初始的坐标数据
        if self.path_coord is not None:
            coordfile = open(self.path_coord + "NLIST.lis", 'rt')
            for everyline in coordfile:
                list_everyline = everyline.split()
                everyline_index = int(list_everyline[0])
                if everyline_index in set_surface_ele:  # 根据element_data中set_surfaceEle方法返回的信息，只需表面点的坐标
                    coord_x = float(list_everyline[1].strip())
                    coord_y = float(list_everyline[2].strip())
                    coord_z = float(list_everyline[3].strip())
                    if whichAxis == 'x':
                        list_coords.append(coord_x)  # x
                    elif whichAxis == 'y':
                        list_coords.append(coord_y)  # y
                    elif whichAxis == 'z':
                        list_coords.append(coord_z)  # z
                    else:
                        list_coords.extend([coord_x, coord_y, coord_z])  # xyz
            coordfile.close()
        if self.data_list is not None:
            pass
        return list_coords

    def allCoord_To_List(self, whichAxis='xyz'):
        list_coords = []  # 获取该文件夹下面的节点初始的坐标数据
        coordfile = open(self.path_coord + "NLIST.lis", 'rt')
        for everyline in coordfile:
            list_everyline = everyline.split()
            # everyline_index = int(everyline[0:9].strip())
            # coord_x = everyline[9:31].strip()
            # coord_y = everyline[31:53].strip()
            # coord_z = everyline[53:75].strip()
            coord_x = float(list_everyline[1].strip())
            coord_y = float(list_everyline[2].strip())
            coord_z = float(list_everyline[3].strip())
            if whichAxis == 'x':
                list_coords.append(coord_x)  # x
            elif whichAxis == 'y':
                list_coords.append(coord_y)  # y
            elif whichAxis == 'z':
                list_coords.append(coord_z)  # z
            else:
                list_coords.extend([coord_x, coord_y, coord_z])  # xyz
        coordfile.close()
        return list_coords
