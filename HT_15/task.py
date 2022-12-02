import rozetka_api
import data_operations


def main():
    file = 'ids.csv'
    all_ids = data_operations.CsvOperations.get_ids(file)
    info = []
    for product_id in all_ids:
        request = rozetka_api.RozetkaAPI.get_item_data(product_id)
        if request:
            info.append(request)
        else:
            print(f"Не вдалось отримати дані з ID {product_id}")

    for product in info:
        data_operations.DataBaseOperations.write_data_to_database(product)


if __name__ == '__main__':
    main()
