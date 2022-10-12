"""
9. Користувачем вводиться початковий і кінцевий рік. Створити цикл, який
   виведе всі високосні роки в цьому проміжку (границі включно). P.S. Рік
   є високосним, якщо він кратний 4, але не кратний 100, а також якщо він
   кратний 400.
"""
if __name__ == "__main__":
    start_year = int(input('Input the starting year: '))
    final_year = int(input('Input the final year: '))

    for year in range(start_year, final_year+1):
        if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
            print(f'{year} is a leap year')
