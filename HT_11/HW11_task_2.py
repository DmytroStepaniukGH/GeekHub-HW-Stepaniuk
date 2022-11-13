"""
2. Створити клас Person, в якому буде присутнім метод __init__ який буде
   приймати якісь аргументи, які зберігатиме в відповідні змінні.
   - Методи, які повинні бути в класі Person - show_age, print_name,
   show_all_information.
   - Створіть 2 екземпляри класу Person та в кожному з екземплярів створіть
   атрибут profession (його не має інсувати під час ініціалізації в самому
   класі) та виведіть його на екран (прінтоніть)
"""


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def print_name(self):
        print(f'My name is {self.name}.')

    def show_age(self):
        print(f'I am {self.age}.')

    def show_all_information(self):
        self.print_name()
        self.show_age()


if __name__ == "__main__":
    user_1 = Person('Kolia', 27)
    user_1.profession = 'QA'

    user_2 = Person('Vasia', 32)
    user_2.profession = 'DevOps'

    user_2.show_all_information()
    print(user_2.profession)