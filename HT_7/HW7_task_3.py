"""
3. Всі ви знаєте таку функцію як <range>. Напишіть свою реалізацію цієї
   функції. Тобто щоб її можна було використати у вигляді:
    for i in my_range(1, 10, 2):
        print(i)
    1
    3
    5
    7
    9
   P.S. Повинен вертатись генератор.
   P.P.S. Для повного розуміння цієї функції - можна почитати документацію
   по ній: https://docs.python.org/3/library/stdtypes.html#range
   P.P.P.S Не забудьте обробляти невалідні ситуації (типу range(1, -10, 5)
   тощо). Подивіться як веде себе стандартний range в таких випадках.
"""


def my_range(my_start, my_stop=None, my_step=None):
    if my_stop is None:
        if not isinstance(my_start, int):
            raise TypeError('Start must be integer')
        start = 0
        stop = my_start
        step = 1
    elif my_step is None:
        if not isinstance(my_stop, int):
            raise TypeError('Stop must be integer')
        start = my_start
        stop = my_stop
        step = 1
    else:
        if not isinstance(my_step, int):
            raise TypeError('Step must be integer')
        if my_step == 0:
            raise ValueError('Step must not be 0')
        start = my_start
        stop = my_stop
        step = my_step

    if step > 0:
        while start < stop:
            yield start
            start += step

    elif step < 0:
        while start > stop:
            yield start
            start += step


if __name__ == "__main__":
    for i in my_range(1, 10, 2):
        print(i)

    print(list(range(0, -10, -1)))
    print(list(my_range(0, -10, -1)))
    print(list(range(0, -10, -2)))
    print(list(my_range(0, -10, -2)))
    print(list(range(0)))
    print(list(my_range(0)))
    print(list(range(4)))
    print(list(my_range(4)))
    print(list(range(2, 5)))
    print(list(my_range(2, 5)))
    print(list(range(1, -10, 5)))
    print(list(my_range(1, -10, 5)))
    print(list(my_range(1, -10, 0)))
    print(list(range(1, -10, 0)))
