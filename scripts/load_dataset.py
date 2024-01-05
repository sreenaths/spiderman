import sys

from alive_progress import alive_bar;

from core.target_db import TargetDB
from core.dataset import get_db_names, get_table_names, get_schema


url = sys.argv[1] if len(sys.argv) > 1 else None

if not url:
    print("""SpiderMan - load_dataset
Usage: python scripts/load_dataset.py <url>

load_dataset.py makes it simple to load dataset into any database supported by SQLAlchemy, and expects SQLAlchemy database URL as argument.
More details on the URL is available at https://docs.sqlalchemy.org/en/20/core/engines.html#database-urls.""")
    exit(1)

db_names = get_db_names()
db_names = db_names[140:]
with alive_bar(len(db_names)) as bar:
    for db_name in db_names:
        with TargetDB(f"{url}/{db_name}") as db:
            table_names = get_table_names(db_name)
            db.drop_tables(table_names)

            schema = get_schema(db_name)
            db.execute(schema)
        bar()
