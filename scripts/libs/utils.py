def print_stats(dbs: list):
    db_count = 0
    total_table_count = 0

    for db in dbs:
        table_count = len(db[1])
        if table_count > 0:
            total_table_count = total_table_count + table_count
            db_count = db_count + 1

    print("\n--- Stats ---")
    print("DBs in source: ", len(dbs))
    print("DBs with data: ", db_count)
    print("Total tables processed: ", total_table_count)
