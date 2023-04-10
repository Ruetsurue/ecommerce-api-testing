import json
import os.path


class OrdersHelper:

    @classmethod
    def load_sample_order_json(cls):
        path = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(path, 'payloads', 'orders', 'create_order.json')

        with open(filepath, 'r') as file:
            order_payload = json.load(file)

        return order_payload

    @classmethod
    def assert_api_order(cls, api_order: dict, expected_values: dict):

        assert api_order['customer_id'] == expected_values['customer_id'], \
            f"customer_id == {expected_values['customer_id']} expected, actual: {api_order['customer_id']}"

        assert len(api_order['line_items']) == len(expected_values['line_items']), \
            f"Expected {len(expected_values['line_items'])} item in API order, actual: {len(api_order['line_items'])}"

        for index, item in enumerate(expected_values['line_items']):
            assert api_order['line_items'][index]['product_id'] == item['product_id'], \
                f"Expected product_id {item['product_id']}, actual: {api_order['line_items'][0]['product_id']}"

    @classmethod
    def assert_db_items_in_order(cls, items_in_order, expected_values):
        assert items_in_order, "Order not found in DB"
        assert len(items_in_order) == len(expected_values['line_items']), \
            f"Expected one item in DB order, actual: {len(items_in_order)}"

    @classmethod
    def assert_db_items_in_order_details(cls, items_in_order_details, expected_values):
        expect = {}
        for item in expected_values['line_items']:
            index = item.pop('product_id')
            expect[index] = item

        for order_item_id, item_details in items_in_order_details.items():
            product_id = int(item_details['_product_id'])

            expected_product_ids = map(lambda item: int(item), expect.keys())
            assert product_id in expected_product_ids, \
                f"Product_id {item_details['_product_id']} not found in expected ids list: {expected_product_ids}"

            assert str(item_details['_qty']) == str(expect[product_id]['quantity']), \
                f"Expected order quantity: {expect[product_id]['quantity']}, " \
                f"actual: {item_details['_qty']}"
