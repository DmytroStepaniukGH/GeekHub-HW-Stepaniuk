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
    general_pattern = re.compile('^[0-9a-zA-Z!@#$%]+$')
    char = re.compile('[A-Za-z]')
    number = re.compile('[0-9]')
    spec_char = re.compile('[!@#$%]')
    errors = ''

    try:
        re.search(general_pattern, login).group()
        re.search(general_pattern, password).group()
    except AttributeError:
        return ValidateException('Entered characters cannot be used as '
                                 'login/password characters.\nNote: valid '
                                 'characters for the login are letters of '
                                 'the Latin alphabet.\nFor the password - '
                                 'letters of the Latin alphabet, numbers '
                                 'and special characters !@#$%.')
    else:
        if not char.search(login):
            errors += 'The login must contain only Latin letters.\n'
        if len(login) not in range(3, 51):
            errors += 'The length of the login should be from 3 to 50.\n'
        if not char.search(password):
            errors += 'The password must contain Latin letters.\n'
        if not number.search(password):
            errors += 'The password must contain numbers.\n'
        if not spec_char.search(password):
            errors += 'The password must contain special symbols (!@#$%).\n'
        if len(password) < 8:
            errors += 'Password must be 8 or more characters long\n'

        return 'OK' if len(errors) == 0 else ValidateException(f'{errors}')


if __name__ == "__main__":
    user_login = input("Login: ")
    user_password = input("Password: ")
    print(validate(user_login, user_password))
