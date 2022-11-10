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


def auth(user_login, user_password):
    conn = sqlite3.connect("bankomat.db")
    cur = conn.cursor()
    cur.execute("SELECT user_id FROM Users WHERE login=? and password=?",
                (user_login, user_password))

    row = cur.fetchone()
    conn.close()
    logged = False

    if row is not None:
        logged = True

    return logged


def create_user(login, password):
    conn = sqlite3.connect("bankomat.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO Users (login, password, balance, is_collector)"
                " VALUES (?,?,?,?)",
                (login, password, 0, False))
    conn.commit()
    conn.close()


def get_user_balance(user):
    conn = sqlite3.connect("bankomat.db")
    cur = conn.cursor()
    cur.execute("SELECT balance FROM Users WHERE login=?", (user,))

    row = cur.fetchone()
    conn.close()
    return row[0]


def view_denomination_number(denomination):
    valid_denomination = [10, 20, 50, 100, 200, 500, 1000]
    if denomination in valid_denomination:
        conn = sqlite3.connect("bankomat.db")
        cur = conn.cursor()
        cur.execute("SELECT denomination, number FROM Balance "
                    "WHERE denomination=?", (denomination,))
        row = cur.fetchone()
        print(f'Залишок купюр номіналом {denomination} грн становить '
              f'{row[1]} шт.')
    else:
        print(Fore.RED + 'Введене значення не є доступним номіналом '
                         'купюр\n')


def get_balance_atm():
    conn = sqlite3.connect("bankomat.db")
    cur = conn.cursor()
    cur.execute("SELECT denomination, number FROM Balance")
    row = cur.fetchall()
    summ = 0
    for i in row:
        summ += i[0] * i[1]

    return summ


