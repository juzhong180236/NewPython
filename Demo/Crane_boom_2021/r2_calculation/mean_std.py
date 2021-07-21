import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np


def read_excel(_path):
    excel_object = pd.read_excel(_path, sheet_name="page_1")
    nrows = excel_object.shape[0]
    ncols = excel_object.columns.size

    sum_mfs_rbf = 0
    for i in range(nrows):
        sum_mfs_rbf += excel_object.iloc[i, 1]
    sum_co_kriging = 0
    for i in range(nrows):
        sum_co_kriging += excel_object.iloc[i, 2]
    sum_lr_mfs = 0
    for i in range(nrows):
        sum_lr_mfs += excel_object.iloc[i, 3]
    sum_mfs_mls = 0
    for i in range(nrows):
        sum_mfs_mls += excel_object.iloc[i, 4]

    # print(sum_mfs_rbf / 18)
    # print(sum_co_kriging / 18)
    # print(sum_lr_mfs / 18)
    # print(sum_mfs_mls / 18)
    # print()
    return [sum_mfs_rbf / 18, sum_co_kriging / 18, sum_lr_mfs / 18, sum_mfs_mls / 18]


path_ = r'D:\Alai\paper_Alai\【1】期刊论文\【1】Journal of Mechanical Design\起重机臂架论文\提交过程\【2】第一次审回\仿真数据\r2\\'


def save_to_excel(_list_results_excel, file_name):
    pd_results_excel = pd.DataFrame(_list_results_excel)
    pd_results_excel.columns = ['MFS_RBF', 'Co_Kriging', 'LR_MFS', 'MFS_MLS']
    pd_results_excel.index = ['50', '100_2', '100_3', '100_6', '150_2', '150_3', '150_6', '200']
    writer = pd.ExcelWriter(path_ + file_name + '.xlsx')  # 创建名称为hhh的excel表格
    pd_results_excel.to_excel(writer, 'page_1',
                              float_format='%.3f')  # float_format 控制精度小数点后3位，将data_df写到hhh表格的第一页中。若多个文件，可以在page_2中写入
    writer.save()  #


path_prefix_displacement = r'D:\Alai\paper_Alai\【1】期刊论文\【1】Journal of Mechanical Design\起重机臂架论文\提交过程\【2】第一次审回\仿真数据\r2\displacement'
path_prefix_stress = r'D:\Alai\paper_Alai\【1】期刊论文\【1】Journal of Mechanical Design\起重机臂架论文\提交过程\【2】第一次审回\仿真数据\r2\stress'
# for i in ['50', '100', '150_0', '150_1', '150_2', '150_3', '150_4', '150_5', '200', '250']:
#     read_excel(path_prefix + r'\r2_' + i + '.xlsx')
list_results_displacement = []
list_results_stress = []
for i in ['100_6', '50', '100_2', '100_3', '150_6', '150_3', '150_2', '200']:
    list_results_displacement.append(read_excel(path_prefix_displacement + r'\r2_' + i + '.xlsx'))
    list_results_stress.append(read_excel(path_prefix_stress + r'\r2_' + i + '.xlsx'))
# save_to_excel(list_results_displacement, "r2_displacement")
# save_to_excel(list_results_stress, "r2_stress")
array_results_displacement = np.array(list_results_displacement).T
array_results_displacement[array_results_displacement < 0] = 0.5
array_results_stress = np.array(list_results_stress).T
array_results_stress[array_results_stress < 0] = 0.5


