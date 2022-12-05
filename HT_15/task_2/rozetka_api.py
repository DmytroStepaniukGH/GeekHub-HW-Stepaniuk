import requests


class RozetkaAPI:
    @staticmethod
    def get_item_data(item_id):
        try:
            item_info = {'item_id': item_id}
            url = 'https://rozetka.com.ua/api/product-api/v4/goods/get-main?' \
                  'front-type=xl&country=UA&lang=ua&goodsId='
            session = requests.Session()
            data = session.get(url + f'{item_id}').json()
            item_info['title'] = data['data']['title']
            item_info['old_price'] = data['data']['old_price']
            item_info['current_price'] = data['data']['price']
            item_info['href'] = data['data']['href']
            item_info['brand'] = data['data']['brand']
            item_info['category'] = data['data']['breadcrumbs'][-1]['title']

            return item_info

        except KeyError:
            return False




