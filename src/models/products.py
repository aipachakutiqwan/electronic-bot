import os
import json
from src.utils import utils
from collections import defaultdict

class Products:

    def __init__(self):
        self.json_file = os.getenv('PRODUCTS_FILE_PATH')

    def read_file(self):
        json_file = utils.read_json_file(self.json_file)
        return json_file

    def get_products(self):
        dict_products = self.read_file()
        return dict_products

    def get_products_and_category(self):
        products = self.get_products()
        products_by_category = defaultdict(list)
        for product_name, product_info in products.items():
            category = product_info.get('category')
            if category:
                products_by_category[category].append(product_info.get('name'))

        return dict(products_by_category)

    def get_product_by_name(self, name):
        products = self.get_products()
        return products.get(name, None)


    def get_products_by_category(self, category):
        products = self.get_products()
        return [product for product in products.values() if product["category"] == category]


    def generate_output_string(self, data_list):
        output_string = ""

        if data_list is None:
            return output_string

        for data in data_list:
            try:
                if "products" in data:
                    products_list = data["products"]
                    for product_name in products_list:
                        product = self.get_product_by_name(product_name)
                        if product:
                            output_string += json.dumps(product, indent=4) + "\n"
                        else:
                            print(f"Error: Product '{product_name}' not found")
                elif "category" in data:
                    category_name = data["category"]
                    category_products = self.get_products_by_category(category_name)
                    for product in category_products:
                        output_string += json.dumps(product, indent=4) + "\n"
                else:
                    print("Error: Invalid object format")
            except Exception as e:
                print(f"Error: {e}")

        return output_string


    def find_category_and_product_only(self, user_input, products_and_category):
        delimiter = "####"
        system_message = f"""
        You will be provided with customer service queries. \
        The customer service query will be delimited with {delimiter} characters.
        Output a python list of objects, where each object has the following format:
        'category': <one of Computers and Laptops, Smartphones and Accessories, Televisions and Home Theater Systems, \
        Gaming Consoles and Accessories, Audio Equipment, Cameras and Camcorders>,
        OR
        'products': <a list of products that must be found in the allowed products below>

        Where the categories and products must be found in the customer service query.
        If a product is mentioned, it must be associated with the correct category in the allowed products list below.
        If no products or categories are found, output an empty list.

        Allowed products:

        Computers and Laptops category:
        TechPro Desktop
        BlueWave Chromebook

        Smartphones and Accessories category:
        MobiTech Wireless Charger
        SmartX EarBuds

        Televisions and Home Theater Systems category:
        SoundMax Soundbar
        CineView OLED TV

        Gaming Consoles and Accessories category:
        GameSphere X
        ProGamer Controller

        Audio Equipment category:
        WaveSound Soundbar
        AudioPhonic Turntable

        Cameras and Camcorders category:
        ZoomMaster Camcorder
        FotoSnap Instant Camera

        Only output the list of objects, nothing else.
        """
        messages = [
            {'role': 'system', 'content': system_message},
            {'role': 'user', 'content': f"{delimiter}{user_input}{delimiter}"},
        ]
        return utils.get_completion_from_messages(messages)


if __name__ == "__main__":
    PROD = Products()
    PROD.read_file()
    PROD.get_products()
    products_and_category = PROD.get_products_and_category()
    user_input = ''
    print(PROD.find_category_and_product_only(user_input, products_and_category))

