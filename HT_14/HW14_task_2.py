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

        if rates:
            print(f'{self.currency} -> UAH')
            print(f'Дата\t\t\tКурс')
            for day in rates:
                print(f'{day[0]}\t\t{day[1]}')
            print('\n')
        else:
            print('Не вдалось отримати інформацію для заданого інтервалу\n')


class Validate:
    @staticmethod
    def validate_format_currency(currency):
        cur_pattern = "^[A-Z]{3}$"
        return re.match(cur_pattern, currency)

    @staticmethod
    def validate_date_format(date):
        date_pattern = "^[0-9]{4}\\-[0-9]{2}\\-[0-9]{2}$"
        return re.match(date_pattern, date)

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

    @staticmethod
    def is_available_key_of_currency(key):
        url = 'https://api.exchangerate.host/symbols'
        response = requests.get(url)
        data = response.json()
        keys = data['symbols'].keys()

        return key in keys


class DataProcessing:
    def __init__(self, currency, start_date, end_date=None):
        self.currency = currency
        self.start_date = start_date
        self.end_date = end_date

    def __check_currency(self):
        status = False
        if not Validate.validate_format_currency(self.currency):
            print('Введена валюта не відповідає формату CCC\n')
        elif not Validate.is_available_key_of_currency(self.currency):
            print('Введений код валюти не підтримується\n')
        else:
            status = True
        return status

    def check_data_for_first_condition(self):
        if self.__check_currency():
            if not Validate.validate_date_format(self.start_date):
                print('Введена дата не відповідає формату РРРР-ММ-ДД\n')

            elif not Validate.validate_current_date(self.start_date):
                print('Введена дата не повинна перевищувати сьогоднішню дату\n')

            else:
                curr_hist = CurrencyHistory(self.currency, self.start_date)
                curr_hist.show_history()

    def check_data_for_second_condition(self):
        if self.__check_currency():
            if not Validate.validate_date_format(self.start_date):
                print('Дата не відповідає формату РРРР-ММ-ДД\n')

            elif not Validate.validate_current_date(self.start_date):
                print('Дата не повинна перевищувати сьогоднішню дату\n')

            elif not Validate.validate_date_format(self.end_date):
                print('Дата не відповідає формату РРРР-ММ-ДД\n')

            elif not Validate.validate_current_date(self.end_date):
                print('Дата не повинна перевищувати сьогоднішню дату\n')

            else:
                curr_hist = CurrencyHistory(self.currency, self.start_date,
                                            self.end_date)
                curr_hist.show_history()


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
                start_date = input('Введіть початкову дату в форматі '
                                   'РРРР-ММ-ДД (наприклад, 2022-11-20): ')
                new_check = DataProcessing(currency, start_date)
                new_check.check_data_for_first_condition()

            elif int(action) == 2:
                currency = input('Введіть код необхідної валюти '
                                 '(USD, EUR, CZK і т.д.): ')
                start_date = input('Введіть початкову дату в форматі '
                                   'РРРР-ММ-ДД (наприклад, 2022-11-20): ')
                end_date = input('Введіть кінцеву дату в форматі '
                                 'РРРР-ММ-ДД (наприклад, 2022-11-20): ')

                new_check = DataProcessing(currency, start_date, end_date)
                new_check.check_data_for_second_condition()

            elif int(action) == 3:
                in_menu = False
            else:
                print('Введене значення не є дією із списку')
        except ValueError:
            print(ValueError('Помилка введеного значення\n'))
    print('До зустрічі!')


if __name__ == "__main__":
    main()
