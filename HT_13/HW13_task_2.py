"""
2. Створити клас Matrix, який буде мати наступний функціонал:
    1. __init__ - вводиться кількість стовпців і кількість рядків
    2. fill() - заповнить створений масив числами - по порядку. Наприклад:
    +────+────+
    | 1  | 2  |
    +────+────+
    | 3  | 4  |
    +────+────+
    | 5  | 6  |
    +────+────+
    3. print_out() - виведе створений масив (якщо він ще не
       заповнений даними - вивести нулі
    4. transpose() - перевертає створений масив. Тобто, якщо взяти попередню
       таблицю, результат буде
    +────+────+────+
    | 1  | 3  | 5  |
    +────+────+────+
    | 2  | 4  | 6  |
    +────+────+────+
    P.S. Всякі там Пандас/Нампай не використовувати - тільки хардкор ;)
    P.P.S. Вивід не обов’язково оформлювати у вигляді таблиці - головне, щоб
           було видно, що це окремі стовпці / рядки
"""


class Matrix:
    arr = []

    def __init__(self, n, m):
        self.n = n
        self.m = m

    def print_out(self):
        if self.arr:
            for i in self.arr:
                for j in i:
                    if j // 10:
                        print(f'{j} ', end=' ')
                    else:
                        print(f'{j} ', end='  ')
                print('\n')
        else:
            for i in range(self.n):
                for j in range(self.m):
                    print(0, end=' ')
                print('\n')

    def fill(self):
        num = 0
        for i in range(self.n):
            arr_j = []
            for j in range(self.m):
                arr_j.append(num)
                num += 1
            self.arr.append(arr_j)

    def transpose(self):
        tr = [list(i) for i in zip(*self.arr)]
        for i in tr:
            for j in i:
                print(f'{j} ', end=' ')
            print('\n')


if __name__ == "__main__":
    a = Matrix(5, 10)
    a.print_out()
    a.fill()
    a.print_out()
    a.transpose()

