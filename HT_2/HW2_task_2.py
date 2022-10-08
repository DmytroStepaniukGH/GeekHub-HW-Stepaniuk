"""
2. Write a script which accepts two sequences of comma-separated colors
   from user. Then print out a set containing all the colors from
   color_list_1 which are not present in color_list_2.
"""
if __name__ == "__main__":
    color_list_1 = input('Please, input a sequence of comma-separated colors: ')
    color_list_2 = input('Please enter another color sequence separated by commas: ')

    set_of_color_1 = set(color_list_1.split(','))
    set_of_color_2 = set(color_list_2.split(','))

    print(f'Colors from the first set that are not in the second: '
          f'{set_of_color_1.difference(set_of_color_2)}')

