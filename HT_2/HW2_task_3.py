"""
3. Write a script which accepts a <number> from user and print out a sum
   of the first <number> positive integers.
"""
if __name__ == "__main__":
    number = int(input('Please, input a number: '))

    print(f'Sum of first positive integers up to and including {number} = {sum(range(1, number+1))}')
