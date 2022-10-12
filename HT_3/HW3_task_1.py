"""
1. Write a script that will run through a list of tuples and replace the
   last value for each tuple. The list of tuples can be hardcoded. The
   "replacement" value is entered by user. The number of elements in the
   tuples must be different.
"""
if __name__ == "__main__":
    value = int(input('Input value: '))
    list_of_tuples = [(2, 3, 4, 1), (5, 6, 8, -4, 7, 33), (98, 6, 32)]

    list_of_tuples = [item[:-1]+(value,) for item in list_of_tuples]
    print(f'Result: {list_of_tuples}')
