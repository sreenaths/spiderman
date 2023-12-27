from os import path
from alive_progress import alive_bar;

from libs.source import SourceReader, File
from libs.db import Database
from libs.sink import write_csv, clean_dir
from libs.utils import print_stats

SOURCE_PATH = './source/spider.zip'
SINK_PATH = './dataset'
DATA_DIR = 'data'

def process_db(db_name: str, data: bytes) -> list[str]:
    processed_tables: list[str] = []

    with Database(data) as db:
        table_names = db.list_tables()

        for table_name in table_names:
            table_data = db.read_table(table_name)

            data_is_missing = len(table_data) > 1
            if data_is_missing:
                sync_file_path = path.join(SINK_PATH, DATA_DIR, db_name, f'{table_name}.csv')
                write_csv(sync_file_path, table_data)
                processed_tables.append(table_name)

    return processed_tables


def process_source(source_path) -> list:
    dbs = []

    with SourceReader(source_path) as source:
        files = source.list_files()

        with alive_bar(len(files)) as bar:
            for file in files:
                tables = process_db(file.name, source.read_file(file))
                dbs.append((file.name, tables))
                bar()

    return dbs


clean_dir(SINK_PATH)

print(f"\nBuilding dataset from {SOURCE_PATH}")
dbs = process_source(SOURCE_PATH)

print_stats(dbs)
