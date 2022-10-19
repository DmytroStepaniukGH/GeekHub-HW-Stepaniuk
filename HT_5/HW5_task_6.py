"""
6. Написати функцію, яка буде реалізувати логіку циклічного зсуву елементів
   в списку. Тобто функція приймає два аргументи: список і величину зсуву
   (якщо ця величина додатна - пересуваємо з кінця на початок, якщо
   від'ємна - навпаки - пересуваємо елементи з початку списку в його
   кінець). Наприклад:
   fnc([1, 2, 3, 4, 5], shift=1) --> [5, 1, 2, 3, 4]
   fnc([1, 2, 3, 4, 5], shift=-2) --> [3, 4, 5, 1, 2]
"""


def shift_values(list_to_shift, shift):
    if shift > 0:
        for i in range(0, shift):
            list_to_shift.insert(0, list_to_shift.pop())
        return list_to_shift
    elif shift < 0:
        for i in range(0, -shift):
            list_to_shift.append(list_to_shift.pop(0))
        return list_to_shift
    else:
        return list_to_shift


if __name__ == "__main__":
    test_list = [1, 2, 3, 4, 5]
    shift = input('Input shift: ')

    try:
        print(shift_values(test_list, int(shift)))
    except ValueError:
        print('The values entered are not valid numbers')
