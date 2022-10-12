"""
2. Write a script to remove empty elements from a list.
   Test list: [(), ('hey'), ('',), ('ma', 'ke', 'my'), [''], {},
   ['d', 'a', 'y'], '', []]
"""
if __name__ == "__main__":
    test_list = [(), ('hey'), ('',), ('ma', 'ke', 'my'), [''], {}, ['d', 'a', 'y'], '', []]

    test_list = list(filter(None, test_list))
    print(f'Result: {test_list}')
