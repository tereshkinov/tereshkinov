from pytest import approx
from math import *
from r2point import R2Point
from convex import Figure, Void, Point, Segment, Polygon
from deq import Deq


class TestVoid:

    # Инициализация (выполняется для каждого из тестов класса)
    def setup_method(self):
        ztr = [R2Point(1, 1), R2Point(1, 2), R2Point(2, 1)]

        self.f = Void(ztr)

    # Нульугольник является фигурой
    def test_figure(self):
        assert isinstance(self.f, Figure)

    def test_void(self):
        assert isinstance(self.f, Void)

    # Периметр нульугольника нулевой
    def test_perimeter(self):
        assert self.f.perimeter() == 0.0

    # Площадь нульугольника нулевая
    def test_area(self):
        assert self.f.area() == 0.0

    def test_count(self):
        assert self.f.count() == 0

    # При добавлении точки нульугольник превращается в одноугольник
    def test_add(self):
        assert isinstance(self.f.add(R2Point(0.0, 0.0)), Point)


class TestPoint:

    def setup_method(self):
        ztr = [R2Point(1, 1), R2Point(1, 2), R2Point(2, 1)]
        self.ztr = ztr
        self.triangle = Deq()
        self.triangle.push_first(ztr[1])
        self.triangle.push_last(ztr[0])
        self.triangle.push_first(ztr[2])
        ztr.append(R2Point(1, 1))
        ztr.append(R2Point(1, 2))
        ztr.append(R2Point(2, 1))
        self.f = Point(R2Point(0.0, 0.0), self.ztr)

    def test_count(self):
        assert self.f.count() == 0

    # Одноугольник является фигурой
    def test_figure(self):
        assert isinstance(self.f, Figure)

    # Конструктор порождает экземпляр класса Point (одноугольник)
    def test_point(self):
        assert isinstance(self.f, Point)

    # Периметр одноугольника нулевой
    def test_perimeter(self):
        assert self.f.perimeter() == 0.0

    # Площадь одноугольника нулевая
    def test_area(self):
        assert self.f.area() == 0.0

    # При добавлении точки одноугольник может не измениться
    def test_add1(self):
        assert self.f.add(R2Point(0.0, 0.0)) is self.f

    # При добавлении точки одноугольник может превратиться в двуугольник
    def test_add2(self):
        assert isinstance(self.f.add(R2Point(1.0, 0.0)), Segment)


class TestSegment:

    def setup_method(self):
        ztr = [R2Point(1, 1), R2Point(1, 2), R2Point(2, 1)]
        self.ztr = ztr
        self.triangle = Deq()
        self.triangle.push_first(ztr[1])
        self.triangle.push_last(ztr[0])
        self.triangle.push_first(ztr[2])
        ztr.append(R2Point(1, 1))
        ztr.append(R2Point(1, 2))
        ztr.append(R2Point(2, 1))
        self.f = Segment(R2Point(0.0, 0.0), R2Point(1.0, 0.0), self.triangle)

    def test_count(self):
        assert self.f.count() == 2

    # Двуугольник является фигурой
    def test_figure(self):
        assert (isinstance(self.f, Figure))

    # Конструктор порождает экземпляр класса Segment (двуугольник)
    def test_segment(self):
        assert isinstance(self.f, Segment)

    # Периметр двуугольника равен удвоенной длине отрезка
    def test_perimeter(self):
        assert self.f.perimeter() == approx(2.0)

    # Площадь двуугольника нулевая
    def test_area(self):
        assert self.f.area() == 0.0

    # При добавлении точки двуугольник может не измениться
    def test_add12323(self):
        assert self.f.add(R2Point(0.5, 0.0)) is self.f

    # Он не изменяется в том случае, когда добавляемая точка совпадает
    # с одним из концов отрезка
    def test_add1(self):
        assert self.f.add(R2Point(0.0, 0.0)) is self.f

    # При добавлении точки правее двуугольник может превратиться в другой
    # двуугольник
    def test_add2(self):
        assert isinstance(self.f.add(R2Point(2.0, 0.0)), Segment)

    # При добавлении точки левее двуугольник может превратиться в другой
    # двуугольник
    def test_add3(self):
        assert isinstance(self.f.add(R2Point(-1.0, 0.0)), Segment)

    # При добавлении точки двуугольник может превратиться в треугольник
    def test_add4(self):
        assert isinstance(self.f.add(R2Point(0.0, 1.0)), Polygon)


class TestPolygon:

    def setup_method(self):
        ztr4 = [R2Point(1, 1), R2Point(1, 2), R2Point(2, 1)]
        self.ztr = ztr4
        self.triangle = Deq()
        self.triangle.push_first(ztr4[1])
        self.triangle.push_last(ztr4[0])
        self.triangle.push_first(ztr4[2])
        self.a = R2Point(0.0, 0.0)
        self.b = R2Point(1.0, 0.0)
        self.c = R2Point(0.0, 1.0)
        self.f = Polygon(self.a, self.b, self.c, self.triangle, 0)

    def test_count1(self):
        assert self.f.count() == 0

    def test_figure(self):
        assert isinstance(self.f, Figure)

    def test_polygon1(self):
        assert isinstance(self.f, Polygon)

    def test_polygon2(self):
        self.f = Polygon(self.b, self.a, self.c, self.ztr, 2)
        assert isinstance(self.f, Polygon)

    def test_vertexes1(self):
        assert self.f.points.size() == 3

    def test_vertexes2(self):
        assert self.f.add(R2Point(0.1, 0.1)).points.size() == 3

    def test_vertexes3(self):
        assert self.f.add(R2Point(1.0, 1.0)).points.size() == 4

    def test_vertexes4(self):
        assert self.f.add(
            R2Point(
                0.4,
                1.0)).add(
            R2Point(
                1.0,
                0.4)).add(
                    R2Point(
                        0.8,
                        0.9)).add(
                            R2Point(
                                0.9,
                                0.8)).points.size() == 7
        assert self.f.add(R2Point(2.0, 2.0)).points.size() == 4

    def test_perimeter1(self):
        assert self.f.perimeter() == approx(2.0 + sqrt(2.0))

    def test_perimeter2(self):
        assert self.f.add(R2Point(1.0, 1.0)).perimeter() == approx(4.0)

    def test_area1(self):
        assert self.f.area() == approx(0.5)

    def test_area2(self):
        assert self.f.add(R2Point(1.0, 1.0)).area() == approx(1.0)


class TestModSegmentDegenerateTriangle:
    def setup_method(self):
        self.triangle = Deq()
        self.triangle.array = [R2Point(1.0, 1.0),
                               R2Point(1.0, 1.0), R2Point(1.0, 1.0)]
        self.a = R2Point(0.0, 0.0)
        self.b = R2Point(2.0, 2.0)
        self.c = R2Point(1.0, 1.0)
        self.d = R2Point(0.0, 1.0)
        self.short = Segment(self.a, self.c, self.triangle)
        self.dot1 = Point(self.c, self.triangle)
        self.dot2 = Point(self.b, self.triangle)
        self.long = Segment(self.a, self.b, self.triangle)
        self.vertical = Segment(self.a, self.d, self.triangle)

    def test_count1(self):
        assert self.short.count() == 0

    def test_count2(self):
        assert self.long.count() == 0

    def test_count3(self):
        assert self.vertical.count() == 2

    def test_count_dot1(self):
        assert self.dot1.count() == 0

    def test_count_dot2(self):
        assert self.dot2.count() == 0
