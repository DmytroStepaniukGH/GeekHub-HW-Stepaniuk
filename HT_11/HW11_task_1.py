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


class Calc:
    last_result = None

    def __init__(self, first_number, second_number):
        self.first_number = first_number
        self.second_number = second_number

    def add(self):
        self.current_res = self.first_number + self.second_number
        self.last_result = Calc.last_result
        Calc.last_result = self.current_res

    def subtraction(self):
        self.current_res = self.first_number - self.second_number
        self.last_result = Calc.last_result
        Calc.last_result = self.current_res

    def multiplication(self):
        self.current_res = self.first_number * self.second_number
        self.last_result = Calc.last_result
        Calc.last_result = self.current_res

    def division(self):
        self.current_res = self.first_number / self.second_number \
            if self.second_number != 0 else Exception('Division by zero')
        self.last_result = Calc.last_result
        Calc.last_result = self.current_res


if __name__ == "__main__":
    res = Calc(2, 5)
    print(f'Last result ( -> None): {res.last_result}')
    res.add()
    print(f'Last result (2 + 5 -> None): {res.last_result}')
    res.subtraction()
    print(f'Last result (2 - 5 -> 7): {res.last_result}')
    res.division()
    print(f'Last result (2 / 5 -> -3): {res.last_result}')
    res.multiplication()
    print(f'Last result (2 * 5 -> 0.4): {res.last_result}')


