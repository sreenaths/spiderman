from pandas import DataFrame
from typing import Callable

from urllib.parse import urlparse, urlunparse

from sqlalchemy import create_engine, text
from sqlalchemy_utils import database_exists, create_database, drop_database


# Wrapper around SQLAlchemy for interacting with external databases
class TargetDB:
    url: str
    db_name: str
    dialect: str
    reset: bool
    preprocessor: Callable[[str], str]

    def __init__(self, url: str, db_name: str, reset: bool = False):
        self.url = urlunparse(urlparse(url)._replace(path=db_name))
        self.reset = reset
        self.db_name = db_name

    def __enter__(self):
        if not database_exists(self.url):
            create_database(self.url)
        elif self.reset:
            drop_database(self.url)
            create_database(self.url)

        self.engine = create_engine(self.url)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return

    def execute_statements(self, statements: list[str]):
        with self.engine.connect() as conn:
            for stmt in statements:
                conn.execute(text(stmt))
            conn.commit()

    def execute(self, sql: str):
        db_stmts = sql.split(";")
        statements = []
        for stmt in db_stmts:
            stmt = stmt.strip()
            if stmt: statements.append(stmt)

        self.execute_statements(statements)

    def insert(self, table_name: str, df: DataFrame, batch_size: int = 500):
        try:
            df.to_sql(table_name, con=self.engine, if_exists='append', index=False, chunksize = batch_size)
        except Exception as e:
            print(f"Error inserting data - DB: {self.db_name} Table: {table_name}")
            raise e
