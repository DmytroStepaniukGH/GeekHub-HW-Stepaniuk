"""
2. Створіть програму для отримання курсу валют за певний період.
   - отримати від користувача дату (це може бути як один день так і
     інтервал - початкова і кінцева дати, продумайте механізм реалізації)
     і назву валюти
   - вивести курс по відношенню до гривні на момент вказаної дати (або за
     кожен день у вказаному інтервалі)
   - не забудьте перевірку на валідність введених даних
"""
import requests
import re
from datetime import datetime


class CurrencyHistory:
    def __init__(self, currency, start_date, end_date=None):
        self.currency = currency
        self.start_date = start_date
        self.end_date = end_date

    def __get_url(self):
        if self.end_date is not None:
            url = f"https://api.exchangerate.host/timeseries?" \
                  f"base={self.currency}" \
                  f"&start_date={self.start_date}" \
                  f"&end_date={self.end_date}" \
                  f"&symbols='UAH'"
            return url
        else:
            url = f"https://api.exchangerate.host/timeseries?" \
                  f"base={self.currency}" \
                  f"&start_date={self.start_date}" \
                  f"&end_date={self.start_date}" \
                  f"&symbols='UAH'"
            return url

    def show_history(self):
        response = requests.get(self.__get_url())
        data = response.json()
        rates = []
        for i, j in data["rates"].items():
            rates.append([i, j['UAH']])

        print(f'{self.currency} -> UAH')
        print(f'Дата\t\t\tКурс')
        for day in rates:
            print(f'{day[0]}\t\t{day[1]}')

        print('\n')


class Validate:
    @staticmethod
    def validate_format_currency(currency):
        cur_pattern = "^[A-Z]{3}$"
        return True if re.match(cur_pattern, currency) else False

    @staticmethod
    def validate_date_format(date):
        date_pattern = "^[0-9]{4}\\-[0-9]{2}\\-[0-9]{2}$"

        return True if re.match(date_pattern, date) else False

    @staticmethod
    def validate_current_date(date):
        now = datetime.now()
        current_date = str(now)[:10].split('-')
        date_slit = date.split('-')

        date_now = datetime(int(current_date[0]),
                            int(current_date[1]),
                            int(current_date[2]))
        input_date = datetime(int(date_slit[0]),
                              int(date_slit[1]),
                              int(date_slit[2]))

        return date_now >= input_date


def main():
    print('Вітаємо в архіві валют!')
    in_menu = True
    while in_menu:
        action = input('Оберіть необхідну дію: \n'
                       '1 - Показати курс валюти за певну дату\n'
                       '2 - Показати курс валюти за проміжок часу\n'
                       '3 - Вихід\n'
                       'Ваш вибір: ')
        try:
            if int(action) == 1:
                currency = input('Введіть код необхідної валюти '
                                 '(USD, EUR, CZK і т.д.): ')
                if Validate.validate_format_currency(currency):
                    date = input('Введіть дату в форматі РРРР-ММ-ДД '
                                 '(наприклад, 2022-11-27): ')
                    if Validate.validate_date_format(date):
                        if Validate.validate_current_date(date):
                            curr_hist = CurrencyHistory(currency, date)
                            try:
                                curr_hist.show_history()
                            except KeyError:
                                print('Нажаль, на введену дату інформація по '
                                      'курсу відносно гривні недоступна\n')
                        else:
                            print('Введена дата не повинна перевищувати '
                                  'сьогоднішню дату\n')
                    else:
                        print('Введена дата не відповідає формату '
                              'РРРР-ММ-ДД\n')
                else:
                    print('Введена валюта не відповідає формату CCC\n')
            elif int(action) == 2:
                currency = input('Введіть код необхідної валюти '
                                 '(USD, EUR, CZK і т.д.): ')
                if Validate.validate_format_currency(currency):
                    start_date = input('Введіть початкову дату в форматі '
                                       'РРРР-ММ-ДД (наприклад, 2022-11-20): ')
                    if Validate.validate_date_format(start_date):
                        if Validate.validate_current_date(start_date):
                            end_date = input('Введіть кінцеву дату в форматі'
                                             ' РРРР-ММ-ДД (наприклад, '
                                             '2022-11-20): ')
                            if Validate.validate_date_format(end_date):
                                if Validate.validate_current_date(end_date):
                                    curr_hist = CurrencyHistory(currency,
                                                                start_date,
                                                                end_date)
                                    try:
                                        curr_hist.show_history()
                                    except KeyError:
                                        print('Нажаль, за даний проміжок '
                                              'інформація по курсу відносно '
                                              'гривні недоступна\n')
                                else:
                                    print('Введена дата не повинна '
                                          'перевищувати сьогоднішню дату\n')
                            else:
                                print('Введена дата не відповідає '
                                      'формату РРРР-ММ-ДД\n')
                        else:
                            print('Введена дата не повинна перевищувати '
                                  'сьогоднішню дату\n')
                    else:
                        print('Введена дата не відповідає формату '
                              'РРРР-ММ-ДД\n')
                else:
                    print('Введена валюта не відповідає формату CCC\n')
            elif int(action) == 3:
                in_menu = False
            else:
                print('Введене значення не є дією із списку')
        except ValueError:
            print(ValueError('Введене значення не є цифрою'))
    print('До зустрічі!')


if __name__ == "__main__":
    main()
