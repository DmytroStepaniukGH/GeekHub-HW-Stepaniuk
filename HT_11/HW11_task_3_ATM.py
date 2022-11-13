"""
Банкомат 3.0
    - реалізуйте видачу купюр за логікою видавання найменшої кількості
      купюр, але в межах наявних в банкоматі. Наприклад: 2560 --> 2х1000,
      1х500, 3х20. Будьте обережні з "жадібним алгоритмом"! Видані купюри
      також мають бути “вилучені” з банкомату. Тобто якщо до операції в
      банкоматі було 5х1000, 5х500, 5х20 - має стати 3х1000, 4х500, 2х20.
    - як і раніше, поповнення балансу користувача не впливає на кількість
      купюр. Їх кількість може змінювати лише інкасатор.
    - обов’язкова реалізація таких дій (назви можете використовувати свої):
    При запускі
    Вхід
    Реєстрація (з перевіркою валідності/складності введених даних)
    Вихід
    Для користувача
    Баланс
    Поповнення
    Зняття
    Історія транзакцій
    Вихід на стартове меню
    Для інкасатора
    Наявні купюри/баланс тощо
    Зміна кількості купюр
    Повна історія операцій по банкомату (дії всіх користувачів та інкасаторів)
    Вихід на стартове меню
    - обов’язкове дотримання РЕР8 (якщо самостійно ніяк,
      то https://flake8.pycqa.org/en/latest/ вам в допомогу)
    - (опціонально) не лініться і придумайте якусь свою особливу
      фішку/додатковий
      функціонал, але при умові що основне завдання виконане
"""
import sqlite3
import re
from datetime import datetime
from colorama import init, Fore


