#!/usr/bin/env -S python3 -B

import re
from stack import Stack


class Compf:

    """
    Grammar

    G0:
    F -> T | F+T | F-T
    T -> M | T*M | T/M
    M -> (F) | {F} | V
    V -> a | b | c | ... | z

    Gs:
    E -> EE+ | EE- | EE* | EE/ | ED* | a | b | ... | z

    """

    SYMBOLS = re.compile("[a-z]")

    def __init__(self):
        self.s = Stack()
        self.data = []
        self.data_figure = ''
        self.compiled_figure = ''

    def compile(self, str):
        self.data.clear()
        for c in "(" + str + ")":
            self.process_symbol(c)
        return " ".join(self.data)

    def process_symbol(self, c):
        if c == '{' or len(self.data_figure) > 0:
            self.data_figure += c
            if self.data_figure.count('{') == self.data_figure.count('}'):
                self.data_figure = self.data_figure[1: -1]
                compilator_figure = Compf()
                self.compiled_figure = compilator_figure.compile(self.data_figure)
                self.s.push(self.compiled_figure)
                self.data.append(self.s.pop())
                self.data.append('D')
                self.data.append('*')
                self.compiled_figure = ''
                self.data_figure = ''

        elif c == "(":
            self.s.push(c)
        elif c == ")":
            self.process_suspended_operators(c)
            self.s.pop()
        elif c in "+-*/":
            self.process_suspended_operators(c)
            self.s.push(c)
        else:
            self.check_symbol(c)
            self.process_value(c)

    def process_suspended_operators(self, c):
        while self.is_precedes(self.s.top(), c):
            self.process_oper(self.s.pop())

    def process_value(self, c):
        self.data.append(c)

    def process_oper(self, c):
        self.data.append(c)

    @classmethod
    def check_symbol(self, c):
        if not self.SYMBOLS.match(c):
            raise Exception(f"Недопустимый символ '{c}'")

    @staticmethod
    def priority(c):
        return 1 if (c == "+" or c == "-") else 2

    @staticmethod
    def is_precedes(a, b):
        if a == "(":
            return False
        elif b == ")":
            return True
        else:
            return Compf.priority(a) >= Compf.priority(b)


if __name__ == "__main__":
    c = Compf()
    while True:
        str = input("Арифметическая  формула: ")
        print(f"Результат её компиляции: {c.compile(str)}")
        print()
