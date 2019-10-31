import numpy as np
from openpyxl import load_workbook


def readExcel(path, sheet, row_index, row_num, column_num):
    ''' 读取Ecxel中的数据

    参数：
        path: Excel文档的绝对路径
        sheet：数据所属sheet的名称
        row_num: 数据的列数
        column: 数据的行数
    返回：
        返回一个tuple（元组），得到data_X和data_Y
    注意：
        data_Y[i - 1] = float(sheet.cell(row=i, column=5).value)，此处数据Y的位置在列5，所以column为5，可更改
    '''
    book = load_workbook(filename=path)  # 按照路径读取Excel
    sheet = book[sheet]  # 读取Excel中的指定sheet
    data_X = np.empty((row_num - row_index + 1, column_num))  # 用于存储数据的array，相较于np.ones只分配不初始化
    data_Y = np.empty(row_num - row_index + 1)
    for i in range(row_index, row_num + 1):
        for j in range(1, column_num + 1):
            data_X[i - row_index][j - 1] = float(sheet.cell(row=i, column=j).value)
            if j == 1:
                data_Y[i - row_index] = float(sheet.cell(row=i, column=5).value)
    return data_X, data_Y
