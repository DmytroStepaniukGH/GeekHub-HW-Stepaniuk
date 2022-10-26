"""
6. Напишіть функцію,яка приймає рядок з декількох слів і повертає довжину
   найкоротшого слова. Реалізуйте обчислення за допомогою генератора в
   один рядок.
"""


def shortest_word(sequence):
    return min([len(x) for x in sequence.split()])


if __name__ == "__main__":
    test_string = input('Input string: ')

    print(shortest_word(test_string))
