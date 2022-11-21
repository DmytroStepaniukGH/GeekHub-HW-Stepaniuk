"""
2. Створіть за допомогою класів та продемонструйте свою реалізацію шкільної
   бібліотеки (включіть фантазію). Наприклад вона може містити класи Person,
   Teacher, Student, Book, Shelf, Author, Category і.т.д. Можна робити по
   прикладу банкомату з меню, базою даних і т.д.
"""
import sqlite3


class Connection:

    def create_connection(self):
        conn = sqlite3.connect("library.db")
        return conn


class Person:

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name


class Student(Connection, Person):

    def return_book(self):
        conn = self.create_connection()
        cur = conn.cursor()

        cur.execute("SELECT book_taken_id FROM Users WHERE first_name=?"
                    " AND last_name=?", (self.first_name, self.last_name))
        row = cur.fetchone()
        book_id = row[0]

        cur.execute("UPDATE Users SET book_taken_id=? WHERE first_name=?"
                    " AND last_name=?", (0, self.first_name, self.last_name))
        conn.commit()

        cur.execute("UPDATE Books SET status=? WHERE id=?",
                    (True, book_id))
        conn.commit()

        cur.execute("SELECT title FROM Books WHERE id=?",
                    (book_id,))
        row = cur.fetchone()

        print(f'Книгу {row[0]} повернуто до бібліотеки\n')
        conn.close()

    def get_book_taken(self):
        conn = self.create_connection()
        cur = conn.cursor()

        cur.execute("SELECT book_taken_id FROM Users WHERE first_name=?"
                    " AND last_name=?", (self.first_name, self.last_name))
        row = cur.fetchone()

        return row[0]


class Book(Connection):

    def __init__(self, author=None, title=None, year_of_publication=None,
                 number_of_pages=None, genre=None):
        self.author = author
        self.title = title
        self.year_of_publication = year_of_publication
        self.number_of_pages = number_of_pages
        self.genre = genre

    def set_state(self, state):
        conn = self.create_connection()
        cur = conn.cursor()
        cur.execute("UPDATE Books SET state=? WHERE title=?",
                    (state, self.title))
        conn.commit()


class Librarian(Person, Connection):

    def __init__(self, first_name, last_name, age, gender):
        super().__init__(first_name, last_name)
        self.age = age
        self.gender = gender

    def _add_new_student(self):
        conn = self.create_connection()
        cur = conn.cursor()
        first_name = input("Введіть ім'я: ")
        last_name = input("Введіть прізвище: ")
        age = int(input("Введіть вік: "))
        gender = input("Введіть стать: ")
        group = input("Введіть групу: ")

        cur.execute("INSERT INTO Users (first_name, last_name, age, gender,"
                    "group_name, book_taken_id, is_librarian) "
                    "VALUES (?,?,?,?,?,?,?)",
                    (first_name, last_name, age, gender, group, 0, False))
        conn.commit()
        conn.close()
        print('Користувач успішно доданий\n')

    def _add_new_book(self):
        author = input("Введіть автора книги: ")
        title = input("Введіть назву книги: ")
        year_of_publication = int(input("Введіть рік видання: "))
        number_of_pages = int(input("Введіть кількість сторінок: "))
        genre = input("Введіть жанр книги: ")

        new_book = Book(author, title, year_of_publication, number_of_pages,
                        genre)
        new_book.status = True
        new_book.state = 'Стан нової'

        conn = self.create_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO Books (author, title, year, number_pages, "
                    "genre, state, status) VALUES (?,?,?,?,?,?,?)",
                    (author, title, year_of_publication, number_of_pages,
                     genre, new_book.state, new_book.status))
        conn.commit()
        conn.close()
        print('Книгу успішно додано\n')

    def _get_user_id(self, first_name, last_name):
        conn = self.create_connection()
        cur = conn.cursor()
        cur.execute("SELECT id FROM Users WHERE first_name=? AND last_name=?",
                    (first_name, last_name,))
        row = cur.fetchone()
        conn.close()
        return row[0]

    def __get_all_titles(self):
        conn = self.create_connection()
        cur = conn.cursor()
        cur.execute("SELECT title FROM Books")
        row = cur.fetchall()

        titles = []
        for title in row:
            titles.append(title[0])

        conn.commit()
        conn.close()
        return titles

    def __get_book_status(self, title):
        conn = self.create_connection()
        cur = conn.cursor()
        cur.execute("SELECT status FROM Books WHERE title=?", (title,))
        row = cur.fetchone()
        conn.close()
        return row[0]

    def _give_book(self, user_id, title):
        if title in self.__get_all_titles():
            if self.__get_book_status(title):
                conn = self.create_connection()
                cur = conn.cursor()
                cur.execute("UPDATE Books SET status=? WHERE title=?",
                            (False, title))
                conn.commit()
                cur.execute("SELECT id FROM Books WHERE title=?", (title,))
                row = cur.fetchone()
                book_id = row[0]
                cur.execute("UPDATE Users SET book_taken_id=? WHERE id=?",
                            (book_id, user_id))
                conn.commit()
                conn.close()
                print(f'Видана книга "{title}"\n')
            else:
                print(f'Книга з назвою "{title}" в бібліотеці є, '
                      'але на даний момент її немає в наявності\n')
        else:
            print(f'Книги з назвою "{title}" в бібліотеці немає\n')

    def _delete_book(self):
        title = input("Введіть назву книги: ")

        if title in self.__get_all_titles():
            conn = self.create_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM Books WHERE title=?", (title,))
            conn.commit()
            conn.close()
            print(f'Книгу "{title}" успішно видалено')
        else:
            print("Не вдалось видалити книгу з такою назвою")

    def _show_all_available_books(self):
        conn = self.create_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Books WHERE status > 0")
        row = cur.fetchall()

        if row:
            for book in row:
                print(f'Автор: {book[1]} | Назва: {book[2]} | '
                      f'Рік: {book[3]} | Сторінки: {book[4]} | '
                      f'Жанр: {book[5]} | Стан: {book[6]}')
        else:
            print('Нажаль, доступних книг немає\n')
        print('\n')
        conn.close()
        conn.close()


