"""
5. Ну і традиційно - калькулятор: Повинна бути 1 функцiя, яка приймає 3
   аргументи - один з яких операцiя, яку зробити!
   Аргументи брати від юзера (можна по одному - окремо 2, окремо +, окремо
   2; можна всі разом - типу 2 + 2). Операції що мають бути присутні: +, -,
   *, /, %, //, **. Не забудьте протестувати з різними значеннями на
   предмет помилок!
"""


def calculator(x, operation, y):
    if operation == '+':
        return x + y
    elif operation == '-':
        return x - y
    elif operation == '*':
        return x * y
    elif operation == '/':
        try:
            return x / y
        except ZeroDivisionError:
            return 'Division by zero!'
    elif operation == '%':
        try:
            return x % y
        except ZeroDivisionError:
            return f'Division by zero!'
    elif operation == '//':
        try:
            return x // y
        except ZeroDivisionError:
            return f'Division by zero!'
    elif operation == '**':
        return x ** y
    else:
        return 'The entered mathematical operation is not correct'


if __name__ == "__main__":
    string_for_calc = input('Enter the data to be calculated separated'
                            ' by a space (ex. 2 + 5): ')
    data_of_string = string_for_calc.split(' ')

    try:
        print(calculator(float(data_of_string[0]), data_of_string[1],
                         float(data_of_string[2])))
    except ValueError:
        print('The data for the calculation was entered incorrectly')
