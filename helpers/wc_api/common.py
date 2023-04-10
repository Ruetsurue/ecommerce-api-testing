import os
from woocommerce import API
from configs.hosts import API_HOSTS
from requests import Response


class WC_API:
    def __init__(self):
        self.wc_api = API(url=API_HOSTS[os.getenv('ENV')],
                          consumer_key=os.getenv('CONSUMER_KEY'),
                          consumer_secret=os.getenv('CONSUMER_SECRET'))

    def assert_status(self, response: Response, expected_status):
        assert response.status_code == expected_status

    def post(self, endpoint, data, expected_status=201, **kwargs):
        response = self.wc_api.post(endpoint=endpoint, data=data, **kwargs)
        self.assert_status(response, expected_status)
        return response.json()

    def get(self, endpoint, expected_status=200, **kwargs):
        response = self.wc_api.get(endpoint=endpoint, **kwargs)
        self.assert_status(response, expected_status)
        return response.json()

    def put(self, endpoint, data, expected_status=200, **kwargs):
        response = self.wc_api.put(endpoint=endpoint, data=data, **kwargs)
        self.assert_status(response, expected_status)
        return response.json()
