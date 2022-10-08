"""
4. Write a script which accepts a <number> from user and then <number>
   times asks user for string input. At the end script must print out
   result of concatenating all <number> strings.
"""
if __name__ == "__main__":
    number = int(input('Please, input a number: '))

    result = ''
    for i in range(1, number+1):
        result += input(f'Please, input the {i} string: ')

    print(f'Result of concatenating all {number} strings: {result}')