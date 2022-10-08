"""
7. Write a script to concatenate all elements in a list into a string and
   print it. List must include both strings and integers and must
   be hardcoded.
"""
if __name__ == "__main__":
    group_of_values = [1, 2, 'geekhub', 'a', 4, True]

    result = ''
    for item in group_of_values:
        result += str(item)

    print(f'Result of concatenation: {result}')

