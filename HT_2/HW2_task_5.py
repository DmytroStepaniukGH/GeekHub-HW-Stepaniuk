"""
5. Write a script which accepts a decimal number from user and converts
   it to hexadecimal.
"""
if __name__ == "__main__":
    number = int(input('Please, input a number: '))

    print(f'{number} in hexadecimal: {hex(number)[2:]}')