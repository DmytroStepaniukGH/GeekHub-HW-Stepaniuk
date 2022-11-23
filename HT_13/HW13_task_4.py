"""
4. Створіть клас, який буде повністю копіювати поведінку list, за виключенням
   того, що індекси в ньому мають починатися з 1, а індекс 0 має викидати
   помилку (такого ж типу, яку кидає list якщо звернутися до неіснуючого
   індексу)
"""


class MyList(list):
    def __getitem__(self, index):
        if index == 0:
            raise IndexError('List index out of range')
        index -= 1
        return list.__getitem__(self, index)

    def __setitem__(self, index, item):
        if index == 0:
            raise IndexError('list index out of range')
        index -= 1
        return list.__setitem__(self, index, item)


if __name__ == "__main__":
    test_list = MyList([1, 2, 3, 4])
    print(test_list[1])
    print(test_list[0])
