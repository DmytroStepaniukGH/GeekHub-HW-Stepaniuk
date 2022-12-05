import csv
import sqlite3


class CsvOperations:
    @staticmethod
    def get_ids(filepath):
        with open(filepath) as csvfile:
            data = []
            reader = csv.DictReader(csvfile)
            for item in reader:
                data.append(int(item['id']))

        return data


class DataBaseOperations:
    @staticmethod
    def write_data_to_database(data):
        conn = sqlite3.connect("products.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO products_info (item_id, title, old_price,"
                    " current_price, href, brand, category) "
                    "VALUES (?,?,?,?,?,?,?)", [value for value in data.values()])
        conn.commit()
        conn.close()
