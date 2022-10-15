"""
4. Наприклад маємо рядок --> "f98neroi4nr0c3n30irn03ien3c0rfe kdno400we(n
   w,kowe%00koi!jn35pijnp4 6ij7k5j78p3kj546p4 65jnpoj35po6j345" -> просто
   потицяв по клавi =)
   Створіть ф-цiю, яка буде отримувати довільні рядки на зразок цього та
   яка обробляє наступні випадки:
   -  якщо довжина рядка в діапазоні 30-50 (включно) -> прiнтує довжину
      рядка, кiлькiсть букв та цифр
   -  якщо довжина менше 30 -> прiнтує суму всіх чисел та окремо рядок без
      цифр та знаків лише з буквами (без пробілів)
   -  якщо довжина більше 50 -> щось вигадайте самі, проявіть фантазію =)
"""


def string_parser(s):
    if len(s) in range(30, 51):
        count_of_digits = 0
        count_of_chars = 0

        for char in s:
            if char.isdigit():
                count_of_digits += 1
            elif char.isalpha():
                count_of_chars += 1

        print(f'Len of string = {len(s)}\n'
              f'Number of letters = {count_of_chars}\n'
              f'Number of digits = {count_of_digits}')

    elif len(s) < 30:
        list_of_digits = []
        chars = ''

        for char in s:
            if char.isdigit():
                list_of_digits.append(int(char))
            elif char.isalpha():
                chars += char

        print(f'Len of string = {len(s)}\n'
              f'String (only letters) = {chars}\n'
              f'Sum of digits = {sum(list_of_digits)}')

    else:
        pattern = """!@#$%^&*'()"{}-+?_=,<>/"""
        special_symbols = ''
        for char in s:
            if char in pattern:
                special_symbols += char
        print(f'Len of special symbols = {len(special_symbols)}\n'
              f'String (only special symbols) = {special_symbols}')


if __name__ == "__main__":
    s1 = 'f98neroi4nr0c3n30irn03ie n3c0rfe54{{{//'
    s2 = 'f98neroi4nrn03ie n3c0r54{{{//'
    s3 = """f98neroi4nr0c3n30irn'"03ie{P[[{[[n3c0rfe kdno400we(nw,kowe%00ko" \
         "i!jn35pijnp4 6ij7k5j78p3kj546p4 65jnpoj35po6j345"""

    string_parser(s1)