def change_number_bills(denomination, new_number):
    valid_denomination = [10, 20, 50, 100, 200, 500, 1000]
    if denomination in valid_denomination and new_number > 0:
        conn = sqlite3.connect("bankomat.db")
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
            add_transaction('admin', f'Поповнення купюр номіналом '
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
                add_transaction('admin', f'Зняття купюр номіналом '
                                         f'{denomination} грн на '
                                         f'{new_number} шт.')
        else:
            print(Fore.RED + 'Введена дія не є дією зі списку\n')

        conn.close()
    else:
        print(Fore.RED + 'Введене значення не є доступним номіналом '
                         'купюр\n')


def deposit_funds(user, deposit):
    if deposit > 0:
        conn = sqlite3.connect("bankomat.db")
        cur = conn.cursor()
        cur.execute("SELECT balance FROM Users WHERE login=?", (user,))
        row = cur.fetchone()

        current_balance = row[0]
        if deposit % 10 == 0:
            new_balance = current_balance + deposit
            cur.execute("UPDATE Users SET balance=? WHERE login=?",
                        (new_balance, user))
            conn.commit()

            conn.close()
            print(Fore.GREEN + f'Баланс успішно поповнений на {deposit} '
                               f'грн.\n')
            add_transaction(user, f"Поповнення на суму {deposit} грн")
        else:
            new_balance = current_balance + deposit - deposit % 10
            cur.execute("UPDATE Users SET balance=? WHERE login=?",
                        (new_balance, user))
            conn.commit()

            conn.close()
            print(Fore.GREEN + f'Баланс успішно поповнений на {deposit} '
                               f'грн. Повернено решту {deposit % 10} '
                               f'грн\n')
            add_transaction(user, f"Поповнення на суму {deposit} грн та "
                                  f"повернення решти {deposit % 10} грн")
    else:
        print(Fore.RED + 'Поповнення можливе лише на суму, більшу за 0 '
                         'грн\n')


def denomination_set(to_pay):
    conn = sqlite3.connect("bankomat.db")
    cur = conn.cursor()
    cur.execute("SELECT denomination, number FROM Balance")
    row = cur.fetchall()
    conn.commit()

    available_money = {x: y for (x, y) in row}

    combination_denom = {10: 0, 20: 0, 50: 0, 100: 0, 200: 0, 500: 0,
                         1000: 0}
    amount_to_pay = to_pay
    status = True
    keys = {10: 0, 20: 0, 50: 0, 100: 0, 200: 0, 500: 0, 1000: 0}

    while amount_to_pay != 0:
        if sum(available_money.values()) != 0:

            if amount_to_pay >= 1000 and available_money[1000] > 0:
                available_count = available_money[1000]
                count = amount_to_pay // 1000
                count_to_write = count if count <= available_count \
                    else available_count

                combination_denom[1000] = count_to_write
                available_money[1000] = available_count - count_to_write
                amount_to_pay -= count_to_write * 1000

            elif amount_to_pay >= 500 and available_money[500] > 0:
                available_count = available_money[500]
                count = amount_to_pay // 500
                count_to_write = count if count <= available_count \
                    else available_count
                combination_denom[500] = count_to_write
                available_money[500] = available_count - count_to_write
                amount_to_pay -= count_to_write * 500

            elif amount_to_pay >= 200 and available_money[200] > 0:
                available_count = available_money[200]
                count = amount_to_pay // 200
                count_to_write = count if count <= available_count \
                    else available_count
                combination_denom[200] = count_to_write
                available_money[200] = available_count - count_to_write
                amount_to_pay -= count_to_write * 200

            elif amount_to_pay >= 100 and available_money[100] > 0:
                available_count = available_money[100]
                count = amount_to_pay // 100
                count_to_write = count if count <= available_count \
                    else available_count
                combination_denom[100] = count_to_write
                available_money[100] = available_count - count_to_write
                amount_to_pay -= count_to_write * 100

            elif amount_to_pay >= 50 and available_money[50] > 0:
                available_count = available_money[50]
                count = amount_to_pay // 50
                count_to_write = count if count <= available_count \
                    else available_count
                combination_denom[50] = count_to_write
                available_money[50] = available_count - count_to_write
                amount_to_pay -= count_to_write * 50

            elif amount_to_pay >= 20 and available_money[20] > 0:
                available_count = available_money[20]
                count = amount_to_pay // 20
                count_to_write = count if count <= available_count \
                    else available_count
                combination_denom[20] = count_to_write
                available_money[20] = available_count - count_to_write
                amount_to_pay -= count_to_write * 20

            elif amount_to_pay >= 10 and available_money[10] > 0:
                available_count = available_money[10]
                count = amount_to_pay // 10
                count_to_write = count if count <= available_count \
                    else available_count
                combination_denom[10] = count_to_write
                available_money[10] -= count_to_write
                amount_to_pay -= count_to_write * 10

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

                combination_denom = {10: 0, 20: 0, 50: 0, 100: 0, 200: 0,
                                     500: 0, 1000: 0}
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


def withdraw_funds(user, withdraw):
    if withdraw > 0:
        if withdraw % 10 == 0:
            if get_balance_atm() - withdraw >= 0:
                conn = sqlite3.connect("bankomat.db")
                cur = conn.cursor()
                cur.execute("SELECT balance FROM Users WHERE login=?",
                            (user,))
                row = cur.fetchone()
                current_balance = row[0]
                new_balance = current_balance - withdraw
                combination = denomination_set(withdraw)
                if new_balance >= 0 and combination:
                    cur.execute("UPDATE Users SET balance=? WHERE login=?",
                                (new_balance, user))
                    conn.commit()

                    print(Fore.GREEN + f'Успішне зняття {withdraw} грн.\n')
                    print('Отримайте Ваші кошти')

                    for key, num in \
                            dict(reversed(combination.items())).items():
                        if num != 0:
                            print(f'Номінал купюри: {key} -> {num} шт.')

                    print('\n')

                    conn.close()
                    add_transaction(user, f"Зняття {withdraw} грн")

                else:
                    conn.close()
                    if new_balance < 0:
                        print(Fore.RED +
                              'На вашому балансі недостатньо коштів для '
                              'здійснення даної операції\n\n')
                    elif not denomination_set(withdraw):
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


def get_current_date_time():
    now = datetime.now()
    return now.strftime("%d/%m/%Y %H:%M:%S")


def add_transaction(user, transaction):
    conn = sqlite3.connect("bankomat.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO Transactions (user, date, transaction_desc) "
                "VALUES (?,?,?)",
                (user, get_current_date_time(), transaction))
    conn.commit()
    conn.close()


def all_transactions():
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


def transaction_history(user):
    conn = sqlite3.connect("bankomat.db")
    cur = conn.cursor()
    cur.execute("SELECT date, transaction_desc FROM Transactions WHERE "
                "user=?", (user,))

    row = cur.fetchall()
    conn.close()
    print(Fore.GREEN + 'Ваша історія операцій: ')
    if len(row) > 0:
        for x in row:
            print(f'{x[0]} - {x[1]}')
    else:
        print('Ще немає транзакцій')

    print('\n')


def view_all_denomination():
    conn = sqlite3.connect("bankomat.db")
    cur = conn.cursor()
    cur.execute("SELECT denomination, number FROM Balance")

    row = cur.fetchall()
    conn.close()
    print(Fore.GREEN + 'Номінали купюр та їх кількість в банкоматі: ')
    for x in row:
        print(f'{x[0]} - {x[1]}')

    print('\n')


def get_available_denomination():
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


def is_collector(user):
    conn = sqlite3.connect("bankomat.db")
    cur = conn.cursor()
    cur.execute("SELECT is_collector FROM Users WHERE login=?",
                (user,))
    row = cur.fetchone()
    conn.close()

    return True if row[0] else False


def validate(login, password):
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


def start_user(login):
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
                                   f'{get_user_balance(login)} грн.\n')
            elif int(action) == 2:
                deposit_value = int(input('Введіть суму для поповнення: '))
                deposit_funds(login, deposit_value)
            elif int(action) == 3:
                print(Fore.GREEN + get_available_denomination())
                withdraw_value = int(input('Введіть суму для зняття: '))
                withdraw_funds(login, withdraw_value)
            elif int(action) == 4:
                transaction_history(login)
            elif int(action) == 5:
                in_action = False
            else:
                print('Введене значення не є дією із списку')
        except ValueError:
            print(ValueError('Введене значення не є цифрою'))