class Atm:
    def __init__(self, login=None, password=None):
        self.login = login
        self.password = password

    def create_connection(self):
        conn = sqlite3.connect("bankomat.db")
        return conn

    def auth(self):
        conn = self.create_connection()
        cur = conn.cursor()
        cur.execute("SELECT user_id FROM Users WHERE login=? and password=?",
                    (self.login, self.password))

        row = cur.fetchone()
        conn.close()
        logged = False

        if row is not None:
            logged = True

        return logged

    def create_user(self, new_login, new_password):
        conn = self.create_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO Users (login, password, balance, is_collector)"
                    " VALUES (?,?,?,?)",
                    (new_login, new_password, 0, False))
        conn.commit()
        conn.close()

    def get_user_balance(self):
        conn = self.create_connection()
        cur = conn.cursor()
        cur.execute("SELECT balance FROM Users WHERE login=?", (self.login,))

        row = cur.fetchone()
        conn.close()
        return row[0]

    def view_denomination_number(self, denomination):
        valid_denomination = [10, 20, 50, 100, 200, 500, 1000]
        if denomination in valid_denomination:
            conn = self.create_connection()
            cur = conn.cursor()
            cur.execute("SELECT denomination, number FROM Balance "
                        "WHERE denomination=?", (denomination,))
            row = cur.fetchone()
            conn.close()
            print(f'Залишок купюр номіналом {denomination} грн становить '
                  f'{row[1]} шт.')
        else:
            print(Fore.RED + 'Введене значення не є доступним номіналом '
                             'купюр\n')

    def get_balance_atm(self):
        conn = self.create_connection()
        cur = conn.cursor()
        cur.execute("SELECT denomination, number FROM Balance")
        row = cur.fetchall()
        summ = 0
        for i in row:
            summ += i[0] * i[1]

        return summ

    def change_number_bills(self, denomination, new_number):
        valid_denomination = [10, 20, 50, 100, 200, 500, 1000]
        if denomination in valid_denomination and new_number > 0:
            conn = self.create_connection()
            cur = conn.cursor()
            cur.execute("SELECT denomination, number FROM Balance WHERE "
                        "denomination=?", (denomination,))
            row = cur.fetchone()
            current_number = row[1]
            action = int(input('Виберіть дію: \n'
                               '1 - Поповнити кількість купюр\n'
                               '2 - Зняти кількість купюр\n'
                               'Ваша дія: '))
            if action == 1:
                cur.execute("UPDATE Balance SET number=? WHERE denomination=?",
                            (current_number + new_number, denomination,))
                conn.commit()
                print(Fore.GREEN + 'Кількість купюр успішно змінена\n')
                self.add_transaction(f'Поповнення купюр номіналом '
                                     f'{denomination} грн на '
                                     f'{new_number} шт.')
            elif action == 2:
                if current_number - new_number < 0:
                    print(Fore.RED + 'Неможливо зняти більшу кількість купюр, '
                                     'аніж доступно в банкоматі\n')
                else:
                    cur.execute("UPDATE Balance SET number=? WHERE "
                                "denomination=?",
                                (current_number - new_number, denomination,))
                    conn.commit()
                    print(Fore.GREEN + 'Кількість купюр успішно змінена\n')
                    self.add_transaction(f'Зняття купюр номіналом '
                                         f'{denomination} грн на '
                                         f'{new_number} шт.')
            else:
                print(Fore.RED + 'Введена дія не є дією зі списку\n')

            conn.close()
        else:
            print(Fore.RED + 'Введене значення не є доступним номіналом '
                             'купюр\n')

    def deposit_funds(self, deposit):
        if deposit > 0:
            conn = sqlite3.connect("bankomat.db")
            cur = conn.cursor()
            cur.execute("SELECT balance FROM Users WHERE login=?", (self.login,))
            row = cur.fetchone()

            current_balance = row[0]
            if deposit % 10 == 0:
                new_balance = current_balance + deposit
                cur.execute("UPDATE Users SET balance=? WHERE login=?",
                            (new_balance, self.login))
                conn.commit()

                conn.close()
                print(Fore.GREEN + f'Баланс успішно поповнений на {deposit} '
                                   f'грн.\n')
                self.add_transaction(f'Поповнення на суму {deposit} грн')
            else:
                new_balance = current_balance + deposit - deposit % 10
                cur.execute("UPDATE Users SET balance=? WHERE login=?",
                            (new_balance, self.login))
                conn.commit()

                conn.close()
                print(Fore.GREEN + f'Баланс успішно поповнений на {deposit} '
                                   f'грн. Повернено решту {deposit % 10} '
                                   f'грн\n')
                self.add_transaction(f'Поповнення на суму {deposit} грн та '
                                     f'повернення решти {deposit % 10} грн')
        else:
            print(Fore.RED + 'Поповнення можливе лише на суму, більшу за 0 '
                             'грн\n')

    def get_count_denomination(self, denomination, combination_denom, available_money,
                               amount_to_pay):
        if amount_to_pay >= denomination and available_money[denomination] > 0:
            available_count = available_money[denomination]
            count = amount_to_pay // denomination
            count_to_write = count if count <= available_count \
                else available_count

            combination_denom[denomination] = count_to_write
            available_money[denomination] = available_count - count_to_write
            amount_to_pay -= count_to_write * denomination

            return combination_denom, available_money, amount_to_pay

    def denomination_set(self, to_pay):
        conn = self.create_connection()
        cur = conn.cursor()
        cur.execute("SELECT denomination, number FROM Balance")
        row = cur.fetchall()
        conn.commit()

        available_money = {x: y for (x, y) in row}
        denominations = [item[0] for item in reversed(row)]
        combination_denom = {item[0]: 0 for item in row}
        keys = {item[0]: 0 for item in row}

        amount_to_pay = to_pay
        status = True

        while amount_to_pay != 0:
            if sum(available_money.values()) != 0:
                for denomination in denominations:
                    items = self.get_count_denomination(denomination,
                                                        combination_denom,
                                                        available_money,
                                                        amount_to_pay)
                    if items:
                        combination_denom = items[0]
                        available_money = items[1]
                        amount_to_pay = items[2]
                        if amount_to_pay == 0:
                            break

                else:
                    for key, num in \
                            dict(reversed(combination_denom.items())).items():
                        if num != 0:
                            key_for_back = key
                            keys[key_for_back] += 1
                            break

                    available_money = {x: y for (x, y) in row}
                    for key, value in keys.items():
                        if available_money[key] > 0:
                            available_money[key] -= value

                    combination_denom = {item[0]: 0 for item in row}
                    amount_to_pay = to_pay

            else:
                status = False
                break

        if status:
            number_bills = tuple(available_money.keys())
            denominations = tuple(available_money.values())

            cur.executemany("UPDATE Balance SET number=? WHERE denomination=?",
                            list(zip(denominations, number_bills)))
            conn.commit()
            conn.close()

            return combination_denom

        else:
            return False

    def withdraw_funds(self, withdraw):
        if withdraw > 0:
            if withdraw % 10 == 0:
                if self.get_balance_atm() - withdraw >= 0:
                    conn = sqlite3.connect("bankomat.db")
                    cur = conn.cursor()
                    cur.execute("SELECT balance FROM Users WHERE login=?",
                                (self.login,))
                    row = cur.fetchone()
                    current_balance = row[0]
                    new_balance = current_balance - withdraw
                    combination = self.denomination_set(withdraw)
                    if new_balance >= 0 and combination:
                        cur.execute("UPDATE Users SET balance=? WHERE login=?",
                                    (new_balance, self.login))
                        conn.commit()

                        print(Fore.GREEN + f'Успішне зняття {withdraw} грн.\n')
                        print('Отримайте Ваші кошти')

                        for key, num in \
                                dict(reversed(combination.items())).items():
                            if num != 0:
                                print(f'Номінал купюри: {key} -> {num} шт.')

                        print('\n')

                        conn.close()
                        self.add_transaction(f'Зняття {withdraw} грн')

                    else:
                        conn.close()
                        if new_balance < 0:
                            print(Fore.RED +
                                  'На вашому балансі недостатньо коштів для '
                                  'здійснення даної операції\n\n')
                        elif not combination:
                            print('Нажаль, з наявних купюр сформувати дану '
                                  'суму зняття неможливо. Будь ласка, спробуйте '
                                  'іншу суму.')
                else:
                    print(Fore.RED + 'Нажаль, сума зняття перевищує баланс '
                                     'банкомату. '
                                     'Будь ласка, спробуйте меншу суму.\n')
            else:
                print('Сума зняття має бути кратна десяти')
        else:
            print(Fore.RED + 'Сума зняття має бути більша за нуль\n')

    def get_current_date_time(self):
        now = datetime.now()
        return now.strftime("%d/%m/%Y %H:%M:%S")

    def add_transaction(self, transaction):
        conn = self.create_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO Transactions (user, date, transaction_desc) "
                    "VALUES (?,?,?)",
                    (self.login, self.get_current_date_time(), transaction))
        conn.commit()
        conn.close()

    def all_transactions(self):
        conn = sqlite3.connect("bankomat.db")
        cur = conn.cursor()
        cur.execute("SELECT date, user, transaction_desc FROM Transactions")

        row = cur.fetchall()
        conn.close()
        print(Fore.GREEN + 'Вся історія транзакцій банкомату: ')
        if len(row) > 0:
            for x in row:
                print(f'{x[0]} {x[1]} - {x[2]}')
        else:
            print('Ще немає транзакцій')

        print('\n')

    def transaction_history(self):
        conn = sqlite3.connect("bankomat.db")
        cur = conn.cursor()
        cur.execute("SELECT date, transaction_desc FROM Transactions WHERE "
                    "user=?", (self.login,))

        row = cur.fetchall()
        conn.close()
        print(Fore.GREEN + 'Ваша історія операцій: ')
        if len(row) > 0:
            for x in row:
                print(f'{x[0]} - {x[1]}')
        else:
            print('Ще немає транзакцій')

        print('\n')

    def view_all_denomination(self):
        conn = sqlite3.connect("bankomat.db")
        cur = conn.cursor()
        cur.execute("SELECT denomination, number FROM Balance")

        row = cur.fetchall()
        conn.close()
        print(Fore.GREEN + 'Номінали купюр та їх кількість в банкоматі: ')
        for x in row:
            print(f'{x[0]} - {x[1]}')

        print('\n')

    def get_available_denomination(self):
        conn = sqlite3.connect("bankomat.db")
        cur = conn.cursor()
        cur.execute("SELECT denomination, number FROM Balance"
                    " WHERE number > 0")
        s = 'Доступні купюри для зняття: '
        row = cur.fetchall()
        conn.close()
        for i in row:
            s += f'{i[0]}, '

        return s[:-2]

    def is_collector(self):
        conn = sqlite3.connect("bankomat.db")
        cur = conn.cursor()
        cur.execute("SELECT is_collector FROM Users WHERE login=?",
                    (self.login,))
        row = cur.fetchone()
        conn.close()

        return True if row[0] else False

    def validate(self, login, password):
        general_pattern = re.compile('^[0-9a-zA-Z]+$')
        char = re.compile('[A-Za-z]')
        number = re.compile('[0-9]')
        errors = ''

        try:
            re.search(general_pattern, login).group()
            re.search(general_pattern, password).group()
        except AttributeError:
            return AttributeError('Введені символи не можуть бути використані'
                                  ' в якості логіна/пароля.\n'
                                  'Для логіна допустимі лише латинські символи.\n'
                                  'Для пароля - латинськы символи та цифри')
        else:
            if not char.search(login):
                errors += 'Логін має складатись лише з латинських сиволів.\n'
            if len(login) not in range(4, 21):
                errors += 'Довжина логіна має бути від 4 до 50 символів.\n'
            if not char.search(password):
                errors += 'Пароль має містити латинські сиволи.\n'
            if not number.search(password):
                errors += 'Пароль має містити цифри.\n'
            if len(password) not in range(4, 21):
                errors += 'Пароль має бути від 4 до 20 символів\n'

            return 'OK' if len(errors) == 0 else f'{errors}'

    def reg_user(self):
        print(Fore.BLUE +
              'Реєстрація нового користувача\n'
              'Підказка: логін користувача має бути від 4 до'
              ' 20 латинських символів.\nПароль від 4 до 20 '
              'символів, має містити латинські символи та '
              'цифри.\n')
        new_login = input('Придумайте логін: ')
        new_password = input('Придумайте пароль: ')

        if self.validate(new_login, new_password) == 'OK':
            self.create_user(new_login, new_password)
            print(Fore.GREEN + '\nРеєстрація успішна. Авторизовано.\n')
            new_user = StartUser(new_login, new_password)
            new_user.user_menu()
        else:
            print(self.validate(new_login, new_password))


