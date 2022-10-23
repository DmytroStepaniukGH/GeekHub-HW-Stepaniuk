"""
2. Створіть функцію для валідації пари ім'я/пароль за наступними правилами:
   - ім'я повинно бути не меншим за 3 символа і не більшим за 50;
   - пароль повинен бути не меншим за 8 символів і повинен мати хоча б одну
   цифру;
   - якесь власне додаткове правило :) додав: ім'я має складатись із
     латинських літер, пароль - містити спецсимвол із даного набору !@#$%
   Якщо якийсь із параметрів не відповідає вимогам - породити виключення із
   відповідним текстом.
"""
import re


class ValidateException(Exception):
    pass


def validate(login, password):
    pattern_login = re.compile('^[A-Za-z]{3,50}$')
    pattern_password = re.compile(r'^(?=.*[0-9].*)(?=.*[A-Za-z].*)'
                                  r'(?=.*[!@#$%].*)[0-9a-zA-Z!@#$%]{8,}$')
    check_login = False
    check_password = False

    if pattern_login.search(login):
        check_login = True
    if pattern_password.search(password):
        check_password = True

    if check_login and check_password:
        return f'{"All ok"}'
    elif check_login and not check_password:
        return ValidateException('The password does not meet the '
                                 'requirements')
    elif not check_login and check_password:
        return ValidateException('The login does not meet the '
                                 'requirements')
    else:
        return ValidateException('The login and password do not meet the '
                                 'requirements')


if __name__ == "__main__":
    user_login = input("Login: ")
    user_password = input("Password: ")
    print(validate(user_login, user_password))
