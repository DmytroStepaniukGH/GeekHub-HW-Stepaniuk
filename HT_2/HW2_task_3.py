"""
3. Write a script which accepts a <number> from user and print out a sum
   of the first <number> positive integers.
"""
if __name__ == "__main__":
    number = int(input('Please, input a number: '))

    sum_of_numbers = 0
    for i in range(1, number+1):
        sum_of_numbers += i

    print(f'Sum of first positive integers up to and including {number} = {sum_of_numbers}')
