from helpers.db import DAO


class CustomerSQL:

    def __init__(self):
        self.db = DAO()

    def select_cust_from_db_by_email(self, email):
        sql = "SELECT * FROM wp_users WHERE `user_email` = :email ORDER BY `user_registered` DESC"
        return self.db.execute_sql(sql, email=email).first()

    def select_all_db_customers(self):
        sql = "SELECT * FROM wp_users"
        return self.db.execute_sql(sql).all()
