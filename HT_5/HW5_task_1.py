"""
1. Написати функцію <square>, яка прийматиме один аргумент - сторону
   квадрата, і вертатиме 3 значення у вигляді кортежа: периметр квадрата,
   площа квадрата та його діагональ.
"""
import math


def square(x):
    return x * 4, x * x, round(math.sqrt(2 * x**2), 2)


if __name__ == "__main__":
    x = input('Input x: ')

    try:
        print(square(float(x)))
    except ValueError:
        print('The values entered are not valid numbers')
