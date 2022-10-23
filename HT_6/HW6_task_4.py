"""
4. Створіть функцію <morse_code>, яка приймає на вхід рядок у вигляді коду
   Морзе та виводить декодоване значення (латинськими літерами).
   Особливості:
    - використовуються лише крапки, тире і пробіли (.- )
    - один пробіл означає нову літеру
    - три пробіли означають нове слово
    - результат може бути case-insensitive (на ваш розсуд - великими чи
      маленькими літерами).
    - для простоти реалізації - цифри, знаки пунктуацїї, дужки, лапки тощо
      використовуватися не будуть. Лише латинські літери.
    - додайте можливість декодування сервісного сигналу SOS (...---...)
    Приклад:
    --. . . -.- .... ..- -...   .. ...   .... . .-. .
    результат: GEEKHUB IS HERE
"""


def morse_code(code):
    morse_dict = {'.-': 'a', '-...': 'b', '-.-.': 'c', '-..': 'd', '.': 'e',
                  '..-.': 'f', '--.': 'g', '....': 'h', '..': 'i', '.---': 'j',
                  '-.-': 'k', '.-..': 'l', '--': 'm', '-.': 'n', '---': 'o',
                  '.--.': 'p', '--.-': 'q', '.-.': 'r', '...': 's', '-': 't',
                  '..-': 'u', '...-': 'v', '.--': 'w', '-..-': 'x',
                  '-.--': 'y', '--..': 'z', '*': ' ', '...---...': 'SOS'}

    return ''.join([morse_dict[char] for char in
                    code.replace('   ', ' * ').split()]).upper()


if __name__ == '__main__':
    text_to_decode = input("Input morse code to decode: ")
    try:
        print(morse_code(text_to_decode))
    except KeyError:
        print('The values entered are not morse code')
