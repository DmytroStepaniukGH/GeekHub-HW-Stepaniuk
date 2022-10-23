"""
1. Створіть функцію, всередині якої будуть записано СПИСОК із п'яти
   користувачів (ім'я та пароль). Функція повинна приймати три аргументи:
   два - обов'язкових (<username> та <password>) і третій - необов'язковий
   параметр <silent> (значення за замовчуванням - <False>).
   Логіка наступна:
    якщо введено правильну пару ім'я/пароль - вертається True;
    якщо введено неправильну пару ім'я/пароль:
        якщо silent == True - функція повертає False
        якщо silent == False - породжується виключення LoginException (його
        також треба створити =))
"""


class LoginException(Exception):
    pass


def verification(login, password, silent=False):
    valid_data = [('DimaS', 'qwerty12'), ('Vania', '34gqqA@'),
                  ('Sasha', '1122gg'), ('invoker', 'qqewwe1'),
                  ('Test', '1test1')]

    check = False
    for item in valid_data:
        if login == item[0] and password == item[1]:
            check = True
            break

    if check:
        return True
    else:
        return False if silent else LoginException('LoginException!')


if __name__ == "__main__":
    user_login = input("Login: ")
    user_password = input("Password: ")

    print(verification(user_login, user_password, True))
