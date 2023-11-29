from libs.source import SourceReader, File
from libs.db import Database
from libs.sink import write_csv, delete_dir
from os import path

SINK_PATH = '../dataset'
def process_db(db_name: str, data: bytes):
    print(f"Processing file: {db_name}")

    with Database(data) as db:
        table_names = db.list_tables()

        for table_name in table_names:
            print(f"Writing data for {table_name}...")
            table_data = db.read_table(table_name)

            sync_file_path = path.join(SINK_PATH, db_name, f'{table_name}.csv')
            write_csv(sync_file_path, table_data)
            print("Done")


SOURCE_PATH = './source/spider.zip'
def process_source():
    with SourceReader(SOURCE_PATH) as source:
        files = source.list_files()
        print('Files found: ', len(files))

        for file in files:
            process_db(file.name, source.read_file(file))

delete_dir(SINK_PATH)
process_source()
