from helpers.db import DAO


class OrdersSQL:
    def __init__(self):
        self.db = DAO()

    def select_items_in_order(self, order_id, order_item_type='line_item'):
        sql = "SELECT * FROM wp_woocommerce_order_items " \
              "WHERE `order_id` = :order_id AND `order_item_type` = :order_item_type"

        binds = {
            "order_id": order_id,
            "order_item_type": order_item_type,
        }

        return self.db.execute_sql(sql, **binds).all()

    def select_order_items_details(self, order_item_ids: list):
        if not isinstance(order_item_ids, list):
            order_item_ids = [order_item_ids]

        sql = "SELECT * FROM wp_woocommerce_order_itemmeta WHERE `order_item_id` IN :order_item_ids"
        binds = {"order_item_ids": order_item_ids}
        order_item_details = self.db.execute_sql(sql, **binds).all()

        result = {}
        for line in order_item_details:
            index = line['order_item_id']
            if index not in result.keys():
                result[index] = {line['meta_key']: line['meta_value']}
            else:
                result[index].update({line['meta_key']: line['meta_value']})

        return result
