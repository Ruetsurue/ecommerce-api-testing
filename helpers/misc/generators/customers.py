import logging
import random
from string import digits, ascii_letters


class CustomerInfoGenerator:

    @classmethod
    def gen_email(cls, email_prefix='', email_domain="ecom.com", email_len=10, **kwargs):
        email_subname = ''.join(random.choices(ascii_letters, k=email_len))
        email = f"{email_subname}@{email_domain}"

        if email_prefix:
            email = f"{email_prefix}_{email}"

        logging.debug(msg=f"Generated email: {email}")
        return email

    @classmethod
    def gen_password(cls, passwd_len=8, **kwargs):
        symbols = ascii_letters + digits
        passwd = ''.join(random.choices(symbols, k=passwd_len))
        logging.debug(msg=f"Generated passwd: {passwd}")
        return passwd
