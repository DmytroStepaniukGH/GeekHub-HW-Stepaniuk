"""
2. Написати програму, яка має складатися з трьох файлів/модулів.
- rozetka_api.py, де створти клас RozetkaAPI, який буде містити 1 метод
  get_item_data, який на вхід отримує id товара з сайту розетки та повертає
  словник з такими даними: item_id (він же і приймається на вхід), title,
  old_price, current_price, href (лінка на цей товар на сайті), brand,
  category. Всі інші методи, що потрібні для роботи мають бути
  приватні/захищені.
- data_operations.py з класами CsvOperations та DataBaseOperations.
  CsvOperations містить метод для читання даних. Метод для читання приймає
  аргументом шлях до csv файлу де в колонкі ID записані як валідні, так і не
  валідні id товарів з сайту. DataBaseOperations містить метод для запису
  даних в sqlite3 базу і відповідно приймає дані для запису. Всі інші методи,
  що потрібні для роботи мають бути приватні/захищені.
- task.py - головний модуль, який ініціалізує і запускає весь процес.
  Суть процесу: читаємо ID товарів з csv файлу, отримуємо необхідні дані і
  записуємо їх в базу. Якщо ID не валідний/немає даних - вивести відповідне
  повідомлення і перейти до наступного.
"""
import data_operations
from rozetka_api import RozetkaAPI


def main():
    file = 'ids.csv'
    all_ids = data_operations.CsvOperations.get_ids(file)
    info = []
    for product_id in all_ids:
        request = RozetkaAPI.get_item_data(product_id)
        if request:
            info.append(request)
        else:
            print(f"Не вдалось отримати дані з ID {product_id}")

    for product in info:
        data_operations.DataBaseOperations.write_data_to_database(product)


if __name__ == '__main__':
    main()
