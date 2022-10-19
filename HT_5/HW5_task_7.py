"""
7. Написати функцію, яка приймає на вхід список (через кому), підраховує
   кількість однакових елементів у ньому і виводить результат. Елементами
   списку можуть бути дані будь-яких типів.
   Наприклад:
   1, 1, 'foo', [1, 2], True, 'foo', 1, [1, 2] ----> "1 -> 3, foo -> 2,
   [1, 2] -> 2, True -> 1"
"""


def find_duplicate(list_to_find):
    result = []
    for item in list_to_find:
        count = 0
        for to_check in list_to_find:
            if type(item) == type(to_check):
                if item == to_check:
                    count += 1

        if f'{item} -> {count}' not in result:
            result.append(f'{item} -> {count}')
    return result


if __name__ == "__main__":
    test_list = [1, 1, 'foo', [1, 2], True, 'foo', 1, [1, 2], (), {}, {}]
    print(find_duplicate(test_list))
