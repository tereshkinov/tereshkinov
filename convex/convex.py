from deq import Deq
from r2point import R2Point
from sympy import *


class Figure:
    def __init__(self):
        self.triangle = Deq()

    def perimeter(self):
        return 0.0

    def area(self):
        return 0.0

    def check_inside(self, point):
        if (not point.is_light(self.triangle.array[0],
                               self.triangle.array[1]) and
                not point.is_light(self.triangle.array[1],
                                   self.triangle.array[2]) and
                not point.is_light(self.triangle.array[2],
                                   self.triangle.array[0])):
            return True
        return False

    def intersection(self, point1, point2):
        if self.check_inside(point1) or self.check_inside(point2):
            return True
        x1, y1 = point1.x, point1.y
        x2, y2 = point2.x, point2.y
        for i in range(3):

            x3, y3 = self.triangle.array[i].x, self.triangle.array[i].y
            x4, y4 = (self.triangle.array[(i + 1) % 3].x,
                      self.triangle.array[(i + 1) % 3].y)

            dx1, dy1 = x2 - x1, y2 - y1
            dx2, dy2 = x4 - x3, y4 - y3

            dx3, dy3 = x1 - x3, y1 - y3

            det = dx1 * dy2 - dx2 * dy1
            det1 = dx1 * dy3 - dx3 * dy1
            det2 = dx2 * dy3 - dx3 * dy2

            if det == 0.0:
                if det1 != 0.0 or det2 != 0.0:
                    return False

                overlap_x = (min(x1, x2) < max(x3, x4)) and (min(x3, x4) < max(
                        x1, x2))
                overlap_y = (min(y1, y2) < max(y3, y4)) and (min(y3, y4) < max(
                        y1, y2))

                if overlap_x or overlap_y:
                    return True

                else:
                    if (x1, y1) == (x3, y3) and (x2, y2) == (x4, y4):
                        return True
                    elif (x1, y1) == (x3, y3) or (x1, y1) == (x4, y4):
                        return True
                    elif (x2, y2) == (x3, y3) or (x2, y2) == (x4, y4):
                        return True

                return False

            s = det1 / det
            t = det2 / det
            if 0.0 <= s <= 1.0 and 0.0 <= t <= 1.0:
                return True


class Void(Figure):
    """ "Hульугольник" """

    def __init__(self, ztr):
        self.ztr = ztr
        self.triangle = Deq()
        self.triangle.push_first(ztr[1])
        if ztr[1].is_light(ztr[0], ztr[2]):
            self.triangle.push_first(ztr[0])
            self.triangle.push_last(ztr[2])
        else:
            self.triangle.push_last(ztr[0])
            self.triangle.push_first(ztr[2])

    def add(self, p):
        return Point(p, self.triangle)

    def count(self):
        return 0


class Point(Figure):
    """ "Одноугольник" """

    def __init__(self, p, triangle):

        self.p = p
        self.triangle = triangle

    def add(self, q):
        return self if self.p == q else Segment(self.p, q, self.triangle)

    def count(self):
        return 0


class Segment(Figure):
    """ "Двуугольник" """

    def __init__(self, p, q, triangle):
        self.p, self.q = p, q
        self.triangle = triangle

    def count(self):
        return 2 if not (self.intersection(self.p, self.q))\
                    or self.intersection(self.p, self.q) is None else 0

    def perimeter(self):
        return 2.0 * self.p.dist(self.q)

    def add(self, r):
        if R2Point.is_triangle(self.p, self.q, r):
            if not (self.intersection(self.p, r)) and\
                    not (self.intersection(self.q, r)):
                return Polygon(self.p, self.q, r,
                               self.triangle, self.count()//2 + 2)
            elif not (self.intersection(self.p, r)) or\
                    not (self.intersection(self.q, r)):
                return Polygon(self.p, self.q, r,
                               self.triangle, self.count()//2 + 1)
            else:
                return Polygon(self.p, self.q, r,
                               self.triangle, self.count()//2)

        elif r.is_inside(self.p, self.q):
            return self
        elif self.p.is_inside(r, self.q):
            return Segment(r, self.q, self.triangle)
        else:
            return Segment(self.p, r, self.triangle)


class Polygon(Figure):
    """ Многоугольник """

    def __init__(self, a, b, c, triangle, count):
        self.cnt = count
        self.points = Deq()
        self.points.push_first(b)
        self.triangle = triangle
        if b.is_light(a, c):
            self.points.push_first(a)
            self.points.push_last(c)
        else:
            self.points.push_last(a)
            self.points.push_first(c)
        self._perimeter = a.dist(b) + b.dist(c) + c.dist(a)
        self._area = abs(R2Point.area(a, b, c))

    def perimeter(self):
        return self._perimeter

    def area(self):
        return self._area

    def count(self):
        return self.cnt

    def add(self, t):

        # поиск освещённого ребра
        for n in range(self.points.size()):
            if t.is_light(self.points.last(), self.points.first()):
                break
            self.points.push_last(self.points.pop_first())

        # хотя бы одно освещённое ребро есть
        if t.is_light(self.points.last(), self.points.first()):

            # учёт удаления ребра, соединяющего конец и начало дека
            self.cnt -= 1 if not\
                (self.intersection(self.points.last(),
                                   self.points.first())) else 0
            self._perimeter -= self.points.first().dist(self.points.last())
            self._area += abs(R2Point.area(t,
                                           self.points.last(),
                                           self.points.first()))

            # удаление освещённых рёбер из начала дека
            p = self.points.pop_first()
            while t.is_light(p, self.points.first()):
                self.cnt -= 1 if\
                    not (self.intersection(p, self.points.first())) else 0
                self._perimeter -= p.dist(self.points.first())
                self._area += abs(R2Point.area(t, p, self.points.first()))
                p = self.points.pop_first()
            self.points.push_first(p)

            # удаление освещённых рёбер из конца дека
            p = self.points.pop_last()
            while t.is_light(self.points.last(), p):
                self.cnt -= 1 if \
                    not (self.intersection(self.points.last(), p)) else 0
                self._perimeter -= p.dist(self.points.last())
                self._area += abs(R2Point.area(t, p, self.points.last()))
                p = self.points.pop_last()
            self.points.push_last(p)

            self.cnt += 1 if not (self.intersection(t, self.points.last()))\
                else 0
            self.cnt += 1 if not (self.intersection(self.points.first(), t))\
                else 0
            self._perimeter += t.dist(self.points.first()) + \
                t.dist(self.points.last())
            self.points.push_first(t)

        return self


if __name__ == "__main__":
    ztr = []
    ztr.append(R2Point(1, 1))
    ztr.append(R2Point(1, 2))
    ztr.append(R2Point(2, 1))

    f = Void(ztr)
    print(type(f), f.__dict__)
    f = f.add(R2Point(0.0, 0.0))
    print(type(f), f.__dict__)
    f = f.add(R2Point(1.0, 0.0))
    print(type(f), f.__dict__)
    f = f.add(R2Point(0.0, 1.0))
    print(type(f), f.__dict__)
