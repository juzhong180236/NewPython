# 【输入str】：将ELIST.lis文件中每一行以多个空格隔开的一行字符串作为输入
# 【输出list】：将ELIST.lis中一行的元素转为list
# 【功能】：去除每行数据中多余的空格，返回只有元素的list
def Text_PerLine_ToList(str_input):
    list_str = str_input.strip().split(" ")
    list_temp = []
    for i in range(len(list_str)):
        if list_str[i] != "":
            list_temp.append(list_str[i])
    return list_temp


# 【输入int,str】：ELIST.lis文件中是四面体节点输入4，六面体节点输入6，第二个参数为ELIST.lis的路径
# 【输出str】：返回以逗号隔开的可绘制模型表面的排列好的索引值字符串(string)
# 【功能】：对四面体或六面体的ELIST.lis进行简化，使其只有表面点的信息，极大减少数据量
def Str_SurfaceEle(geometry_faceNumber, path_input):
    eleFile = open(path_input, "rt")
    list_result = []
    for everyline in eleFile:
        if len(everyline) >= 78:
            list_temp = Text_PerLine_ToList(everyline)
            if len(list_temp) == 14:
                if geometry_faceNumber == 4:
                    if list_temp[1] == '1':
                        list_temp = list(map(int, list_temp))
                        # 所有的ele【前4位】排列为【四面体】的画图形式，得到这些值并存在list_result中
                        list_result.extend([list_temp[6] - 1, list_temp[7] - 1, list_temp[8] - 1,
                                            list_temp[7] - 1, list_temp[8] - 1, list_temp[9] - 1,
                                            list_temp[6] - 1, list_temp[8] - 1, list_temp[9] - 1,
                                            list_temp[6] - 1, list_temp[7] - 1, list_temp[9] - 1])
                elif geometry_faceNumber == 6:
                    if list_temp[1] == '1':
                        list_temp = list(map(int, list_temp))
                        # 所有的ele【前8位】排列为【六面体】的画图形式，得到这些值并存在list_result中
                        list_result.extend(
                            [list_temp[6] - 1, list_temp[7] - 1, list_temp[8] - 1,
                             list_temp[6] - 1, list_temp[8] - 1, list_temp[9] - 1,
                             list_temp[10] - 1, list_temp[11] - 1, list_temp[12] - 1,
                             list_temp[10] - 1, list_temp[12] - 1, list_temp[13] - 1,
                             list_temp[6] - 1, list_temp[9] - 1, list_temp[13] - 1,
                             list_temp[6] - 1, list_temp[10] - 1, list_temp[13] - 1,
                             list_temp[7] - 1, list_temp[11] - 1, list_temp[12] - 1,
                             list_temp[7] - 1, list_temp[8] - 1, list_temp[12] - 1,
                             list_temp[6] - 1, list_temp[10] - 1, list_temp[11] - 1,
                             list_temp[6] - 1, list_temp[7] - 1, list_temp[11] - 1,
                             list_temp[8] - 1, list_temp[9] - 1, list_temp[13] - 1,
                             list_temp[8] - 1, list_temp[12] - 1, list_temp[13] - 1])
    result = er.str_Remove_SameEle(list_result)
    eleFile.close()
    return result
