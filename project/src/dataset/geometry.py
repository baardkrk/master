import math
import numpy as np


class Point2D:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.row, self.col = y, x

    def __str__(self):
        return f'({self.x}, {self.y})'


class Point3D:
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z

    def __str__(self):
        return f'({self.x}, {self.y}, {self.z})'


class Line3D:
    def __init__(self, *args, **kwargs):
        self.__point_init_args = ['point_a', 'point_b']
        self.__point_vec_args = ['point', 'vec']
        if (all({x in kwargs.keys() for x in self.__point_init_args}) or
                (isinstance(args[0], Point3D) and isinstance(args[1], Point3D))):
            self.__point_initialization(*args, **kwargs)
        elif (all({x in kwargs.keys() for x in self.__point_vec_args}) or
              (isinstance(args[0], Point3D) and isinstance(args[1], Vec3D))):
            self.__point_vec_initialization(*args, **kwargs)
        else:
            raise ValueError("Invalid arguments")

    def __point_initialization(self, *args, **kwargs):
        try:
            assert kwargs[self.__point_init_args[0]].isinstance(Point3D)
            assert kwargs[self.__point_init_args[1]].isinstance(Point3D)
            point_a = kwargs[self.__point_init_args[0]]
            point_b = kwargs[self.__point_init_args[1]]
        except (KeyError, AssertionError):
            point_a = args[0]
            point_b = args[1]
        self.pos = point_a
        x = point_b.x - point_a.x
        y = point_b.y - point_a.y
        z = point_b.z - point_a.z
        self.u = Vec3D(x, y, z, point_a)

    def __point_vec_initialization(self, *args, **kwargs):
        try:
            assert kwargs[self.__point_vec_args[0]].isinstance(Point3D)
            assert kwargs[self.__point_vec_args[1]].isinstance(Vec3D)
            self.pos = kwargs[self.__point_vec_args[0]]
            self.u = kwargs[self.__point_vec_args[1]]
        except (KeyError, AssertionError):
            self.pos = args[0]
            self.u = args[1]

    def __str__(self):
        return f'pos: {self.pos}, unit_vector: {self.u}'


class Vec3D:
    def __init__(self, x, y, z, pos=Point3D(0, 0, 0)):
        self.x, self.y, self.z = x, y, z
        self.pos = pos

    def norm(self):
        m = self.mag()
        if m == 0:
            raise RuntimeError("Cannot divide by zero.")
        return Vec3D(self.x / m, self.y / m, self.z / m, pos=self.pos)

    def mag(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def __str__(self):
        return f'pos: {self.pos}, components: ({self.x}, {self.y}, {self.z})'


def closest_points(line_a: Line3D, line_b: Line3D):
    t_term_1 = line_a.u.x ** 2 + line_a.u.y ** 2 + line_a.u.z ** 2
    s_term_1 = -(line_a.u.x * line_b.u.x + line_a.u.y * line_b.u.y + line_a.u.z * line_b.u.z)
    t_term_2 = line_a.u.x * line_b.u.x + line_a.u.y * line_b.u.y + line_a.u.z * line_b.u.z
    s_term_2 = -(line_b.u.x ** 2 + line_b.u.y ** 2 + line_b.u.z ** 2)
    q_term_1 = line_a.u.x * (line_b.pos.x - line_a.pos.x) + line_a.u.y * (line_b.pos.y - line_a.pos.y) + \
               line_a.u.z * (line_b.pos.z - line_a.pos.z)
    q_term_2 = line_b.u.x * (line_b.pos.x - line_a.pos.x) + line_b.u.y * (line_b.pos.y - line_a.pos.y) + \
               line_b.u.z * (line_b.pos.z - line_a.pos.z)
    a = np.array([[t_term_1, s_term_1],
                  [t_term_2, s_term_2]])
    b = np.array([[q_term_1],
                  [q_term_2]])
    res = np.linalg.solve(a, b)
    t = res[0][0]
    s = res[1][0]
    point_a = Point3D(line_a.pos.x + t*line_a.u.x,
                      line_a.pos.y + t*line_a.u.y,
                      line_a.pos.z + t*line_a.u.z)
    point_b = Point3D(line_b.pos.x + s*line_b.u.x,
                      line_b.pos.y + s*line_b.u.y,
                      line_b.pos.z + s*line_b.u.z)
    return point_a, point_b


def distance_to_3d_line(point: Point3D, line: Line3D):
    vec = Vec3D(point.x, point.y, point.z, Point3D(0, 0, 0))
    beam = Line3D(vec.pos, vec)
    closest, _ = closest_points(beam, line)
    return math.sqrt(closest.x**2 + closest.y**2 + closest.z**2)


if __name__ == '__main__':
    # Test closest points
    l1 = Line3D(Point3D(0.0, 2.0, -1.0), Vec3D(1.0, 1.0, 2.0))
    l2 = Line3D(Point3D(1.0, 0.0, -1.0), Vec3D(1.0, 1.0, 3.0))
    a, b = closest_points(l1, l2)
    assert (a.x, a.y, a.z) == (-1.5, 0.5, -4.0)
    assert (b.x, b.y, b.z) == (0.0, -1.0, -4.0)
