import os
from requests_oauthlib import OAuth1


class CredentialHelper:

    @classmethod
    def get_wc_keys(cls):
        creds = {
            "client_key": os.getenv('CONSUMER_KEY'),
            "client_secret": os.getenv('CONSUMER_SECRET'),
        }

        return creds

    @classmethod
    def get_oauth1(cls):
        return OAuth1(**cls.get_wc_keys())
