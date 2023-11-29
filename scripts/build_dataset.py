from os import path
from yaspin import yaspin

from libs.source import SourceReader, File
from libs.db import Database
from libs.sink import write_csv, delete_dir
from libs.utils import print_stats

SINK_PATH = '../dataset'
def process_db(db_name: str, data: bytes) -> list[str]:
    processed_tables: list[str] = []

    with Database(data) as db:
        table_names = db.list_tables()

        for table_name in table_names:
            table_data = db.read_table(table_name)

            data_is_missing = len(table_data) > 1
            if data_is_missing:
                sync_file_path = path.join(SINK_PATH, db_name, f'{table_name}.csv')
                write_csv(sync_file_path, table_data)
                processed_tables.append(table_name)

    return processed_tables


SOURCE_PATH = './source/spider.zip'
def process_source() -> list:
    dbs = []

    with SourceReader(SOURCE_PATH) as source:
        files = source.list_files()

        for file in files:
            tables = process_db(file.name, source.read_file(file))
            dbs.append((file.name, tables))

    return dbs


delete_dir(SINK_PATH)
with yaspin(text="Processing..."):
    dbs = process_source()
print_stats(dbs)