def start_collector(login):
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
                print(f'Баланс банкомату: {get_balance_atm()} грн\n')
            elif int(action) == 2:
                denomination = int(input('Введіть номінал купюри: '))
                view_denomination_number(denomination)
            elif int(action) == 3:
                view_all_denomination()
            elif int(action) == 4:
                denomination_to_change = int(input('Введіть номінал купюри '
                                                   'для зміни: '))
                value_to_change = int(input('Введіть кількість купюр '
                                            'для зміни: '))
                change_number_bills(denomination_to_change, value_to_change)
            elif int(action) == 5:
                transaction_history(login)
            elif int(action) == 6:
                all_transactions()
            elif int(action) == 7:
                in_action = False
            else:
                print('Введене значення не є дією із списку')
        except ValueError:
            print(ValueError('Введене значення не є цифрою'))


def reg_user():
    print(Fore.BLUE +
          'Реєстрація нового користувача\n'
          'Підказка: логін користувача має бути від 4 до'
          ' 20 латинських символів.\nПароль від 4 до 20 '
          'символів, має містити латинські символи та '
          'цифри.\n')
    new_login = input('Придумайте логін: ')
    new_password = input('Придумайте пароль: ')

    if validate(new_login, new_password) == 'OK':
        create_user(new_login, new_password)
        print(Fore.GREEN + '\nРеєстрація успішна. Авторизовано.\n')
        start_user(new_login)
    else:
        print(validate(new_login, new_password))


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
                init(autoreset=True)
                in_menu = True

                if auth(login, password) and not is_collector(login):
                    print(Fore.GREEN + '\nАвторизація успішна\n')
                    start_user(login)

                elif auth(login, password) and is_collector(login):
                    print(Fore.GREEN + '\nАвторизація успішна\n')
                    start_collector(login)

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
                                reg_user()
                            elif int(action) == 2:
                                in_menu = False
                            else:
                                print(Fore.RED + 'Введене значення не є дією '
                                                 'із списку\n')
                        except ValueError:
                            print(Fore.RED + 'Помилка введеного значення\n')
            elif int(action) == 2:
                reg_user()
            elif int(action) == 3:
                print(Fore.GREEN + '\nДо зустрічі!')
                in_main_menu = False

            else:
                print(Fore.RED + 'Введене значення не є дією із списку\n')
        except ValueError:
            print(Fore.RED + 'Помилка введеного значення\n')


if __name__ == "__main__":
    start()
