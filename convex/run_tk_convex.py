#!/usr/bin/env -S python3 -B
from tk_drawer import TkDrawer
from r2point import R2Point
from convex import Void, Point, Segment, Polygon


def void_draw(self, tk):
    pass


def point_draw(self, tk):
    tk.draw_point(self.p)


def segment_draw(self, tk):
    tk.draw_line(self.p, self.q)


def polygon_draw(self, tk):
    for n in range(self.points.size()):
        tk.draw_line(self.points.last(), self.points.first())
        self.points.push_last(self.points.pop_first())


setattr(Void, 'draw', void_draw)
setattr(Point, 'draw', point_draw)
setattr(Segment, 'draw', segment_draw)
setattr(Polygon, 'draw', polygon_draw)

ztr = []
try:
    for i in range(3):
        print(f"{i+1} точка замкнутого треугольника")
        ztr.append(R2Point())
except (EOFError, KeyboardInterrupt, ValueError):
    print("\n=(")

tk = TkDrawer()
f = Void(ztr)
tk.clean()

try:
    while True:
        tk.draw_point(ztr[0])
        tk.draw_line(ztr[0], ztr[1])
        tk.draw_line(ztr[1], ztr[2])
        tk.draw_line(ztr[2], ztr[0])
        print("введите точку для расчета оболочки")
        f = f.add(R2Point())
        tk.clean()
        f.draw(tk)
        print(f"S = {f.area()}, P = {f.perimeter()}, count = {f.count()}")
except (EOFError, KeyboardInterrupt, ValueError):
    print("\nStop")
    tk.close()
