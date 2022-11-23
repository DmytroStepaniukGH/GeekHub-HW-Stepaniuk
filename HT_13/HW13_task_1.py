"""
1. Створіть клас Car, який буде мати властивість year (рік випуску).
   Додайте всі необхідні методи до класу, щоб можна було виконувати
   порівняння car1 > car2 , яке буде показувати, що car1 старша за car2.
   Також, операція car1 - car2 повинна повернути різницю між роками випуску.
"""


class Car:
    def __init__(self, name, year):
        self.name = name
        self.year = year

    def __gt__(self, other):
        return f'{self.name} старша за {other.name}' \
            if self.year < other.year\
            else f'{self.name} молодша за {other.name}'

    def __sub__(self, other):
        return f'Різниця: {abs(self.year - other.year)} років'


if __name__ == "__main__":
    car1 = Car('Audi', 1980)
    car2 = Car('BMW', 1992)
    print(car1 > car2)
    print(car1 - car2)