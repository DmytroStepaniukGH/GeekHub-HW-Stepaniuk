"""
2. Створіть 3 рiзних функцiї (на ваш вибiр). Кожна з цих функцiй повинна
   повертати якийсь результат (напр. інпут від юзера, результат
   математичної операції тощо). Також створiть четверту ф-цiю, яка
   всередині викликає 3 попередні, обробляє їх результат та також повертає
   результат своєї роботи. Таким чином ми будемо викликати одну (четверту)
   функцiю, а вона в своєму тiлi - ще 3.
"""
import re


def create_uppercase(name: str) -> str:
    """
    The function accepts a string containing first name and return the
    uppercase string
    """
    try:
        filter(None, re.match('^[A-Za-z]*$', name).groups())
    except AttributeError:
        return False
    else:
        return name if name.isupper() else name.upper()


def calc_balance(balance: float, exchange_rate: float) -> float:
    """
    The function takes two real numbers: the user's balance and the bitcoin
    exchange rate and returns the result in the currency of the exchange
    rate in UAN
    """
    try:
        return round(float(balance) * float(exchange_rate), 2)
    except ValueError:
        return False


def convert_to_usd(value: float) -> float:
    """
    The function accepts two values: the balance in UAN
    and returns the balance in USD
    """
    try:
        return round(float(value) / 36.57, 2)
    except ValueError as err:
        return False


def create_output():
    name = input("Input your name in English: ")
    balance = input("Input your balance in BTC: ")
    ex_rate_btc_to_uan = input('Input exchange rate of BTC to UAN: ')

    if not create_uppercase(name):
        print(f'Error: {name} - is not a number or contains '
              f'non-English characters')
    elif not calc_balance(balance, ex_rate_btc_to_uan):
        print(f'Error: {balance} or {ex_rate_btc_to_uan} is not a number')
    else:
        print(f'USER {create_uppercase(name)} HAS '
              f'{calc_balance(balance, ex_rate_btc_to_uan)} IN UAN AND ' 
              f'{convert_to_usd(calc_balance(balance, ex_rate_btc_to_uan))}'
              f' IN USD.')


if __name__ == "__main__":
    create_output()
