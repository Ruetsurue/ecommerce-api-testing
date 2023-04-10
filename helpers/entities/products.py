from helpers.api.products import ProductsAPI
from helpers.sql.products import ProductsSQL


class ProductHelper:
    def __init__(self):
        self.api = ProductsAPI()
        self.sql = ProductsSQL()

    def select_all_products_from_db(self):
        return self.sql.select_all_products_from_db()

    def get_all_products_from_api(self, per_page=100):
        return self.api.get_products_by_params(per_page=per_page)

    def select_random_product_from_db(self):
        return self.sql.select_random_product()

    def get_product_by_id(self, product_id):
        return self.api.get_product_by_id(product_id)
