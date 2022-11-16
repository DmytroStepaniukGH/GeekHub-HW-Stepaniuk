"""
1. Створити клас Calc, який буде мати атребут last_result та 4 методи. Методи
   повинні виконувати математичні операції з 2-ма числами, а саме додавання,
   віднімання, множення, ділення.
   - Якщо під час створення екземпляру класу звернутися до атрибута last_result він повинен повернути пусте значення.
    - Якщо використати один з методів - last_result повинен повернути результат виконання ПОПЕРЕДНЬОГО методу.
    Example:
    last_result --> None
    1 + 1
    last_result --> None
    2 * 3
    last_result --> 2
    3 * 4
    last_result --> 6
    ...
    - Додати документування в клас (можете почитати цю статтю:
    https://realpython.com/documenting-python-code/ )
"""


class Calc():
    """
    Клас Calc для виконання математичних операцій додавння, віднімання,
    множення або ділення над двома дійсними числами

    ---------
    Attributes:
    last_result : int або float в залежності від використаного методу
        зберігає значенння останнього використаного методу,
        за замовчуванням дорівнює None
    ---------
    Methods:
    add(first_number, second_number)
        обчислює результат додавання двох чисел та змінює значення
        атрибута класу на поточний результат

    subtraction(first_number, second_number)
        обчислює результат віднімання двох чисел та змінює значення
        атрибута класу на поточний результат

    multiplication(first_number, second_number)
        обчислює результат множення двох чисел та змінює значення
        атрибута класу на поточний результат

    division(first_number, second_number)
        обчислює результат ділення двох чисел та змінює значення
        атрибута класу на поточний результат
    """
    last_result = None

    def add(self, first_number, second_number):
        current_res = first_number + second_number
        self.last_result = Calc.last_result
        Calc.last_result = current_res

    def subtraction(self, first_number, second_number):
        current_res = first_number - second_number
        self.last_result = Calc.last_result
        Calc.last_result = current_res

    def multiplication(self, first_number, second_number):
        current_res = first_number * second_number
        self.last_result = Calc.last_result
        Calc.last_result = current_res

    def division(self, first_number, second_number):
        current_res = first_number / second_number \
            if second_number != 0 else Exception('Division by zero')
        self.last_result = Calc.last_result
        Calc.last_result = current_res


if __name__ == "__main__":
    print(Calc.__doc__)
    res = Calc()
    print(f'Last result ( -> None): {res.last_result}')
    res.add(1, 1)
    print(f'Last result (1 + 1 -> None): {res.last_result}')
    res.subtraction(2, 5)
    print(f'Last result (2 - 5 -> 2): {res.last_result}')
    res.division(2, 5)
    print(f'Last result (2 / 5 -> -3): {res.last_result}')
    res.multiplication(2, 5)
    print(f'Last result (2 * 5 -> 0.4): {res.last_result}')
