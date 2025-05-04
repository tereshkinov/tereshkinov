#!/usr/bin/env python3

import re
from operator import add, sub, mul, truediv
from stack import Stack
from compf import Compf


class Calc(Compf):
    '''
    модификации есть и в компиляторе, я там их и указал
    self.count является списком с количеством различных цифр
    '''

    SYMBOLS = re.compile("[0-9]")

    def __init__(self):
        super().__init__()
        self.r = Stack()
        self.count = [0 for i in range(11)]

    # Интерпретация арифметического выражения
    def compile(self, str):
        self.count = [0 for i in range(11)] #11 ячеек для правильной работы $9
        Compf.compile(self, str)
        return self.r.top()

    # Обработка цифры
    def process_value(self, c):
        self.r.push(int(c))
        self.count[int(c)] += 1

    # Обработка символа операции
    def process_oper(self, c):
        if c == '$':
            first = self.r.pop()
            kkk = 0
            for i in range(first + 1):
                kkk += self.count[i]
            self.r.push(kkk -1)
            self.count[first] -= 1

        else:
            second, first = self.r.pop(), self.r.pop()
            self.r.push({"+": add, "-": sub, "*": mul,
                         "/": truediv}[c](first, second))


if __name__ == "__main__":
    c = Calc()
    while True:
        str = input("Арифметическое выражение: ")
        print(f"Результат его вычисления: {c.compile(str)}")
        print()
