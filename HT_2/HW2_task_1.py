"""
1. Write a script which accepts a sequence of comma-separated numbers from
   user and generates a list and a tuple with those numbers.
"""
if __name__ == "__main__":
    numbers = input('Please, input a sequence of comma-separated numbers: ')
    list_of_numbers = numbers.split(',')
    tuple_of_numbers = tuple(list_of_numbers)

    print(f'List of numbers: {list_of_numbers}')
    print(f'Tuple of numbers: {tuple_of_numbers}')
