from netgen.csg import *

# constructive solid geometry
left = Plane(Pnt(0, 0, 0), Vec(-1, 0, 0))
right = Plane(Pnt(1, 1, 1), Vec(1, 0, 0))
front = Plane(Pnt(0, 0, 0), Vec(0, -1, 0))
back = Plane(Pnt(1, 1, 1), Vec(0, 1, 0))
bot = Plane(Pnt(0, 0, 0), Vec(0, 0, -1))
top = Plane(Pnt(1, 1, 1), Vec(0, 0, 1))


def create_cube1():
    cube = left * right * front * back * bot * top
    geo = CSGeometry()
    geo.Add(cube)

    mesh = geo.GenerateMesh(maxh=0.1)
    mesh.Save("cube.vol")


def create_cube2():
    cube = OrthoBrick(Pnt(0, 0, 0), Pnt(1, 1, 1))
    hole = Cylinder(Pnt(0.5, 0.5, 0), Pnt(0.5, 0.5, 1), 0.2)

    geo = CSGeometry()
    geo.Add(cube - hole)
    mesh = geo.GenerateMesh(maxh=0.1)
    mesh.Save("cube_hole.vol")
    geo = CSGeometry()
    geo.Add(cube - hole)
    geo.Add(cube * hole)
