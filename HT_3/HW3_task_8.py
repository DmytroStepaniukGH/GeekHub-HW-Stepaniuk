"""
8. Створити цикл від 0 до ... (вводиться користувачем). В циклі створити
   умову, яка буде виводити поточне значення, якщо остача від ділення на 17
   дорівнює 0.
"""
if __name__ == "__main__":
    number = int(input('Input a number: '))

    for i in range(number):
        if i % 17 == 0:
            print(i)