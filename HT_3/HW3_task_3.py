"""
3. Write a script to concatenate the following dictionaries to create a NEW one.
   dict_1 = {'foo': 'bar', 'bar': 'buz'}
   dict_2 = {'dou': 'jones', 'USD': 36}
   dict_3 = {'AUD': 19.2, 'name': 'Tom'}
"""
if __name__ == "__main__":
    dict_1 = {'foo': 'bar', 'bar': 'buz'}
    dict_2 = {'dou': 'jones', 'USD': 36}
    dict_3 = {'AUD': 19.2, 'name': 'Tom'}

    result_dict = {}
    for item in (dict_1, dict_2, dict_3):
        result_dict.update(item)

    print(f'New dictionary: {result_dict}')