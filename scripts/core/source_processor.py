from os import path
import json
from alive_progress import alive_bar;

import core.dataset as dataset
from core.source_db import SourceDB, types_used

from utils.zip import ZipReader
from utils.filesystem import write_csv, write_str


# Source paths
SOURCE_PATH = './source/spider.zip'

DB_SOURCE_DIR = 'spider/database'
TRAIN_DATA_1 = 'spider/train_spider.json'
TRAIN_DATA_2 = 'spider/train_others.json'
TEST_DATA = 'spider/dev.json'

def write_schema(table_names: list[str], db: SourceDB):
    table_ddls = []
    for table_name in table_names:
        ddl = db.get_table_ddl(table_name)
        # ddl = db.get_original_table_ddl(table_name) # Used for schema debugging
        table_ddls.append(ddl)

    file_path = dataset.path_to_schema_file(db.name)
    #file_path = path.join("./schema", f"{db.name}.sql") # Used for schema debugging

    schema = "\n\n".join(table_ddls)
    schema = schema + "\n" # New line at EOF
    write_str(file_path, schema)


def write_data(table_names: list[str], db: SourceDB):
    data_dir = dataset.path_to_data_dir(db.name)

    for table_name in table_names:
        table_data = db.get_table_data(table_name)

        data_is_missing = len(table_data) > 1 # 1st row is always header
        if data_is_missing:
            file_path = path.join(data_dir, f'{table_name}.csv')
            write_csv(file_path, table_data)


def process_db(db_name: str, data: bytes):
    with SourceDB(db_name, data) as db:
        table_names = db.list_tables()
        write_schema(table_names, db)
        write_data(table_names, db)


def process_queries(db_name: str, queries: list, file_path: str):
    filtered_queries = [["question", "sql"]]
    for query in queries:
        if query["db_id"] == db_name:
            filtered_queries.append([query["question"], query["query"]])

    if len(filtered_queries) > 1:
        write_csv(file_path, filtered_queries)


def process_source():
    print(f"\nBuilding dataset from {SOURCE_PATH}")

    with ZipReader(SOURCE_PATH) as source:
        train_queries = json.loads(source.read_file(TRAIN_DATA_1))
        train_queries += json.loads(source.read_file(TRAIN_DATA_2))
        test_queries = json.loads(source.read_file(TEST_DATA))

        # Example sqlite file path: spider/database/academic/academic.sqlite
        files = source.list_sqlite_files_in(DB_SOURCE_DIR)
        with alive_bar(len(files)) as bar:
            for file in files:
                file_data = source.read_file(file.path)
                db_name = file.name
                process_db(db_name, file_data)
                process_queries(db_name, train_queries, dataset.path_to_train_queries_file(db_name))
                process_queries(db_name, test_queries, dataset.path_to_test_queries_file(db_name))
                bar()

    #print("Datatypes in use: ", types_used) # Used for schema debugging
