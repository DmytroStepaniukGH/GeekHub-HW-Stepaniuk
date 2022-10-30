"""
2. Написати функцію, яка приймає два параметри: ім'я (шлях) файлу та
   кількість символів. Файл також додайте в репозиторій. На екран має бути
   виведений список із трьома блоками - символи з початку, із середини та з
   кінця файлу. Кількість символів в блоках - та, яка введена в другому
   параметрі. Придумайте самі, як обробляти помилку, наприклад, коли
   кількість символів більша, ніж є в файлі або, наприклад, файл із двох
   символів і треба вивести по одному символу, то що виводити на місці
   середнього блоку символів?). Не забудьте додати перевірку чи файл існує.
"""


def reader(file_name, n_symb):
    try:
        with open(file_name, 'r', encoding = 'utf-8') as f:
            len_file = len(f.read())
            if len_file % n_symb == 0 and len_file == n_symb * 3:
                f.seek(0)
                return f'{f.read(n_symb)}\t{f.read(n_symb)}' \
                       f'\t{f.read(n_symb)}'
            else:
                return f'Error. It is not possible to divide the ' \
                       f'file into the specified number of characters ' \
                       f'in blocks.'
    except FileNotFoundError:
        return FileNotFoundError('Error: no such file or directory')


if __name__ == "__main__":
    print(reader("python_description.txt", 28))
