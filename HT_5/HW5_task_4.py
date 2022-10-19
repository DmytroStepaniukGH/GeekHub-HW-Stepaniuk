"""
4. Написати функцію <prime_list>, яка прийматиме 2 аргументи - початок
   і кінець діапазона, і вертатиме список простих чисел всередині цього
   діапазона. Не забудьте про перевірку на валідність введених даних та у
   випадку невідповідності - виведіть повідомлення.
"""


def prime_list(start_range, end_range):
    prime_numbers = []

    for number in range(start_range, end_range + 1):
        if number > 1:
            for i in range(2, number):
                if number % i == 0:
                    break
            else:
                prime_numbers.append(number)

    return prime_numbers


if __name__ == "__main__":
    start_number = input('Input start: ')
    end_number = input('Input start: ')

    try:
        print(prime_list(int(start_number), int(end_number)))
    except ValueError:
        print('The values entered are not valid numbers')
