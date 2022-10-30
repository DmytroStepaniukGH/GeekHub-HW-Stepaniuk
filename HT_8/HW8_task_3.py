"""
3. Програма-банкомат.
   Використовуючи функції створити програму з наступним функціоналом:
      - підтримка 3-4 користувачів, які валідуються парою ім'я/пароль
        (файл <users.CSV>);
      - кожен з користувачів має свій поточний баланс
        (файл <{username}_balance.TXT>) та історію транзакцій
        (файл <{username_transactions.JSON>);
      - є можливість як вносити гроші, так і знімати їх. Обов'язкова
        перевірка введених даних (введено цифри; знімається не більше,
        ніж є на рахунку і т.д.).
   Особливості реалізації:
      - файл з балансом - оновлюється кожен раз при зміні балансу (містить
        просто цифру з балансом);
      - файл - транзакціями - кожна транзакція у вигляді JSON рядка
        додається в кінець файла;
      - файл з користувачами: тільки читається. Але якщо захочете
        реалізувати функціонал додавання нового користувача - не стримуйте
        себе :)
   Особливості функціонала:
      - за кожен функціонал відповідає окрема функція;
      - основна функція - <start()> - буде в собі містити весь workflow
        банкомата:
      - на початку роботи - логін користувача (програма запитує
        ім'я/пароль).
        Якщо вони неправильні - вивести повідомлення про це і закінчити
        роботу (хочете - зробіть 3 спроби, а потім вже закінчити роботу -
        все на ентузіазмі :))
      - потім - елементарне меню типн:
        Введіть дію:
           1. Подивитись баланс
           2. Поповнити баланс
           3. Вихід
      - далі - фантазія і креатив, можете розширювати функціонал, але
        основне завдання має бути повністю реалізоване :)
    P.S. Увага! Файли мають бути саме вказаних форматів (csv, txt, json
        відповідно)
    P.S.S. Добре продумайте структуру програми та функцій
"""
import csv
from datetime import datetime
import json
from colorama import init, Fore
from colorama import Back
from colorama import Style


def auth(user_login, user_password):
    with open('users.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        database = []
        for row in reader:
            database.append(dict(username=row['login'],
                                 password=row['password'], ))

    logged = False
    for row in database:
        if row['username'] == user_login and \
                row['password'] == user_password:
            logged = True
            print(Fore.GREEN + '\nАвторизація успішна\n')

    return logged


def view_balance(user):
    with open(user + '_balance.txt', 'r', encoding='utf-8') as f:
        print(Fore.GREEN + f'На Вашому балансі: {f.read()} грн.\n')


def deposit_funds(user, deposit):
    with open(user + '_balance.txt', 'r+', encoding='utf-8') as f:
        current_balance = f.readline()
        new_balance = float(float(current_balance) + float(deposit))
        f.seek(0)
        f.truncate(0)
        f.write(str(new_balance))

        print(Fore.GREEN + f'Баланс успішно поповнений на {deposit} грн.\n')


def withdraw_funds(user, withdraw):
    with open(user + '_balance.txt', 'r+', encoding='utf-8') as f:
        current_balance = f.readline()
        new_balance = float(float(current_balance) - float(withdraw))
        if new_balance >= 0:
            f.seek(0)
            f.truncate(0)
            f.write(str(new_balance))
            print(Fore.GREEN + f'Успішне зняття {withdraw} грн.\n')
            return True
        else:
            print(Fore.RED + 'На вашому балансі недостатньо коштів для '
                             'здійснення даної операції\n\n')
            return False


def transaction_history(user):
    with open(user + '_transactions.json', 'r', encoding='utf-8') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        json_data = file_data["transactions"]
        print(Fore.GREEN + 'Ваша історія операцій: ')
        if len(json_data) > 0:
            for x in json_data:
                for value in x.values():
                    print(value)
                print('\n')
        else:
            print('Ще немає транзакцій\n')


def get_current_date_time():
    now = datetime.now()
    return now.strftime("%d/%m/%Y %H:%M:%S")


def write_json(new_data, filename):
    with open(filename, 'r+', encoding='utf-8') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data["transactions"].append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent=4, ensure_ascii=False)


def add_transaction(user, transaction):
    new_transaction = {"date": get_current_date_time(),
                       "transaction": transaction
                       }
    write_json(new_transaction, user + '_transactions.json')


def start():
    print(Fore.MAGENTA + 'Ласково просимо до банкомату!')
    login = input(Fore.CYAN + 'Введіть логін: ')
    password = input('Введіть пароль: ')
    init(autoreset=True)
    in_action = True
    if auth(login, password):
        while in_action:
            action = input(Fore.BLUE+'Введіть дію:\n  '
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
                    deposit_value = float(input('Введіть суму для поповнення: '))
                    deposit_funds(login, deposit_value)
                    add_transaction(login, f"Поповнення на суму {deposit_value} грн")
                elif int(action) == 3:
                    withdraw_value = float(input('Введіть суму для зняття: '))
                    if withdraw_funds(login, withdraw_value):
                        add_transaction(login, f"Зняття {withdraw_value} грн")
                elif int(action) == 4:
                    transaction_history(login)
                elif int(action) == 5:
                    in_action = False
                else:
                    print('Введене значення не є дією із списку')
            except ValueError:
                print(ValueError('Введене значення не є цифрою'))

        print(Fore.GREEN + 'До зустрічі!')
    else:
        print(Fore.RED + '\nПомилка авторизації. Введені дані невірні')


if __name__ == "__main__":
    start()
