from typing import Callable

from sqlalchemy import create_engine, text
from sqlalchemy_utils import database_exists, create_database

from core.source_processor import TABLE_DELIM


def _get_dialect(url: str) -> str:
    dialect = url.split(":")[0]
    dialect = dialect.split("+")[0]
    return dialect

def _sql_preprocess_default(sql: str) -> str:
    return sql

def _sql_preprocess_hive(sql: str) -> str:
    sql = sql.replace('"', '`')
    sql = sql.replace('\'', '"')
    sql = sql.replace('NOT NULL DEFAULT', 'DEFAULT')

    sql = sql.replace(" DEFAULT NULL", "")
    # sql = sql.replace(" DEFAULT ''", "")
    # sql = sql.replace(" DEFAULT 'G'", "")
    # sql = sql.replace(" DEFAULT 'F'", "")
    # sql = sql.replace(" DEFAULT 'Asia'", "")

    sql = sql.replace("BLOB", "BINARY")
    sql = sql.replace("SMALLINT", "INT")

    processed_lines = []
    lines = sql.split("\n")

    for line in lines:
        ls_line = line.lstrip()
        if (ls_line.startswith("PRIMARY KEY") or
            ls_line.startswith("NOT NULL") or
            ls_line.startswith("UNIQUE")):
            if line[-1] == ",":
                line = line[:-1] + " DISABLE NOVALIDATE,"
            else:
                line = line + " DISABLE NOVALIDATE"

        # Temporary Hack to get it working with Hive
        if ls_line.startswith("FOREIGN KEY"):
            line = None

        if line != None:
            processed_lines.append(line)

    sql = "\n".join(processed_lines)

    # Fix issue created by above hack
    sql = sql.replace(",\n)", "\n)")

    return sql


# Wrapper around SQLAlchemy for interacting with external databases
class TargetDB:
    url: str
    dialect: str
    preprocessor: Callable[[str], str]

    def __init__(self, url: str):
        self.url = url
        self.dialect = _get_dialect(url)

        if self.dialect == "hive":
            self.preprocessor = _sql_preprocess_hive
        else:
            self.preprocessor = _sql_preprocess_default

    def __enter__(self):
        if not database_exists(self.url):
            create_database(self.url)

        self.engine = create_engine(self.url)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return

    def drop_tables(self, table_names: list[str]):
        conn = self.engine.connect()
        for table_name in table_names:
            sql = self.preprocessor(f'DROP TABLE "{table_name}"')
            conn.execute(text(sql))
        conn.commit()
        conn.close()

    def execute(self, sql: str):
        conn = self.engine.connect()
        sql = self.preprocessor(sql)
        stmts = sql.split(TABLE_DELIM)
        for stmt in stmts:
            stmt = stmt.strip()
            if stmt[-1] == ";":
                stmt = stmt[:-1]
            print(">>>>", stmt)
            conn.execute(text(stmt))
        conn.commit()
        conn.close()
