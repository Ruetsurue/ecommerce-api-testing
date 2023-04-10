import pytest
from random import randint
from configs.set_env import create_test_enviroment
from helpers.api.products import ProductsAPI
from helpers.sql.products import ProductsSQL
from helpers.sql.orders import OrdersSQL
from helpers.wc_api.orders import WC_API_Orders
from helpers.wc_api.coupons import WC_API_Coupons
from helpers.entities.orders import OrdersHelper
from helpers.entities.customers import CustomerHelper
from helpers.entities.coupons import CouponHelper
from helpers.misc.generators.common import generate_random_string


@pytest.fixture(scope='module')
def order_tests_ctx():
    order_test_context = {
        "products_sql": ProductsSQL(),
        "orders_sql": OrdersSQL(),
        "products_api": ProductsAPI(),
        "wc_api_orders": WC_API_Orders(),
        "wc_api_coupons": WC_API_Coupons(),
        "customer_helper": CustomerHelper(),
        "coupon_helper": CouponHelper(),
    }

    return order_test_context


@pytest.mark.orders
class TestOrders:
    @pytest.mark.tcid48
    @pytest.mark.xfail(reason="Order validation needs to be reworked")
    def test_create_paid_order_guest_user(self, order_tests_ctx):

        order_data = {"customer_id": 0}
        api_order = order_tests_ctx['wc_api_orders'].create_order(order_data)
        OrdersHelper.assert_api_order(api_order=api_order, expected_values=order_data)

        items_in_order = order_tests_ctx['orders_sql'].select_items_in_order(api_order['id'])
        OrdersHelper.assert_db_items_in_order(items_in_order=items_in_order, expected_values=order_data)

        order_item_ids = [item['order_item_id'] for item in items_in_order]
        order_item_details = order_tests_ctx['orders_sql'].select_order_items_details(order_item_ids)
        OrdersHelper.assert_db_items_in_order_details(items_in_order_details=order_item_details,
                                                      expected_values=order_data)

    @pytest.mark.tcid49
    @pytest.mark.xfail(reason="Order validation needs to be reworked")
    def test_create_paid_order_registered_user(self, order_tests_ctx):

        new_user = order_tests_ctx['customer_helper'].create_customer()
        order_data = {"customer_id": new_user['id']}
        api_order = order_tests_ctx['wc_api_orders'].create_order(order_data)
        OrdersHelper.assert_api_order(api_order=api_order, expected_values=order_data)

        items_in_order = order_tests_ctx['orders_sql'].select_items_in_order(api_order['id'])
        OrdersHelper.assert_db_items_in_order(items_in_order=items_in_order, expected_values=order_data)

        order_item_ids = [item['order_item_id'] for item in items_in_order]
        order_item_details = order_tests_ctx['orders_sql'].select_order_items_details(order_item_ids)
        OrdersHelper.assert_db_items_in_order_details(items_in_order_details=order_item_details,
                                                      expected_values=order_data)

    @pytest.mark.parametrize("move_to_status", [
        pytest.param("cancelled", marks=pytest.mark.tcid55),
        pytest.param("completed", marks=pytest.mark.tcid56),
        pytest.param("on-hold", marks=pytest.mark.tcid57),
    ])
    def test_change_order_status(self, move_to_status, order_tests_ctx):
        new_order = order_tests_ctx['wc_api_orders'].create_order()
        new_order_id = new_order['id']

        order_info = order_tests_ctx['wc_api_orders'].get_order(new_order_id)
        assert order_info, f"Order id={order_info['id']} not found"

        order_tests_ctx['wc_api_orders'].move_order_to_status(order_id=new_order_id, new_status=move_to_status)
        order_info = order_tests_ctx['wc_api_orders'].get_order(new_order_id)
        assert order_info['status'] == move_to_status, \
            f"Expected order status {move_to_status}, actual: {order_info['status']}"

    @pytest.mark.negative
    @pytest.mark.tcid58
    def test_change_order_invalid_status(self, order_tests_ctx):
        move_to_status = "asdfghj"
        new_order = order_tests_ctx['wc_api_orders'].create_order()
        new_order_id = new_order['id']

        order_info = order_tests_ctx['wc_api_orders'].get_order(new_order_id)
        assert order_info, f"Order id={order_info['id']} not found"

        data = {"status": move_to_status}
        err_response = order_tests_ctx['wc_api_orders'].update_order_invalid_data(new_order_id, data=data)

        exp_err_code = "rest_invalid_param"
        assert err_response['code'] == exp_err_code, \
            f"Expected error code {exp_err_code}, actual: {err_response['code']}"

        exp_err_msg = "Invalid parameter(s): status"
        assert err_response['message'] == exp_err_msg, \
            f"Expected error message {exp_err_msg}, actual: {err_response['message']}"

    @pytest.mark.tcid59
    def test_update_order_customer_note(self, order_tests_ctx):
        new_order = order_tests_ctx['wc_api_orders'].create_order()
        new_order_id = new_order['id']

        order_info = order_tests_ctx['wc_api_orders'].get_order(new_order_id)
        assert order_info, f"Order id={order_info['id']} not found"

        new_customer_note = generate_random_string()
        data = {"customer_note": new_customer_note}
        order_tests_ctx['wc_api_orders'].update_order(new_order_id, data=data)

        order = order_tests_ctx['wc_api_orders'].get_order(new_order_id)
        assert order['customer_note'] == new_customer_note, \
            f"Expected customer_note: {new_customer_note}, actual: {order['customer_note']}"

    @pytest.mark.tcid60
    def test_order_with_50_percent_off_coupon(self, order_tests_ctx):

        coupon_code = "50off"
        coupon = order_tests_ctx['coupon_helper'].find_coupon_by_code(coupon_code)

        if not coupon:
            coupon = order_tests_ctx['wc_api_coupons'].create_n_percent_off_coupon(n_percent=50)

        product_info = {
            "name": generate_random_string(prefix="tcid60"),
            "type": "simple",
            "regular_price": "150",
        }

        product = order_tests_ctx['products_api'].create_product(product_info=product_info)
        product_info = order_tests_ctx['products_api'].get_product_by_id(product['id'])
        product_price = product_info['price']

        order_data = {
            "line_items": [{
                "product_id": product['id'],
                "quantity": randint(1, 10),
            }],
            "coupon_lines": [{
                "code": coupon_code,
            }]
        }
        order = order_tests_ctx['wc_api_orders'].create_order(custom_payload=order_data, use_random_product=False)

        expected_total = \
            float(product_price) * order_data['line_items'][0]['quantity'] * (float(coupon['amount']) / 100)

        order_shipping_total = [float(item['total']) for item in order['shipping_lines']]
        order_shipping_total = sum(order_shipping_total)
        total_without_shipping = float(order['total']) - order_shipping_total

        assert total_without_shipping == expected_total, \
            f"Expected order total: {expected_total}, actual: {total_without_shipping}"
