"""
6. Write a script to get the maximum and minimum VALUE in a dictionary.
"""
if __name__ == "__main__":
    dict_1 = {"USD2017": 25, "USD2018": 28, "USD2019": 26,
              "USD2020": 23, "USD2021": 27, "USD2022": 36}

    print(f'Maximum: {max(dict_1.values())}')
    print(f'Minimum: {min(dict_1.values())}')