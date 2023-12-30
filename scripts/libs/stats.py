import os
import os.path as path

from configs import SINK_PATH, SCHEMA_FILE_NAME, DATA_DIR


def print_stats():
    dbs_with_data = 0
    total_tables = 0
    dbs_with_train_queries = 0
    dbs_with_test_queries = 0

    db_names = os.listdir(SINK_PATH)

    if '.DS_Store' in db_names:
        db_names.remove('.DS_Store')

    for db_name in db_names:
        if path.exists(path.join(SINK_PATH, db_name, DATA_DIR)):
            dbs_with_data += 1

        if path.exists(path.join(SINK_PATH, db_name, 'train_queries.csv')):
            dbs_with_train_queries += 1

        if path.exists(path.join(SINK_PATH, db_name, 'test_queries.csv')):
            dbs_with_test_queries += 1

        with open(path.join(SINK_PATH, db_name, SCHEMA_FILE_NAME)) as f:
            lines = f.read()
            total_tables += lines.count('CREATE TABLE')


    print("--- Stats ---")
    print("DBs in source: ", len(db_names))
    print("DBs with training queries: ", dbs_with_train_queries)
    print("DBs with test queries: ", dbs_with_test_queries)

    print("DBs with data: ", dbs_with_data)
    print("Total tables: ", total_tables)