class StartUser:
    def __init__(self, login, password):
        self.user = Atm(login, password)

    def user_menu(self):
        in_action = True

        while in_action:
            action = input(Fore.BLUE + 'Введіть дію:\n  '
                                       '1. Переглянути баланс\n  '
                                       '2. Поповнити баланс\n  '
                                       '3. Зняти кошти\n  '
                                       '4. Переглянути історію операцій\n  '
                                       '5. Вихід\n  '
                                       'Ваша дія: ')
            print('\n')
            try:
                if int(action) == 1:
                    print(Fore.GREEN + f'На Вашому балансі: '
                                       f'{self.user.get_user_balance()} грн.\n')
                elif int(action) == 2:
                    deposit_value = int(input('Введіть суму для поповнення: '))
                    self.user.deposit_funds(deposit_value)
                elif int(action) == 3:
                    print(Fore.GREEN + self.user.get_available_denomination())
                    withdraw_value = int(input('Введіть суму для зняття: '))
                    self.user.withdraw_funds(withdraw_value)
                elif int(action) == 4:
                    self.user.transaction_history()
                elif int(action) == 5:
                    in_action = False
                else:
                    print('Введене значення не є дією із списку')
            except ValueError:
                print(ValueError('Введене значення не є цифрою'))

    def collector_menu(self):
        in_action = True

        while in_action:
            action = input(Fore.BLUE + 'Введіть дію:\n  '
                                       '1. Переглянути баланс банкомату\n  '
                                       '2. Переглянути кількість купюр певного'
                                       ' номіналу\n  '
                                       '3. Переглянути всі доступні купюри\n  '
                                       '4. Змінити кількість купюр\n  '
                                       '5. Переглянути транзакції інкасатора\n  '
                                       '6. Переглянути всі транзакції '
                                       'банкомату\n  '
                                       '7. Вихід\n  '
                                       'Ваша дія: ')
            print('\n')
            try:
                if int(action) == 1:
                    print(f'Баланс банкомату: {self.user.get_balance_atm()} грн\n')
                elif int(action) == 2:
                    denomination = int(input('Введіть номінал купюри: '))
                    self.user.view_denomination_number(denomination)
                elif int(action) == 3:
                    self.user.view_all_denomination()
                elif int(action) == 4:
                    denomination_to_change = int(input('Введіть номінал купюри '
                                                       'для зміни: '))
                    value_to_change = int(input('Введіть кількість купюр '
                                                'для зміни: '))
                    self.user.change_number_bills(denomination_to_change, value_to_change)
                elif int(action) == 5:
                    self.user.transaction_history()
                elif int(action) == 6:
                    self.user.all_transactions()
                elif int(action) == 7:
                    in_action = False
                else:
                    print('Введене значення не є дією із списку')
            except ValueError:
                print(ValueError('Введене значення не є цифрою'))


