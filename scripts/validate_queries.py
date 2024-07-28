"""Try running queries on the target database, and validate they can be successfully executed"""

import sys
from alive_progress import alive_bar

from core.target_db import TargetDB
from core.dataset import DatasetDir
from utils.filesystem import read_csv
from utils.args import get_args


args = get_args("Validate successful execution of all queries on the target database")

dataset = DatasetDir()
db_names = dataset.get_db_names()

print("Executing queries...")
with alive_bar(len(db_names)) as progress:
    for db_name in db_names:

        progress.text(f">> DB: {db_name}")
        with TargetDB(args.url, db_name) as db:
            queries_file_path = dataset.path_to_queries_file(db_name)
            replaced_queries_file_path = queries_file_path[:-3] + "csv"
            queries = read_csv(replaced_queries_file_path)[1:]

            count = len(queries)
            for idx, query in enumerate(queries):
                progress.text(f">>>>> DB: {db_name} | {idx} | Query: {idx}/{count}")
                try:
                    db.execute(query[1])
                except Exception as e:
                    print(e)
                    print("Details: ", db_name, idx, query[0], query[1])
                    sys.exit()

        progress() # pylint: disable=not-callable

print("Validation successful.")
