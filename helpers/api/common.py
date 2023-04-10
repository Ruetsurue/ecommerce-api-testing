import json
import logging
import os
import requests

from configs.hosts import API_HOSTS
from helpers.credentials import CredentialHelper as ch


class RequestsUtility:

    def __init__(self):
        self.env = os.getenv('ENV', 'test')
        self.base_url = API_HOSTS[self.env]
        self.auth = ch.get_oauth1()

    def assert_response_code(self, expected, actual):
        error_msg = f"Expected status code {expected}, actual: {actual}"
        assert expected == actual, error_msg

    def get(self, endpoint, params=None, payload=None, headers=None, expected_response_code=200):
        url = f"{self.base_url}{endpoint}"

        if not headers:
            headers = {"Content-Type": "application/json"}

        logging.debug(f"using url: {url}")
        response = requests.get(url=url, params=params, data=json.dumps(payload), headers=headers, auth=self.auth)
        self.assert_response_code(expected_response_code, response.status_code)

        return response.json()

    def get_api_records_by_pages(self, endpoint, **request_params):
        result = []
        max_pages = 1000

        if 'per_page' not in request_params:
            request_params['per_page'] = 100

        for page_num in range(1, max_pages + 1):
            logging.debug(f"Product batch: {page_num}")
            request_params['page'] = page_num
            data_batch = self.get(endpoint=endpoint, params=request_params)

            if not data_batch:
                logging.debug(f"Exiting at batch: {page_num}")
                return result
            result.extend(data_batch)

    def post(self, endpoint, payload=None, headers=None, expected_response_code=201):
        url = f"{self.base_url}{endpoint}"

        if not headers:
            headers = {"Content-Type": "application/json"}

        logging.debug(f"using url: {url}")
        response = requests.post(url=url, data=json.dumps(payload), headers=headers, auth=self.auth)
        self.assert_response_code(expected_response_code, response.status_code)

        return response.json()

    def put(self, endpoint, params=None, payload=None, headers=None, expected_response_code=200):
        url = f"{self.base_url}{endpoint}"

        if not headers:
            headers = {"Content-Type": "application/json"}

        logging.debug(f"using url: {url}")
        response = requests.put(url=url, data=payload, params=params, headers=headers, auth=self.auth)
        import pdb; pdb.set_trace()
        self.assert_response_code(expected_response_code, response.status_code)
        return response.json()
