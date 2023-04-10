import pytest
import time

from configs.set_env import create_test_enviroment
from helpers.wc_api.coupons import WC_API_Coupons


@pytest.fixture(scope="module")
def test_ctx():
    coupon_tests_ctx = {
        "wc_api_coupons": WC_API_Coupons()
    }
    return coupon_tests_ctx


@pytest.mark.coupons
class TestCoupons:

    @pytest.mark.parametrize("coupon_discount_type", [
        pytest.param("percent", marks=pytest.mark.tcid37),
        pytest.param("fixed_cart", marks=pytest.mark.tcid38),
        pytest.param("fixed_product", marks=pytest.mark.tcid39),
    ])
    def test_create_coupon_discount_type(self, coupon_discount_type, test_ctx):

        timestamp = time.strftime("%d%m%y_%H%M%S")
        coupon_data = {
            "code": f"coupon_{coupon_discount_type}_{timestamp}",
            "discount_type": coupon_discount_type
        }

        new_coupon = test_ctx['wc_api_coupons'].create_coupon(coupon_data)
        coupon_id = new_coupon['id']

        coupon_info = test_ctx['wc_api_coupons'].get_coupon(coupon_id)
        assert coupon_info['code'] == coupon_data['code'], \
            f"Expected coupon code: {coupon_data['code']}, actual: {coupon_info['code']}"

        assert coupon_info['discount_type'] == coupon_discount_type, \
            f"Expected coupon discount type: {coupon_discount_type}, actual: {coupon_info['discount_type']}"

    @pytest.mark.negative
    @pytest.mark.tcid40
    def test_create_coupon_invalid_data(self, test_ctx):

        timestamp = time.strftime("%d%m%y_%H%M%S")
        coupon_discount_type = 'asdfghjk'
        coupon_data = {
            "code": f"coupon_{coupon_discount_type}_{timestamp}",
            "discount_type": coupon_discount_type
        }

        new_coupon = test_ctx['wc_api_coupons'].create_coupon_with_invalid_data(coupon_data)
        assert not new_coupon.get('id'), f"Coupon should not have been created"
