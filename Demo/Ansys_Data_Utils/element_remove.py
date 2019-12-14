def str_Remove_SameEle(list_input):
    """
    【输入list】：经过排列后，能画出四面体或六面体的索引的列表（list）
    【输出str】：删除模型除表面以外、内部点的索引，返回以【逗号】隔开，可绘制模型【表面】的排列好的索引值字符串(string)
    【功能】：每三个相连索引为一组，所有只出现一次（模型表面）的索引组所构成的字符串
    :param list_input:
    :return:
    """
    # 将索引信息转为int类型后，每3个一组（称为【单面索引组】）进行排序，得到【顺序单面索引组】，再转为字符串，放入list_sort中。
    # 例如953转为'3,5,9'
    list_sort = []
    for i in range(0, len(list_input), 3):
        list_temp = [int(list_input[i]), int(list_input[i + 1]), int(list_input[i + 2])]
        list_temp.sort(key=lambda x: x)
        list_sort.append(str(list_temp[0]) + ',' + str(list_temp[1]) + ',' + str(list_temp[2]))
    # 直接使用set对相同的顺序单面索引组只保留一个，即对画多次的表面只画一次
    # 这一步使内部面片不用画两次了，但是还是会画一次
    set_sort = set(list_sort)
    # 每个【顺序单面索引组】的初始出现次数设置为0，使用dict类型保存
    # 例如{'3,5,8':0,'4,5,8':0,...}
    dict_sort = {}
    for ele in list_sort:
        dict_sort[ele] = 0
    # 利用set_sort对list_sort进行检测，list_sort中出现多次的【顺序单面索引组】就会被识别。
    for ele in list_sort:
        if ele in set_sort:
            dict_sort[ele] += 1  # 如果检测到【顺序单面索引组】一次，就加1
    # 最终得到只出现一次的【顺序单面索引组】组成的dict_sort，将它的key保存在list_sort中，
    list_sort = []
    for key, value in dict_sort.items():
        if value == 1:
            list_sort.append(key)
    # 返回逗号隔开的索引值字符串
    return ','.join(list_sort)
