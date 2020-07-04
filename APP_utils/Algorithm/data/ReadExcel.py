import numpy as np
from openpyxl import load_workbook


def readExcel(path=None, sheet=None, row_index=3, column_index=4, row_num=165, column_num=8, y_column=1):
    """

    :param path:Excel文档的绝对路径
    :param sheet:数据所属sheet的名称
    :param row_index: 读取数据的开始行数
    :param column_index: 读取数据的开始列数
    :param row_num:数据的行数
    :param column_num:数据的列数
    :param y_column:

    :return:
    """
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
    data_X = np.empty((column_num, row_num))  # 用于存储数据的array，相较于np.ones只分配不初始化
    data_Y = np.empty(row_num)
    for j in range(column_index, column_index + column_num):
        for i in range(row_index, row_index + row_num):
            data_X[j - column_index][i - row_index] = np.abs(float(sheet.cell(row=i, column=j).value))
            if j == column_index:
                data_Y[i - row_index] = float(sheet.cell(row=i, column=y_column).value)
    return data_X, data_Y
