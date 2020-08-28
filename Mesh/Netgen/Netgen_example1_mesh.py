import netgen.gui
from ngsolve import *
from netgen import geom2d as g2


# mesh = Mesh(g2.unit_square.GenerateMesh(maxh=0.2))
# print(mesh.nv,mesh.ne)  # number of vertices & elements

def example1():
    geo = g2.SplineGeometry()
    p1 = geo.AppendPoint(0, 0)
    p2 = geo.AppendPoint(1, 0)
    p3 = geo.AppendPoint(1, 1)
    p4 = geo.AppendPoint(0, 1)

    geo.Append(["line", p1, p2])
    geo.Append(["line", p2, p3])
    geo.Append(["line", p3, p4])
    geo.Append(["line", p4, p1])

    mesh = geo.GenerateMesh(maxh=0.5)
    print(len(mesh.Points()))
    # for p in mesh.Points():
    #     x, y, z = p.p
    #     print(x, y)
    # for el in mesh.Elements2D():
    #     print(el.vertices)


# example1()


def example2():
    geo = g2.SplineGeometry()
    p1, p2, p3, p4 = [geo.AppendPoint(x, y) for x, y in [(0, 0), (1, 0), (1, 1), (0, 1)]]
    geo.Append(["line", p1, p2])
    geo.Append(["spline3", p2, p3, p4])
    geo.Append(["line", p4, p1])
    mesh = geo.GenerateMesh(maxh=0.1)

    for p in mesh.Points():
        x, y, z = p.p
        print(x, y)
    for el in mesh.Elements2D():
        print(el.vertices)


# example2()

def example3():
    geo = g2.SplineGeometry()
    p1, p2, p3, p4 = [geo.AppendPoint(x, y) for x, y in [(0, 0), (1, 0), (1, 1), (0, 1)]]
    p5, p6 = [geo.AppendPoint(x, y) for x, y in [(2, 0), (2, 1)]]
    # 可以给出多个区域的网格，默认是左边是1，右边是0，如果区域增加就需要更多的数字
    geo.Append(["line", p1, p2], leftdomain=1, rightdomain=0)
    geo.Append(["line", p2, p3], leftdomain=1, rightdomain=2)
    geo.Append(["line", p3, p4], leftdomain=1, rightdomain=0)
    geo.Append(["line", p4, p1], leftdomain=1, rightdomain=0)
    geo.Append(["line", p2, p5], leftdomain=2, rightdomain=0)
    geo.Append(["line", p5, p6], leftdomain=2, rightdomain=0)
    geo.Append(["line", p6, p3], leftdomain=2, rightdomain=0)
    mesh = geo.GenerateMesh(maxh=0.1)
    for p in mesh.Points():
        x, y, z = p.p
        print(x, y)


# example3()

def example4():
    geo = g2.SplineGeometry()
    p1, p2, p3, p4 = [geo.AppendPoint(x, y) for x, y in [(0, 0), (1, 0), (1, 1), (0, 1)]]
    geo.Append(["line", p1, p2], maxh=0.1)
    geo.Append(["line", p2, p3])
    geo.Append(["line", p3, p4])
    geo.Append(["line", p4, p1])
    geo.SetDomainMaxH(1, 0.1)  # 对指定区域按照第二个参数设置全域网格大小
    geo.SetMaterial(1, "iron")

    mesh = geo.GenerateMesh()
    # print(geo.SetMaterial(1, "iron"))
    print(len(mesh.Points()))
    # for p in mesh.Points():
    #     x, y, z = p.p
    #     print(x, y)
    # for el in mesh.Elements2D():
    #     print(el.vertices)
    # pass


def example5():
    geo = g2.SplineGeometry()
    p1, p2, p3, p4 = [geo.AppendPoint(x, y) for x, y in [(0, 0), (1, 0), (1, 1), (0, 1)]]
    p5, p6 = [geo.AppendPoint(x, y) for x, y in [(2, 0), (2, 1)]]
    # 可以给出多个区域的网格，默认是左边是1，右边是0，如果区域增加就需要更多的数字
    geo.Append(["line", p1, p2], leftdomain=1, rightdomain=0, maxh=0.1)
    geo.Append(["line", p2, p3], leftdomain=1, rightdomain=2)
    geo.Append(["line", p3, p4], leftdomain=1, rightdomain=0)
    geo.Append(["line", p4, p1], leftdomain=1, rightdomain=0)
    geo.Append(["line", p2, p5], leftdomain=2, rightdomain=0)
    geo.Append(["line", p5, p6], leftdomain=2, rightdomain=0)
    geo.Append(["line", p6, p3], leftdomain=2, rightdomain=0)
    geo.SetDomainMaxH(2, 0.01)  # 对指定区域按照第二个参数设置全域网格大小
    geo.SetMaterial(2, "iron")
    # geo.AddCircle(c=(5, 0), r=0.5, leftdomain=2, rightdomain=1)
    # geo.AddRectangle((0, 0), (3, 2))

    mesh = geo.GenerateMesh()
    for p in mesh.Points():
        x, y, z = p.p
        print(x, y)


def example6():
    geo = g2.SplineGeometry()
    p1 = geo.AppendPoint(0, 0)
    p2 = geo.AppendPoint(1, 0)
    p3 = geo.AppendPoint(1, 1)
    p4 = geo.AppendPoint(0, 1)

    geo.Append(["line", p1, p2])
    geo.Append(["line", p2, p3])
    geo.Append(["line", p3, p4])
    geo.Append(["line", p4, p1])
    mesh = geo.GenerateMesh(maxh=0.5, quad_dominated=True)
    print(len(mesh.Points()))
    # for p in mesh.Points():
    #     x, y, z = p.p
    #     print(x, y)
    # for el in mesh.Elements2D():
    #     print(el.vertices)


example1()
# example4()
example6()
