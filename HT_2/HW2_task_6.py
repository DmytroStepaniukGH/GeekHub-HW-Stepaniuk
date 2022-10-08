"""
6. Write a script to check whether a value from user input is contained
   in a group of values.
    e.g. [1, 2, 'u', 'a', 4, True] --> 2 --> True
         [1, 2, 'u', 'a', 4, True] --> 5 --> False
"""
if __name__ == "__main__":
    value = int(input('Please, input a value: '))
    group_of_values = [1, 2, 'u', 'a', 4, True]

    print('True') if value in group_of_values else print('False')

