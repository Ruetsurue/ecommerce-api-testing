from helpers.wc_api.common import WC_API


class WC_API_Products:
    def __init__(self):
        self.wc_api = WC_API()

    def update_product(self, product_id, product_info):
        endpoint = f"products/{product_id}"
        response = self.wc_api.put(endpoint=endpoint, data=product_info)
        return response
