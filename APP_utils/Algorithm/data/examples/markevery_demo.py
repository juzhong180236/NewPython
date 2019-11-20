import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# 使用的backend，
plt.style.use('dark_background')
plt.style.use('ggplot')
# To list all available styles, use:
print(plt.style.available)
# To display where the currently active matplotlibrc file was loaded from, one can do the following:
print(matplotlib.matplotlib_fname())
import matplotlib.gridspec as gridspec

# define a list of markevery cases to plot
cases = [None,  # 数组x所有点全部画出来
         10,  # 从索引0开始，索引每增加10画一个
         (198, 1),  # 从数组x索引198开始，索引每增加1画一个
         [16, 24, 199],  # 根据数组x的索引，画索引为16、24、199的点
         [0, -1],  # 根据数组x的索引，画索引0、-1的点
         slice(0, 199, 99),  # 根据数组x的索引，从0开始，到198结束（不包括199），增量为99
         0.1,
         0.3,
         1.3,
         (0.0, 0.1),
         (0.45, 0.1)]

# define the figure size and grid layout properties
figsize = (10, 8)
cols = 3
rows = len(cases) // cols + 1
# define the data for cartesian plots
delta = 0.11
x = np.linspace(0, 10 - 2 * delta, 200) + delta
# print(len(x))
y = np.sin(x) + 1.0 + delta


# 去除因为plt.subplots多画出来的axs
def trim_axs(axes, N):
    """little helper to massage the axs list to have correct length..."""
    # axes.flat将axes数组转为一个迭代器
    # 因为最后返回的是数组axes中前N-1个元素
    # 所以这里要先axes = axes.flat，不能直接将axes.flat放到in后边循环
    # 如果直接循环axes.flat，其实axes还是原来的多维数组，没有序号为N-1的元素
    axes = axes.flat
    for axis in axes[N:]:
        axis.remove()
    return axes[:N]


fig1, axs = plt.subplots(rows, cols, figsize=figsize, constrained_layout=False)
# 根据分图的数量决定axes的数量
axs = trim_axs(axs, len(cases))
for ax, case in zip(axs, cases):
    ax.set_title('markevery=%s' % str(case))
    # ms圆圈的大小
    # ax.set_xscale('log')
    # ax.set_yscale('log')
    # ax.set_xlim((6, 6.7))
    # ax.set_ylim((1.1, 1.7))
    ax.plot(x, y, 'o', ls='-', ms=4, markevery=case)
r = np.linspace(0, 3.0, 200)
theta = 2 * np.pi * r
with plt.style.context('dark_background'):
    fig4, axs = plt.subplots(rows, cols, figsize=figsize,
                             subplot_kw={'projection': 'polar'}, constrained_layout=False)
    axs = trim_axs(axs, len(cases))
    for ax, case in zip(axs, cases):
        ax.set_title('markevery=%s' % str(case))
        ax.plot(theta, r, 'o', ls='-', ms=4, markevery=case)
plt.show()


