"""
3. Користувач вводить змінні "x" та "y" з довільними цифровими значеннями.
   Створіть просту умовну конструкцію (звiсно вона повинна бути в тiлi
   ф-цiї), під час виконання якої буде перевірятися рівність змінних "x"
   та "y" та у випадку нерівності - виводити ще і різницю.
   Повинні працювати такі умови (x, y, z заміність на відповідні числа):
    x > y;       вiдповiдь - "х бiльше нiж у на z"
    x < y;       вiдповiдь - "у бiльше нiж х на z"
    x == y.      відповідь - "х дорівнює y"
"""


def comparison(x, y):
    if x > y:
        return f'{x} is greater than {y} by {x-y}'
    elif x < y:
        return f'{y} is greater than {x} by {y-x}'
    else:
        return f'{x} is equal to {y}'


if __name__ == "__main__":
    x = input('Input x: ')
    y = input('Input y: ')

    try:
        print(comparison(float(x), float(y)))
    except ValueError:
        print('The values entered are not valid numbers')