def main():
    in_main_menu = True
    librarian = Librarian('Ольга', 'Бащенко', 45, 'Жіноча')
    while in_main_menu:
        action = input(('Оберіть наступну дію:\n'
                        '1 - Видати книгу\n'
                        '2 - Прийняти книгу\n'
                        '3 - Показати всі доступні книги\n'
                        '4 - Додати нового користувача\n'
                        '5 - Робота з бібліотечним фондом\n'
                        '6 - Вихід\n'
                        'Ваша дія: '))
        try:
            if int(action) == 1:
                in_menu = True
                first_name = input("Введіть ім'я: ")
                last_name = input("Введіть прізвище: ")
                print('\n')

                try:
                    student = Student(first_name, last_name)
                    if student.get_book_taken():
                        print('Можна користуватися лише однією книгою '
                              'одночасно :( Великий попит\n')
                    else:
                        user_id = librarian._get_user_id(first_name, last_name)
                        title = input('Введіть назву книги: ')
                        librarian._give_book(user_id, title)

                except TypeError:
                    print('Не знайдено такого користувача.\n')
                    while in_menu:
                        action = input(('Оберіть наступну дію:\n'
                                        '1 - Створити нового користувача\n'
                                        '2 - Вихід\n'
                                        'Ваша дія: '))
                        try:
                            if int(action) == 1:
                                librarian._add_new_student()
                            elif int(action) == 2:
                                in_menu = False
                            else:
                                print('Введене значення не є дією '
                                      'із списку\n')
                        except ValueError:
                            print('Помилка введеного значення\n')

            elif int(action) == 2:
                first_name = input("Введіть ім'я: ")
                last_name = input("Введіть прізвище: ")
                print('\n')
                try:
                    student = Student(first_name, last_name)
                    student.return_book()
                except TypeError:
                    print('У вас ще немає книги в користуванні\n')

            elif int(action) == 3:
                librarian._show_all_available_books()

            elif int(action) == 4:
                librarian._add_new_student()

            elif int(action) == 5:
                in_menu = True
                while in_menu:
                    action = input(('Оберіть наступну дію:\n'
                                    '1 - Додати нову книгу\n'
                                    '2 - Видалити книгу\n'
                                    '3 - Змінити стан книги\n'
                                    '4 - Вихід\n'
                                    'Ваша дія: '))
                    try:
                        if int(action) == 1:
                            librarian._add_new_book()

                        elif int(action) == 2:
                            librarian._delete_book()

                        elif int(action) == 3:
                            title = input('Введіть назву книги для '
                                          'зміни її стану: ')
                            new_state = input('Опишіть стан книги: ')

                            book = Book()
                            book.title = title
                            book.set_state(new_state)
                            print('Стан книги успішно оновлений\n')

                        elif int(action) == 4:
                            in_menu = False

                        else:
                            print('Введене значення не є дією '
                                  'із списку\n')

                    except ValueError:
                        print('Помилка введеного значення\n')

            elif int(action) == 6:
                print('До зустрічі!')
                in_main_menu = False

            else:
                print('Введене значення не є дією із списку\n')
        except ValueError:
            print('Помилка введеного значення\n')


if __name__ == "__main__":
    main()
