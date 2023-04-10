from helpers.misc.generators.customers import CustomerInfoGenerator as ci
from helpers.api.common import RequestsUtility


class CustomerAPI:

    def __init__(self):
        self.req = RequestsUtility()

    def create_customer(self, **kwargs):
        endpoint = "/wp-json/wc/v3/customers"
        customer_info = {}

        if not kwargs.get('email'):
            customer_info['email'] = ci.gen_email(**kwargs)

        if not kwargs.get('password'):
            customer_info['password'] = ci.gen_password(**kwargs)

        customer_info.update(**kwargs)
        return self.req.post(endpoint=endpoint, payload=customer_info)

    def create_customer_with_existing_email(self, **kwargs):
        endpoint = "/wp-json/wc/v3/customers"
        customer_info = {}
        customer_info.update(**kwargs)
        return self.req.post(endpoint=endpoint, payload=customer_info, expected_response_code=400)

    def list_all_customers(self, per_page=100):
        endpoint = '/wp-json/wc/v3/customers'
        params = {"per_page": per_page, "role": "all"}
        return self.req.get(endpoint=endpoint, params=params)
