from helpers.api.customers import CustomerAPI
from helpers.sql.customers import CustomerSQL


class CustomerHelper:
    def __init__(self):
        self.api = CustomerAPI()
        self.sql = CustomerSQL()

    def create_customer(self, **kwargs):
        return self.api.create_customer(**kwargs)

    def create_customer_with_existing_email(self, **kwargs):
        return self.api.create_customer_with_existing_email(**kwargs)

    def list_all_customers(self, per_page=100):
        return self.api.list_all_customers(per_page=per_page)

    def select_cust_from_db_by_email(self, email):
        return self.sql.select_cust_from_db_by_email(email=email)

    def select_all_db_customers(self):
        return self.sql.select_all_db_customers()
