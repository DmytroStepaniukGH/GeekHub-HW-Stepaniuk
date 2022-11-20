"""
3. Створіть клас в якому буде атрибут який буде рахувати кількість створених
   екземплярів класів.
"""


class Car:
    count = 0

    def __init__(self, car):
        Car.count += 1
        self.car = car

    def print_car_name(self):
        print(self.car)


if __name__ == "__main__":
    car1 = Car('Opel')
    print(car1.count)

    car2 = Car('Daewoo')
    print(car2.count)

    car3 = Car('BMW')
    print(car3.count)

    car4 = Car('Audi')
    print(car4.count)
