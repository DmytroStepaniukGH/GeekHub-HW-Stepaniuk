import requests


class RozetkaAPI:
    @staticmethod
    def get_item_data(item_id):
        try:
            url = 'https://rozetka.com.ua/api/product-api/v4/goods/get-main?' \
                  'front-type=xl&country=UA&lang=ua&goodsId='
            session = requests.Session()
            data = session.get(url + f'{item_id}').json()
            title = data['data']['title']
            old_price = data['data']['old_price']
            current_price = data['data']['price']
            href = data['data']['href']
            brand = data['data']['brand']
            category = data['data']['breadcrumbs'][-1]['title']

            return item_id, title, old_price, current_price, href, brand, category

        except KeyError:
            return False




