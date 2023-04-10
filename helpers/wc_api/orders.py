from helpers.wc_api.common import WC_API
from helpers.entities.orders import OrdersHelper
from helpers.sql.products import ProductsSQL
from random import randint


class WC_API_Orders:

    def __init__(self):
        self.wc_api = WC_API()

    def create_order(self, custom_payload=None, use_random_product=True):
        endpoint = "orders"
        payload: dict = OrdersHelper.load_sample_order_json()

        if custom_payload:
            # sample_payload |= custom_payload
            payload.update(custom_payload)

        if payload.get('line_items') is None and use_random_product:
            products_sql = ProductsSQL()
            random_product = products_sql.select_random_product()
            payload.update({
                'line_items': [
                    {
                        "product_id": random_product.ID,
                        "quantity": randint(1, 10),
                    }
                ]
            })

        # use guest user if unspecified
        if payload.get('customer_id') is None:
            payload.update({'customer_id': 0})

        new_order = self.wc_api.post(endpoint, data=payload)
        return new_order

    def get_order(self, order_id):
        endpoint = f"orders/{order_id}"
        order = self.wc_api.get(endpoint=endpoint)
        return order

    def update_order(self, order_id, data):
        endpoint = f"orders/{order_id}"
        response = self.wc_api.put(endpoint=endpoint, data=data)
        return response

    def update_order_invalid_data(self, order_id, data, expected_status=400):
        endpoint = f"orders/{order_id}"
        response = self.wc_api.put(endpoint=endpoint, data=data, expected_status=expected_status)
        return response

    def move_order_to_status(self, order_id, new_status):
        data = {
            "status": new_status
        }
        return self.update_order(order_id=order_id, data=data)

    def cancel_order(self, order_id):
        status = "cancelled"
        return self.move_order_to_status(order_id, status)
