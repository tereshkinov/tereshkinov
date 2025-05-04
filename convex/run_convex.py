#!/usr/bin/env -S python3 -B
from r2point import R2Point
from convex import Void

ztr = []
try:
    for i in range(3):
        print(f"{i+1} точка замкнутого треугольника")
        ztr.append(R2Point())
except (EOFError, KeyboardInterrupt):
    print("\n=(")

f = Void(ztr)
try:
    while True:
        print("введите точку для расчета оболочки")
        f = f.add(R2Point())
        print(f"S = {f.area()}, P = {f.perimeter()}, count = {f.count()}")
        print()
except (EOFError, KeyboardInterrupt):
    print("\nStop")
