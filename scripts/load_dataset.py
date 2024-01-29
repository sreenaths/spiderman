import sys

from alive_progress import alive_bar;

from core.target_db import TargetDB
from core.dataset import get_db_names, get_schema, get_table_names, get_data

url = sys.argv[1] if len(sys.argv) > 1 else None

if not url:
    print("""SpiderMan - load_dataset
Usage: python scripts/load_dataset.py <url> <dataset_dir>

Eg URL: hive://<address>:10000""")
    exit(1)

SKIP_DBS = ["baseball_1", "soccer_1", "wta_1"]
db_names = get_db_names()

db_names = [name for name in db_names if name not in SKIP_DBS]
with alive_bar(len(db_names)) as bar:
    for db_name in db_names:
        bar.text(f">> DB: {db_name}")
        with TargetDB(url, db_name) as db:
            schema = get_schema(db_name)
            db.execute(schema)

            table_names = get_table_names(db_name)
            for table_name in table_names:
                bar.text(f">> DB: {db_name} | Table: {table_name}")
                column_names, rows = get_data(db_name, table_name)

                bar.text(f">> DB: {db_name} | Table: {table_name} | Rows: {len(rows)}")
                db.insert(table_name, column_names, rows)
        bar()