def start():
    print(Fore.MAGENTA + 'Ласково просимо до банкомату!')
    init(autoreset=True)
    in_main_menu = True

    while in_main_menu:
        action = input(('Оберіть наступну дію:\n'
                        '1 - Вхід\n'
                        '2 - Реєстрація\n'
                        '3 - Вихід\n'
                        'Ваша дія: '))
        try:
            if int(action) == 1:
                login = input('Введіть логін: ')
                password = input('Введіть пароль: ')
                new_session = Atm(login, password)
                init(autoreset=True)
                in_menu = True

                if new_session.auth() and not new_session.is_collector():
                    print(Fore.GREEN + '\nАвторизація успішна\n')
                    user = StartUser(login, password)
                    user.user_menu()

                elif new_session.auth() and new_session.is_collector():
                    print(Fore.GREEN + '\nАвторизація успішна\n')
                    user = StartUser(login, password)
                    user.collector_menu()

                else:
                    print(Fore.RED + '\nПомилка авторизації. Введені дані '
                                     'невірні\n')
                    while in_menu:
                        action = input(('Оберіть наступну дію:\n'
                                        '1 - Створити нового користувача\n'
                                        '2 - Вихід з банкомату\n'
                                        'Ваша дія: '))
                        try:
                            if int(action) == 1:
                                new_session.reg_user()
                            elif int(action) == 2:
                                in_menu = False
                            else:
                                print(Fore.RED + 'Введене значення не є дією '
                                                 'із списку\n')
                        except ValueError:
                            print(Fore.RED + 'Помилка введеного значення\n')
            elif int(action) == 2:
                new_session = Atm()
                new_session.reg_user()
            elif int(action) == 3:
                print(Fore.GREEN + '\nДо зустрічі!')
                in_main_menu = False

            else:
                print(Fore.RED + 'Введене значення не є дією із списку\n')
        except ValueError:
            print(Fore.RED + 'Помилка введеного значення\n')


if __name__ == "__main__":
    start()
