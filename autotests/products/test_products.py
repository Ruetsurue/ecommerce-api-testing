import datetime
import logging
import pytest

from helpers.api.products import ProductsAPI
from helpers.sql.products import ProductsSQL
from helpers.wc_api.products import WC_API_Products
from helpers.misc.generators.common import generate_random_string
from configs.set_env import create_test_enviroment


@pytest.fixture(scope="module")
def product_test_ctx():
    ctx = {
        "prod_api": ProductsAPI(),
        "prod_sql": ProductsSQL(),
        "wc_api_products": WC_API_Products(),
    }

    return ctx


@pytest.mark.products
class TestProducts:

    @pytest.mark.tcid47
    def test_show_all_products(self, product_test_ctx):
        api_products = product_test_ctx['prod_api'].get_products_by_params()
        logging.info(f"Products in API: {len(api_products)}")

        db_products = product_test_ctx['prod_sql'].select_all_products_from_db()
        logging.info(f"Products in DB: {len(db_products)}")

        err_msg = "Number of products in API and DB doesn't match"
        assert len(api_products) == len(db_products), err_msg

    @pytest.mark.tcid25
    def test_product_by_id(self, product_test_ctx):
        db_product = product_test_ctx['prod_sql'].select_random_product()
        api_product = product_test_ctx['prod_api'].get_product_by_id(db_product.ID)

        assert api_product['name'] == db_product.post_title, "Product name in API and DB doesn't match"

    @pytest.mark.tcid26
    def test_create_simple_product(self, product_test_ctx):
        product_info = {
            "name": generate_random_string(prefix="tcid26"),
            "type": "simple",
            "regular_price": "10.99",
        }

        new_product = product_test_ctx['prod_api'].create_product(product_info)
        db_product = product_test_ctx['prod_sql'].select_product_by_id(new_product['id'])

        assert new_product['name'] == db_product.post_title, "Product name doesn't match"
        assert new_product['regular_price'] == product_info['regular_price'], "Price doesn't match"
        assert new_product['type'] == product_info['type'], "Product type doesn't match"

    @pytest.mark.tcid51
    def test_get_products_with_after_filter(self, product_test_ctx):

        last_days = 3
        date_after = datetime.datetime.now().replace(microsecond=0) - datetime.timedelta(days=last_days)
        date_after = datetime.datetime.isoformat(date_after)
        logging.info(f"Selecting products created after {date_after}")

        products_after_api = product_test_ctx['prod_api'].get_products_by_params(after=date_after)
        products_after_db = product_test_ctx['prod_sql'].select_all_products_after(after=date_after)

        err_msg = f"Number of entries doesn't match. API: {len(products_after_api)}, DB: {len(products_after_db)}"
        logging.info(f"API products: {len(products_after_api)}, DB products: {len(products_after_db)}")
        assert len(products_after_api) == len(products_after_db), err_msg

        product_ids_api = set([product['id'] for product in products_after_api])
        product_ids_db = set([product.ID for product in products_after_db])
        logging.info(f"API IDs: {product_ids_api}, DB IDs: {product_ids_db}")

        unmatched_product_ids = list(product_ids_api - product_ids_db)
        assert not unmatched_product_ids, f"Some product IDs didn't match: {unmatched_product_ids}"

    @pytest.mark.tcid61
    def test_update_product_regular_price(self, product_test_ctx):
        random_product = product_test_ctx['prod_sql'].select_random_product()
        product_id = random_product.ID

        new_product_info = {"regular_price": "95.99"}
        product_test_ctx['wc_api_products'].update_product(product_id, new_product_info)
        product_info = product_test_ctx['prod_api'].get_product_by_id(product_id)

        assert product_info['regular_price'] == new_product_info['regular_price'], \
            f"Expected product regular_price in API: {new_product_info['regular_price']}, " \
            f"actual: {product_info['regular_price']}"

    @pytest.mark.tcid63
    def test_update_sale_price_sets_on_sale_true(self, product_test_ctx):

        product_info = {
            "name": generate_random_string(prefix="tcid63"),
            "type": "simple",
            "regular_price": "63.99",
        }

        new_product = product_test_ctx['prod_api'].create_product(product_info)
        assert not new_product['on_sale'], f"Expected on_sale == False or absent, actual: {new_product['on_sale']}"

        sale_price = {"sale_price": "53.99"}
        product_test_ctx['wc_api_products'].update_product(new_product['id'], product_info=sale_price)
        product_info = product_test_ctx['prod_api'].get_product_by_id(new_product['id'])
        assert product_info['on_sale'], f"Expected on_sale == True, actual: {new_product['on_sale']}"

    @pytest.mark.tcid64
    def test_update_sale_price_sets_on_sale_false(self, product_test_ctx):

        product_info = {
            "name": generate_random_string(prefix="tcid64"),
            "type": "simple",
            "regular_price": "64.99",
        }

        new_product = product_test_ctx['prod_api'].create_product(product_info)
        assert not new_product['on_sale'], f"Expected on_sale == False or absent, actual: {new_product['on_sale']}"

        set_sale_price = {"sale_price": "54.99"}
        product_test_ctx['wc_api_products'].update_product(new_product['id'], product_info=set_sale_price)
        product_info = product_test_ctx['prod_api'].get_product_by_id(new_product['id'])
        assert product_info['on_sale'], f"Expected on_sale == True, actual: {new_product['on_sale']}"

        empty_sale_price = {"sale_price": ""}
        product_test_ctx['wc_api_products'].update_product(new_product['id'], product_info=empty_sale_price)
        product_info = product_test_ctx['prod_api'].get_product_by_id(new_product['id'])
        assert not product_info['on_sale'], f"Expected on_sale == False or absent, actual: {new_product['on_sale']}"

    @pytest.mark.tcid65
    def test_update_sell_price(self, product_test_ctx):

        product_info = {
            "name": generate_random_string(prefix="tcid65"),
            "type": "simple",
            "regular_price": "64.99",
        }

        new_product = product_test_ctx['prod_api'].create_product(product_info)
        assert not new_product['on_sale'], f"Expected on_sale == False or absent, actual: {new_product['on_sale']}"

        set_sale_price = {"sale_price": "54.99"}
        product_test_ctx['wc_api_products'].update_product(new_product['id'], product_info=set_sale_price)
        product_info = product_test_ctx['prod_api'].get_product_by_id(new_product['id'])
        assert product_info['sale_price'] == set_sale_price['sale_price'], \
            f"Expected sale_price == {set_sale_price['sale_price']}, actual: {new_product['on_sale']}"

        new_sale_price = {"sale_price": "44.99"}
        product_test_ctx['wc_api_products'].update_product(new_product['id'], product_info=new_sale_price)
        product_info = product_test_ctx['prod_api'].get_product_by_id(new_product['id'])
        assert product_info['sale_price'] == new_sale_price['sale_price'], \
            f"Expected sale_price == {new_sale_price['sale_price']}, actual: {new_product['on_sale']}"
