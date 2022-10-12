"""
7. Write a script which accepts a <number>(int) from user and generates
   dictionary in range <number> where key is <number> and value is
   <number>*<number>
    e.g. 3 --> {0: 0, 1: 1, 2: 4, 3: 9}
"""
if __name__ == "__main__":
    number = int(input('Input a number to generate a dictionary: '))

    result = {number: number**2 for number in range(number+1)}
    print(f'Result: {result}')



