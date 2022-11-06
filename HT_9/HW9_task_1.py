"""
Банкомат 2.0
    - усі дані зберігаються тільки в sqlite3 базі даних у відповідних
      таблицях. Більше ніяких файлів. Якщо в попередньому завданні ви добре
      продумали структуру програми то у вас не виникне проблем швидко
      адаптувати її до нових вимог.
    - на старті додати можливість залогінитися або створити нового
      користувача (при створенні нового користувача, перевіряється
      відповідність логіну і паролю мінімальним вимогам. Для перевірки
      створіть окремі функції)
    - в таблиці з користувачами також має бути створений унікальний
      користувач-інкасатор, який матиме розширені можливості (домовимось,
      що логін/пароль будуть admin/admin щоб нам було простіше перевіряти)
    - банкомат має власний баланс
    - кількість купюр в банкоматі обмежена (тобто має зберігатися номінал
      та кількість). Номінали купюр - 10, 20, 50, 100, 200, 500, 1000
    - змінювати вручну кількість купюр або подивитися їх залишок в
      банкоматі може лише інкасатор
    - користувач через банкомат може покласти на рахунок лише суму кратну
      мінімальному номіналу що підтримує банкомат. В іншому випадку -
      повернути "здачу" (наприклад при поклажі 1005 --> повернути 5). Але
      це не має впливати на баланс/кількість купюр банкомату, лише
      збільшується баланс користувача (моделюємо наявність двох незалежних
      касет в банкоматі - одна на прийом, інша на видачу)
    - зняти можна лише в межах власного балансу, але не більше ніж є всього
      в банкоматі.
    - при неможливості виконання якоїсь операції - вивести повідомлення з
      причиною (невірний логін/пароль, недостатньо коштів на рахунку,
      неможливо видати суму наявними купюрами тощо.)
    - файл бази даних з усіма створеними таблицями і даними також додайте в
      репозиторій, що б ми могли його використати
"""
import sqlite3
import re
from datetime import datetime
from colorama import init, Fore


def auth(user_login, user_password):
    conn = sqlite3.connect("bankomat.db")
    cur = conn.cursor()
    cur.execute("SELECT user_id FROM Users WHERE login=? and password=?", (user_login, user_password))

    row = cur.fetchone()
    conn.close()
    logged = False

    if row is not None:
        logged = True

    return logged


def create_user(login, password):
    conn = sqlite3.connect("bankomat.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO Users (login, password, balance, is_collector) VALUES (?,?,?,?)",
                (login, password, 0, False))
    conn.commit()
    conn.close()


def view_balance(user):
    conn = sqlite3.connect("bankomat.db")
    cur = conn.cursor()
    cur.execute("SELECT balance FROM Users WHERE login=?", (user,))

    row = cur.fetchone()
    conn.close()
    print(Fore.GREEN + f'На Вашому балансі: {row[0]} грн.\n')


def deposit_funds(user, deposit):
    if deposit > 0:
        conn = sqlite3.connect("bankomat.db")
        cur = conn.cursor()
        cur.execute("SELECT balance FROM Users WHERE login=?", (user,))
        row = cur.fetchone()

        current_balance = row[0]
        new_balance = current_balance + int(deposit)
        cur.execute("UPDATE Users SET balance=? WHERE login=?", (new_balance, user))
        conn.commit()

        conn.close()
        print(Fore.GREEN + f'Баланс успішно поповнений на {deposit} грн.\n')
        add_transaction(user, f"Поповнення на суму {deposit} грн")
    else:
        print(Fore.RED + 'Поповнення можливе лише на суму, більшу за 0 грн\n')


