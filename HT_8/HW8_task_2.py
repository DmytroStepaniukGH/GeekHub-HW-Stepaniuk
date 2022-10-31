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
        with open(file_name, 'r', encoding='utf-8') as f:
            if len(f.read()) >= n_symb:
                f.seek(0)
                s = f.read()
                mid_ch = len(s) // 2

                start_s = s[:n_symb]
                end_s = s[-n_symb:]

                if n_symb % 2 == 0:
                    mid_s = s[mid_ch - n_symb // 2:mid_ch + n_symb // 2]
                else:
                    mid_s = s[mid_ch - n_symb // 2:mid_ch + n_symb // 2 + 1]

                return f'{start_s}\t\t{mid_s}\t\t{end_s}'
            else:
                return f'The specified number of characters exceeds the ' \
                       f'number of characters in the file'
    except FileNotFoundError:
        return FileNotFoundError('Error: no such file or directory')


if __name__ == "__main__":
    print(reader('python_description.txt', 3))
