"""
3. На основі попередньої функції (скопіюйте кусок коду) створити наступний
   скрипт:
   а) створити список із парами ім'я/пароль різноманітних видів
      (орієнтуйтесь по правилам своєї функції) - як валідні, так і ні;
   б) створити цикл, який пройдеться по цьому циклу і, користуючись
      валідатором, перевірить ці дані і надрукує для кожної пари значень
      відповідне повідомлення, наприклад:
      Name: vasya
      Password: wasd
      Status: password must have at least one digit
      -----
      Name: vasya
      Password: vasyapupkin2000
      Status: OK
   P.S. Не забудьте використати блок try/except ;)
"""
import re


class ValidateException(Exception):
    pass


def validate(login, password):
    pattern_password = re.compile('^[0-9a-zA-Z!@#$%]+$')
    char = re.compile('[A-Za-z]')
    number = re.compile('[0-9]')
    spec_char = re.compile('[!@#$%]')
    errors = ''

    try:
        re.search(pattern_password, login).group()
        re.search(pattern_password, password).group()
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
    users = [('Di', 'qwet()'), ('Va--', '34gqqA@'), ('Sasha', '1122gg'),
             ('inggg', 'qqewwtte$1'), ('Test', '1test1'),
             ('  ', 'ff677$fdfdf'), ('Gjjjdd', '{77}'), ('--f-', '/// f\\()')]

    for user in users:
        print(f'Name: {user[0]}\nPassword: {user[1]}\nStatus: '
              f'{validate(user[0], user[1])}\n---------------\n')
