"""
5. Написати функцію <fibonacci>, яка приймає один аргумент і виводить всі
   числа Фібоначчі, що не перевищують його.
"""


def fibonacci(n):
    numbers_fib = [0, 1]

    if n < 0:
        return 'Number < 0'
    elif n == 0:
        return 'Please, input number > 0'
    elif n == 1:
        return numbers_fib[:-1]
    elif n == 2:
        numbers_fib.append(1)
        return numbers_fib
    else:
        i = 2
        next_number = 2
        while next_number < n:
            next_number = numbers_fib[i - 1] + numbers_fib[i - 2]
            i += 1
            numbers_fib.append(next_number)
        return numbers_fib[:-1]


if __name__ == "__main__":
    number = input('Input number: ')

    try:
        print(fibonacci(int(number)))
    except ValueError:
        print('The values entered are not valid numbers')
