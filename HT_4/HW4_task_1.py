"""
1. Написати функцiю season, яка приймає один аргумент
   (номер мiсяця вiд 1 до 12) та яка буде повертати пору року, до якої цей
   мiсяць належить (зима, весна, лiто або осiнь). У випадку некоректного
   введеного значення - виводити відповідне повідомлення.
"""


def season(month):
    if month in range(1, 3) or month == 12:
        return 'Winter'
    elif month in range(3, 6):
        return 'Spring'
    elif month in range(6, 9):
        return 'Summer'
    elif month in range(9, 12):
        return 'Autumn'
    else:
        return 'The value is not a month number'


if __name__ == "__main__":
    value = input('Enter the month number (from 1 to 12): ')

    try:
        print(season(int(value)))
    except ValueError:
        print(f'Error: {value} is not an integer')
