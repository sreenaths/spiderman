import os
from os import path


BASE_DIR = './dataset'


def path_to_data_dir(db_name: str) -> str:
    return path.join(BASE_DIR, db_name, 'data')


def path_to_data_file(db_name: str, table_name: str):
    return path.join(BASE_DIR, db_name, 'data', f'{table_name}.csv')


def path_to_schema_file(db_name: str) -> str:
    return path.join(BASE_DIR, db_name, 'schema.sql')


def path_to_train_queries_file(db_name: str) -> str:
    return path.join(BASE_DIR, db_name, 'train_queries.csv')


def path_to_test_queries_file(db_name: str) -> str:
    return path.join(BASE_DIR, db_name, 'test_queries.csv')


def scan():
    dbs_with_data = 0
    total_tables = 0
    dbs_with_train_queries = 0
    dbs_with_test_queries = 0

    db_names = os.listdir(BASE_DIR)

    if '.DS_Store' in db_names:
        db_names.remove('.DS_Store')

    for db_name in db_names:
        if path.exists(path_to_data_dir(db_name)):
            dbs_with_data += 1

        if path.exists(path_to_train_queries_file(db_name)):
            dbs_with_train_queries += 1

        if path.exists(path_to_test_queries_file(db_name)):
            dbs_with_test_queries += 1

        with open(path_to_schema_file(db_name)) as f:
            lines = f.read()
            total_tables += lines.count('CREATE TABLE')


    print("--- Dataset Stats ---")
    print("DBs in source: ", len(db_names))
    print("DBs with training queries: ", dbs_with_train_queries)
    print("DBs with test queries: ", dbs_with_test_queries)

    print("DBs with data: ", dbs_with_data)
    print("Total tables: ", total_tables)
