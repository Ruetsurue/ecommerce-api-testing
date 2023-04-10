from helpers.api.common import RequestsUtility


class ProductsAPI:

    def __init__(self):
        self.req = RequestsUtility()

    def get_products_by_params(self, **request_params):
        endpoint = "/wp-json/wc/v3/products"
        return self.req.get_api_records_by_pages(endpoint=endpoint, **request_params)

    def get_product_by_id(self, product_id):
        endpoint = f"/wp-json/wc/v3/products/{str(product_id)}"
        return self.req.get(endpoint=endpoint)

    def create_product(self, product_info):
        endpoint = "/wp-json/wc/v3/products"
        return self.req.post(endpoint=endpoint, payload=product_info)

    def update_product(self, product_id, product_info):
        endpoint = f"/wp-json/wc/v3/products/{product_id}"
        return self.req.put(endpoint=endpoint, payload=product_info)
