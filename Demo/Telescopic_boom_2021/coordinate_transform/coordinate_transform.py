import numpy as np


def translate(_point, dx, dy, dz):
    return [_point[0] + dx, _point[1] + dy, _point[2] + dz]


def scale(_point, sx, sy, sz):
    return [_point[0] * sx, _point[1] * sy, _point[2] * sz]


def rotateX(_point, angle):
    radian = np.pi / 180 * angle
    cosa = np.cos(radian)
    sina = np.sin(radian)
    return [_point[0],
            _point[1] * cosa - _point[2] * sina,
            _point[1] * sina + _point[2] * cosa]


def rotateY(_point, angle):
    radian = np.pi / 180 * angle
    cosa = np.cos(radian)
    sina = np.sin(radian)
    return [_point[2] * sina + _point[0] * cosa,
            _point[1],
            _point[2] * cosa - _point[0] * sina]


def rotateZ(_point, angle):
    radian = np.pi / 180 * angle
    cosa = np.cos(radian)
    sina = np.sin(radian)
    return [_point[0] * cosa - _point[1] * sina,
            _point[0] * sina - _point[1] * cosa,
            _point[2]]


if __name__ == "__main__":
    point1 = [0, 20, 0]
    print(rotateX(point1, 60))