def draw(_array_results, picture_name):
    plt.figure(figsize=(12, 6.75))
    ax = plt.gca()
    x = ['0.5_3.5', '1_3(1)', '1_3(2)', '1_3(3)', '1.5_2.5(1)', '1.5_2.5(2)', '1.5_2.5(3)', '2_2']

    # plot_co_kriging1 = plt.plot(x, _array_results[1], label="Co_Kriging", linewidth=1.5,
    #                             marker='^',
    #                             markersize=10,
    #                             color='g',
    #                             clip_on=False)
    # plot_lr_mfs1 = plt.plot(x, _array_results[2], label="LR_MFS", linewidth=1.5,
    #                         marker='D',
    #                         markersize=10,
    #                         color='#ff7f0e',
    #                         clip_on=False)
    # plot_mfs_mls1 = plt.plot(x, _array_results[3], label="MFS_MLS", linewidth=1.5,
    #                          marker='o',
    #                          markersize=10,
    #                          color='#1f77b4',
    #                          clip_on=False)
    # plot_mfs_rbf1 = plt.plot(x, _array_results[0], label="MFS_RBF", linewidth=1.5,
    #                          marker='s',
    #                          markersize=10,
    #                          color='r',
    #                          clip_on=False)
    list_mean = []
    list_std = []
    for i in range(8):
        _mean = np.round(
            (_array_results[0][i] + _array_results[1][i] + _array_results[2][i] + _array_results[3][i]) / 4, 3)
        # family {‘serif’, ‘sans-serif’, ‘cursive’, ‘fantasy’, ‘monospace’}
        # styles=['normal','italic','oblique']
        # weights=['light','normal','medium','semibold','bold','heavy','black']
        _std = np.round(
            np.std([_array_results[0][i], _array_results[1][i], _array_results[2][i], _array_results[3][i]]), 3)
        ax.text(i - 0.05, _mean / 2, _mean, family='sans-serif', weight='bold', color='#ffffff', fontsize=15,
                rotation=90)
        ax.text(i - 0.22, _mean + _std + 0.01, _std, family='sans-serif', weight='bold', color='#000000', fontsize=15)
        list_std.append(_std)
        list_mean.append(_mean)
    print(list_mean)
    print(list_std)
    # elinewidth误差棒腹板粗细 工字梁误差棒翼缘板的宽度
    error_params = dict(elinewidth=3, ecolor='#ff7f0e', capsize=5)  # 设置误差标记参数
    plt.bar(x, list_mean, width=0.45, color='#1f77b4', yerr=list_std, error_kw=error_params,
            tick_label=['0.5_3.5', '1_3(1)', '1_3(2)', '1_3(3)', '1.5_2.5(1)', '1.5_2.5(2)', '1.5_2.5(3)', '2_2'])
    # plot_average = plt.plot(x, list_average, label="Mean value of $\mathrm{R}^2$", linewidth=1.5,
    #                         marker='v',
    #                         markersize=8,
    #                         linestyle='--',
    #                         color='b',
    #                         clip_on=False)
    #
    # _plot = plot_average
    # labs = [_p.get_label() for _p in _plot]
    # bbox_to_anchor=(x, y, 长, 宽),总图是1*1的 loc是bbox中落在xy位置的角点或中点
    # plt.legend(_plot, labs, bbox_to_anchor=(0, 0.1, 1, 0.2), borderaxespad=0, ncol=3, loc="lower center", fontsize=15)
    bounds = [[0, 7], [0, 1]]
    # plt.xlim(bounds[0][0], bounds[0][1])
    # plt.xlim(bounds[0][0], bounds[0][1])
    plt.ylim(bounds[1][0], bounds[1][1])
    # x_ticks = np.arange(0, bounds[0][1] + 6, 6)
    x_ticks = ['0.5_3.5', '1_3(1)', '1_3(2)', '1_3(3)', '1.5_2.5(1)', '1.5_2.5(2)', '1.5_2.5(3)', '2_2']
    y_ticks = np.linspace(bounds[1][0], bounds[1][1] + 0.2, 7, endpoint=True)
    plt.tick_params(labelsize=15)
    plt.yticks(y_ticks, weight='semibold')
    plt.xticks(x_ticks, weight='semibold', rotation=-30)
    # bottom, top = plt.ylim()
    # left, right = plt.xlim()
    # ax.spines['bottom'].set_position(('data', bottom))
    # ax.spines['left'].set_position(('data', left))
    ax.set_axisbelow(True)  # 网格线靠后
    plt.grid()
    plt.xlabel("Sampling strategy", fontsize=24, weight='semibold')
    plt.ylabel(r'$\mathrm{R}^2$', fontsize=24)

    # ax.text(3, 8, 'boxed italics text in data coords', style='italic')

    # plt.show()
    plt.savefig(path_ + picture_name + '.tif', bbox_inches='tight')


draw(array_results_displacement, 'mean_std_displacement')
draw(array_results_stress, 'mean_std_stress')
