import os

from sqlalchemy.engine import create_engine, Engine
from sqlalchemy import text


class DAO:
    def __init__(self):
        db_url = os.getenv('DB_URL')
        self.engine: Engine = create_engine(db_url)

    def execute_sql(self, statement, **binds):
        statement = text(statement)
        with self.engine.connect() as conn:
            result = conn.execute(statement, **binds)
        return result
