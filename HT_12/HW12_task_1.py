"""
1. Напишіть програму, де клас «геометричні фігури» (Figure) містить
   властивість color з початковим значенням white і метод для зміни кольору
   фігури, а його підкласи «овал» (Oval) і «квадрат» (Square) містять методи
   _init_ для завдання початкових розмірів об'єктів при їх створенні.
"""


class Figure:
    color = 'white'

    def change_color(self, new_color):
        self.color = new_color


class Oval(Figure):
    def __init__(self, a, b):
        self.a = a
        self.b = b


class Square(Figure):
    def __init__(self, a):
        self.a = a


if __name__ == "__main__":
    oval = Oval(4, 5)
    square = Square(10)
    print(oval.color)
    print(square.color)
    oval.change_color('green')
    square.change_color('red')
    print(oval.color)
    print(square.color)