import os
from src.utils import utils


class Orders:

    def __init__(self):
        self.json_file = os.getenv('ORDERS_FILE_PATH', '/Users/c325018/Documents/interviews/electronic-bot/src/data/orders.json')
        self.json_file = os.getenv('ORDERS_FILE_PATH', '/Users/c325018/Documents/interviews/electronic-bot/src/data/orders.json')

    def read_file(self):
        json_file = utils.read_json_file(self.json_file)
        return json_file

    def get_orders(self):
        dict_orders = self.read_file()
        return dict_orders

if __name__ == "__main__":
    ORD = Orders()
    ORD.read_file()
    ORD.get_orders()