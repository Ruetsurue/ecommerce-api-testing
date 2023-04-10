import random

from helpers.db import DAO


class ProductsSQL:
    def __init__(self):
        self.db = DAO()

    def select_all_products_from_db(self):
        sql = "SELECT * FROM wp_posts WHERE `post_type`='product'"
        return self.db.execute_sql(sql).all()

    def select_all_products_after(self, after):
        sql = "SELECT * FROM wp_posts WHERE `post_type`='product' AND `post_date` > :after"
        binds = {"after": after}
        return self.db.execute_sql(sql, **binds).all()

    def select_product_by_id(self, product_id):
        sql = "SELECT * FROM wp_posts WHERE `post_type`='product' AND `ID`=:product_id"
        binds = {"product_id": str(product_id)}
        return self.db.execute_sql(sql, **binds).first()

    def select_random_product(self, limit=5000):
        sql = "SELECT * FROM wp_posts WHERE `post_type`='product' LIMIT :limit"
        binds = {"limit": limit}
        products = self.db.execute_sql(sql, **binds).all()
        product = random.choice(products)
        return product
