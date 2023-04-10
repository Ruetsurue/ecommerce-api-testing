from helpers.wc_api.common import WC_API


class WC_API_Coupons:
    def __init__(self):
        self.wc_api = WC_API()

    def get_coupon(self, coupon_id):
        endpoint = f"coupons/{coupon_id}"
        return self.wc_api.get(endpoint=endpoint)

    def get_all_coupons(self):
        endpoint = f"coupons"
        return self.wc_api.get(endpoint=endpoint)

    def create_coupon(self, coupon_data):
        endpoint = "coupons"
        response = self.wc_api.post(endpoint=endpoint, data=coupon_data)
        return response

    def create_coupon_with_invalid_data(self, coupon_data):
        endpoint = "coupons"
        response = self.wc_api.post(endpoint=endpoint, data=coupon_data, expected_status=400)
        return response

    def create_n_percent_off_coupon(self, n_percent):
        coupon_data = {
            "code": f"{n_percent}off",
            "discount_type": "percent",
            "amount": str(n_percent),
        }

        return self.create_coupon(coupon_data)
