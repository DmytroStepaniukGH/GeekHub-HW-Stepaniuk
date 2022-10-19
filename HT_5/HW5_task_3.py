"""
3. Написати функцию <is_prime>, яка прийматиме 1 аргумент - число від
   0 до 1000, и яка вертатиме True, якщо це число просте і
   False - якщо ні.
"""


def is_prime(x):
    if x in range(2, 1001):
        for i in range(2, x):
            if x % i == 0:
                return False
        return True
    elif x > 1000:
        return 'The number was not verified as it is not in the range ' \
               '0-1000'
    else:
        return False


if __name__ == "__main__":
    x = input('Input x: ')

    try:
        print(is_prime(int(x)))
    except ValueError:
        print('The values entered are not valid numbers')
