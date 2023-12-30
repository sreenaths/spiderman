from os import path
import json
from alive_progress import alive_bar;

from libs.zip import ZipReader
from libs.db import Database, types_used
from libs.file import write_csv, clean_dir, write_str
from libs.stats import print_stats

from configs import SINK_PATH, SOURCE_PATH, SCHEMA_FILE_NAME, DATA_DIR, TRAIN_DATA_1, TRAIN_DATA_2, TEST_DATA


def write_schema(table_names: list[str], db: Database, db_sink_path: str):
    table_ddls = []

    for table_name in table_names:
        ddl = db.get_table_ddl(table_name)
        # ddl = db.get_original_table_ddl(table_name) # Used for schema debugging
        table_ddls.append(ddl)

    file_path = path.join(db_sink_path, SCHEMA_FILE_NAME)
    #file_path = path.join("./schema", f"{db.name}.sql") # Used for schema debugging

    schema = "\n\n".join(table_ddls)
    schema = schema + "\n" # New line at EOF
    write_str(file_path, schema)


def write_data(table_names: list[str], db: Database, db_sink_path: str):
    for table_name in table_names:
        table_data = db.get_table_data(table_name)

        data_is_missing = len(table_data) > 1 # 1st row is always header
        if data_is_missing:
            file_path = path.join(db_sink_path, DATA_DIR, f'{table_name}.csv')
            write_csv(file_path, table_data)


def process_db(db_name: str, data: bytes):
    db_sink_path = path.join(SINK_PATH, db_name)

    with Database(db_name, data) as db:
        table_names = db.list_tables()
        write_schema(table_names, db, db_sink_path)
        write_data(table_names, db, db_sink_path)


def process_queries(db_name: str, queries: list, type: str):
    filtered_queries = [["question", "sql"]]
    for query in queries:
        if query["db_id"] == db_name:
            filtered_queries.append([query["question"], query["query"]])

    if len(filtered_queries) > 1:
        file_path = path.join(SINK_PATH, db_name, f'{type}_queries.csv')
        write_csv(file_path, filtered_queries)


def process_source(source_path):
    with ZipReader(source_path) as source:
        train_queries = json.loads(source.read_file(TRAIN_DATA_1))
        train_queries += json.loads(source.read_file(TRAIN_DATA_2))
        test_queries = json.loads(source.read_file(TEST_DATA))

        files = source.list_files()
        with alive_bar(len(files)) as bar:
            for file in files:
                file_data = source.read_file(file.path)
                process_db(file.name, file_data)
                process_queries(file.name, train_queries, "train")
                process_queries(file.name, test_queries, "test")
                bar()


clean_dir(SINK_PATH)

print(f"\nBuilding dataset from {SOURCE_PATH}")
process_source(SOURCE_PATH)
#print("Datatypes in use: ", types_used) # Used for schema debugging

print("\n")
print_stats()
