from pytest import mark
from requests import Response

from helpers.entities.customers import CustomerHelper
from helpers.misc.generators.customers import CustomerInfoGenerator as ci
from configs.set_env import create_test_enviroment


@mark.customer
class TestCustomer:
    @mark.tcid29
    def test_create_customer_only_email_passwd(self):
        ch = CustomerHelper()
        email, password = ci.gen_email(email_prefix='tcid29'), ci.gen_password()
        response: Response = ch.create_customer(email=email, password=password)

        assert email == response['email'], "Emails don't match"

        cust_db_record = ch.select_cust_from_db_by_email(email=email)
        cust_db_email = cust_db_record.user_email
        assert cust_db_email == email, "Email in db doesn't match"

    @mark.tcid30
    def test_list_all_customers(self):
        ch = CustomerHelper()
        all_api_customers = ch.list_all_customers(per_page=100)
        all_db_customers = ch.select_all_db_customers()
        assert len(all_api_customers) == len(all_db_customers), "Number of customers in API and DB doesn't match"

    @mark.negative
    @mark.tcid24
    def test_create_customer_with_existing_email(self):
        ch = CustomerHelper()
        email, password = ci.gen_email(email_prefix='tcid29'), ci.gen_password()
        new_customer: Response = ch.create_customer(email=email, password=password)

        # create customer again with the same data
        repeat_customer: Response = ch.create_customer_with_existing_email(email=email, password=password)
        customer_exists_conflict_code = "registration-error-email-exists"
        err_msg = f"Expected conflict code {customer_exists_conflict_code}, got: {repeat_customer['code']}"
        assert repeat_customer["code"] == customer_exists_conflict_code, err_msg

        duplicate_err_text = "An account is already registered with your email address"
        err_msg = f"Error text should contain {duplicate_err_text}, but it doesn't"
        assert repeat_customer["message"].find(duplicate_err_text) != -1, err_msg