def withdraw_funds(user, withdraw):
    if withdraw > 0:
        conn = sqlite3.connect("bankomat.db")
        cur = conn.cursor()
        cur.execute("SELECT balance FROM Users WHERE login=?", (user,))
        row = cur.fetchone()
        current_balance = row[0]
        new_balance = current_balance - int(withdraw)
        if new_balance >= 0:
            cur.execute("UPDATE Users SET balance=? WHERE login=?", (new_balance, user))
            conn.commit()
            print(Fore.GREEN + f'Успішне зняття {withdraw} грн.\n')
            conn.close()
            add_transaction(user, f"Зняття {withdraw} грн")
        else:
            conn.close()
            print(Fore.RED + 'На вашому балансі недостатньо коштів для '
                             'здійснення даної операції\n\n')
    else:
        print(Fore.RED + 'Сума зняття має бути більша за нуль\n')


def get_current_date_time():
    now = datetime.now()
    return now.strftime("%d/%m/%Y %H:%M:%S")


def add_transaction(user, transaction):
    conn = sqlite3.connect("bankomat.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO Transactions (user, date, transaction_desc) VALUES (?,?,?)",
                (user, get_current_date_time(), transaction))
    conn.commit()
    conn.close()


def transaction_history(user):
    conn = sqlite3.connect("bankomat.db")
    cur = conn.cursor()
    cur.execute("SELECT date, transaction_desc FROM Transactions WHERE user=?", (user,))

    row = cur.fetchall()
    conn.close()
    print(Fore.GREEN + 'Ваша історія операцій: ')
    if len(row) > 0:
        for x in row:
            print(f'{x[0]} - {x[1]}')
    else:
        print('Ще немає транзакцій')

    print('\n')


def is_collector(user):
    conn = sqlite3.connect("bankomat.db")
    cur = conn.cursor()
    cur.execute("SELECT is_collector FROM Users WHERE login=?", (user,))
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
                view_balance(login)
            elif int(action) == 2:
                deposit_value = int(input('Введіть суму для поповнення: '))
                deposit_funds(login, deposit_value)
            elif int(action) == 3:
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
    print("Odmen")


def start():
    print(Fore.MAGENTA + 'Ласково просимо до банкомату!')
    login = input(Fore.CYAN + 'Введіть логін: ')
    password = input('Введіть пароль: ')
    init(autoreset=True)
    in_menu = True

    if auth(login, password) and not is_collector(login):
        print(Fore.GREEN + '\nАвторизація успішна\n')
        start_user(login)
        print(Fore.GREEN + 'До зустрічі!')

    elif auth(login, password) and is_collector(login):
        print(Fore.GREEN + '\nАвторизація успішна\n')
        start_collector(login)
        print(Fore.GREEN + 'До зустрічі!')

    else:
        print(Fore.RED + '\nПомилка авторизації. Введені дані невірні')
        while in_menu:
            action = input(('Оберіть наступну дію:\n'
                            '1 - Створити нового користувача\n'
                            '2 - Вихід з банкомату\n'
                            'Ваша дія: '))
            try:
                if int(action) == 1:
                    print('Реєстрація нового користувача\n'
                          'Підказка: логін користувача має бути від 4 до '
                          '20 символів латинського алфівіту. Пароль від 4 '
                          'до 20 символів латинського алфавіту, а також має'
                          ' містити хоча б одну цифру\n')
                    new_login = input('Придумайте логін: ')
                    new_password = input('Придумайте пароль: ')
                    if validate(new_login, new_password) == 'OK':
                        create_user(login, password)
                        print(Fore.GREEN + '\nАвторизація успішна\n')
                        start_user(login)
                        print(Fore.GREEN + '\nДо зустрічі!')
                        in_menu = False
                    else:
                        print(validate(new_login, new_password))
                elif int(action) == 2:
                    print(Fore.GREEN + '\nДо зустрічі!')
                    in_menu = False
                else:
                    print(Fore.RED + 'Введене значення не є дією із списку\n')
            except ValueError:
                print(Fore.RED + 'Помилка введеного значення\n')


if __name__ == "__main__":
    start()
    # create_user('test', 'test')
    # print(is_collector('admin'))
