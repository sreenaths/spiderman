from os import path
from alive_progress import alive_bar;

from libs.source import SourceReader, File
from libs.db import Database, types_used
from libs.sink import write_csv, clean_dir, write_str
from libs.utils import print_stats


SOURCE_PATH = './source/spider.zip'
SINK_PATH = './dataset'

DATA_DIR = 'data'
SCHEMA_FILE_NAME = 'schema.sql'

TABLE_SKIPLIST = ['sqlite_sequence']


def write_schema(table_names: list[str], db: Database, db_sink_path: str,
                 ):
    table_ddls = []

    for table_name in table_names:
        if table_name not in TABLE_SKIPLIST:
            table_ddls.append(db.get_table_ddl(table_name))

    file_path = path.join(db_sink_path, SCHEMA_FILE_NAME)
    #file_path = path.join("./schema_f", f"{db_name}.sql")

    schema = "\n\n".join(table_ddls)
    schema = schema + "\n" # New line at EOF
    write_str(file_path, schema)


def write_data(table_names: list[str], db: Database, db_sink_path: str) -> list[str]:
    processed_tables: list[str] = []

    for table_name in table_names:
        table_data = db.get_table_data(table_name)

        data_is_missing = len(table_data) > 1
        if data_is_missing:
            file_path = path.join(db_sink_path, DATA_DIR, f'{table_name}.csv')
            write_csv(file_path, table_data)
            processed_tables.append(table_name)

    return processed_tables


def write_queries(db_name: str):
    return


def process_db(db_name: str, data: bytes) -> list[str]:
    db_sink_path = path.join(SINK_PATH, db_name)

    with Database(data) as db:
        table_names = db.list_tables()

        write_schema(table_names, db, db_sink_path, db_name)

        return write_data(table_names, db, db_sink_path)


def process_source(source_path) -> list:
    dbs = []

    with SourceReader(source_path) as source:
        files = source.list_files()

        with alive_bar(len(files)) as bar:
            for file in files:
                file_data = source.read_file(file)
                tables = process_db(file.name, file_data)
                dbs.append((file.name, tables))
                bar()

    return dbs


clean_dir(SINK_PATH)

print(f"\nBuilding dataset from {SOURCE_PATH}")
dbs = process_source(SOURCE_PATH)
#print("Datatypes in use: ", types_used)

print_stats(dbs)
