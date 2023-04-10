from helpers.wc_api.coupons import WC_API_Coupons


class CouponHelper:

    def __init__(self):
        self.api = WC_API_Coupons()

    def find_coupon_by_code(self, coupon_code, case_sensitive=True):
        coupons = self.api.get_all_coupons()

        for coupon in coupons:
            if case_sensitive:
                if coupon['code'] == coupon_code:
                    return coupon
            else:
                if coupon['code'].lower() == coupon_code.lower():
                    return coupon

        return None
