# import jieba
# import wordcloud
#
# txt = "航空航天，能源，风电，生物，医疗，机械，工程，建筑，城市，工厂，森林火灾，数字孪生，数字孪生，5G，大数据，工业互联网，工业4.0," \
#       "人工智能，机器学习，仿真，建模，3D，虚拟现实，增强现实，混合现实，传感器，通讯，智能制造，边缘计算，分布式存储，卫星，船舶，气候，物流，油田钻井"
#
# w = wordcloud.WordCloud(width=1000, font_path="msyh.ttc", height=800, background_color="white")
# w.generate(",".join(jieba.lcut(txt)))
# w.to_file("1.png")


# -*- coding:utf-8 -*-
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
# 构建数据
x = ['2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011',
     '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020']
y1 = [28, 24, 22, 27, 34, 25, 44, 36, 43, 34, 50, 60, 61, 75, 151, 331, 821, 779]
# y2 = [0, 0, 0, 0, 0, 0, 0, 5, 6, 14, 9, 22, 61, 78, 105, 151, 416]
bar_width = 0.36
fig = plt.figure(figsize=(10, 6))
# 将X轴数据改为使用range(len(x_data), 就是0、1、2...
# plt.bar(x=list(map(int, x)), height=y2, label='中文', color='#ff7f0e', alpha=0.8, width=bar_width)
plt.bar(x=list(map(int, x)), height=y1, label='英文', color='steelblue', alpha=0.8, width=bar_width)
# 将X轴数据改为使用np.arange(len(x_data))+bar_width,
# 就是bar_width、1+bar_width、2+bar_width...这样就和第一个柱状图并列了
# 在柱状图上显示具体数值, ha参数控制水平对齐方式, va控制垂直对齐方式
# for x1, yy in enumerate(y1):
#     plt.text(x1, yy + 1, str(yy), ha='center', va='bottom', fontsize=16, rotation=0)
# for x1, yy in enumerate(y2):
#     plt.text(x1 + bar_width, yy + 1, str(yy), ha='center', va='bottom', fontsize=16, rotation=0)
# 设置标题
# plt.title("[数字孪生]英文论文发表")
# 为两条坐标轴设置名称
x_ticks = np.arange(2003, 2021, 1)
y_ticks = np.arange(0, 851, 100)
plt.xticks(x_ticks, fontsize=13, rotation=30)
plt.yticks(y_ticks, fontsize=13)
plt.xlabel("Publication Year", fontsize=16)
plt.ylabel("Number of Papers", fontsize=16)
# 显示图例
# plt.legend()
# plt.savefig("a.jpg")
plt.show()
