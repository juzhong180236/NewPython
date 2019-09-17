import turtle as t
import turtle
from turtle import *

# 四个参数分别是窗体的宽、高、x位置、y位置（屏幕左上角和窗体左上角的相对位置，默认居中）
# turtle.setup(650, 350, 200, 200)
t.setup(650, 350, 200, 200)
# turtle.penup()
penup()
# turtle.goto(x, y)在世界坐标系中以直线连接点
# turtle坐标系，就是局部坐标，fd(d)正前方，bk(d)正后方，circle(r,angle)转圈
# turtle.fd(-250)
# turtle.pendown()
# turtle.pensize(25)
# turtle.pencolor('purple')
fd(-250)
pendown()
pensize(25)
pencolor('purple')
# 设置海龟的朝向，seth(angle)在世界坐标系中改变海龟的朝向，逆时针旋转为正度数
# 在turtle坐标系中，left(angle),right(angle)设置海龟的朝向
# turtle.colormode(mode) mode 1.0/mode 255
# turtle.seth(-40)
# for i in range(4):
#     turtle.circle(40, 80)
#     turtle.circle(-40, 80)
# turtle.circle(40, 80 / 2)
# turtle.fd(40)
# turtle.circle(16, 180)
# turtle.fd(20 * 2 / 3)
# turtle.done()
seth(-40)
for i in range(4):
    circle(40, 80)
    circle(-40, 80)
circle(40, 80 / 2)
fd(40)
circle(16, 180)
fd(20 * 2 / 3)
done()
