"""
5. Напишіть функцію,яка приймає на вхід рядок та повертає кількість окремих
   регістро-незалежних букв та цифр, які зустрічаються в рядку більше ніж 1
   раз. Рядок буде складатися лише з цифр та букв (великих і малих).
   Реалізуйте обчислення за допомогою генератора в один рядок
    Example (input string -> result):
    "abcde" -> 0            # немає символів, що повторюються
    "aabbcde" -> 2          # 'a' та 'b'
    "aabBcde" -> 2          # 'a' присутнє двічі і 'b' двічі (`b` та `B`)
    "indivisibility" -> 1   # 'i' присутнє 6 разів
    "Indivisibilities" -> 2 # 'i' присутнє 7 разів та 's' двічі
    "aA11" -> 2             # 'a' і '1'
    "ABBA" -> 2             # 'A' і 'B' кожна двічі
"""


def count_chars(sequence):
    return f""""{sequence}" -> {len({x: sequence.lower().count(x) 
                                     for x in set(sequence.lower()) 
                                     if sequence.lower().count(x) > 1})}"""


if __name__ == "__main__":
    test_string = input('Input string: ')

    print(count_chars(test_string))
