from tempfile import NamedTemporaryFile, _TemporaryFileWrapper
from sqlite3 import connect, Connection


ANSI_TYPE_MAP = {
    "TEXT": "VARCHAR(2000)", # TODO: Check the max length needed
    "BOOL": "BOOLEAN",
    "TINYINT UNSIGNED": "SMALLINT",
    "SMALLINT UNSIGNED": "SMALLINT",
    "MEDIUMINT UNSIGNED": "INT",
    "DOUBLE": "REAL",
    "BIT": "BOOLEAN",
    "YEAR": "INT", # As the value in it is an integer
    "DATETIME": "TIMESTAMP"
}

types_used = set()

def _get_ansi_type(col_type: str) -> str:
    col_type = col_type.upper()

    if not col_type:
        # Type is missing in sakila_1.film table, for rating & special_features columns
        col_type = "VARCHAR(64)"

    if col_type.startswith("INT"):
        col_type = "INT"

    if col_type.startswith("BIGINT"):
        col_type = "BIGINT"

    if col_type.startswith("NUMBER"):
        col_type = col_type.replace("NUMBER", "NUMERIC")

    if col_type.startswith("FLOAT"):
        col_type = col_type.replace("FLOAT", "DECIMAL")

    if col_type.startswith("VARCHAR2"):
        col_type = col_type.replace("VARCHAR2", "VARCHAR")

    if col_type.startswith("CHARACTER VARCHAR"):
        col_type = col_type.replace("CHARACTER VARCHAR", "VARCHAR")

    if col_type in ANSI_TYPE_MAP:
        col_type = ANSI_TYPE_MAP[col_type]

    types_used.add(col_type)

    return col_type

INDENTATION = "    "


class Database:
    data: bytes
    file: _TemporaryFileWrapper
    connection: Connection

    def __init__(self, data: bytes):
        self.data = data

    def __enter__(self):
        self.file = NamedTemporaryFile(suffix=".sqlite")
        self.file.write(self.data)
        self.file.seek(0)

        self.connection = connect(self.file.name, check_same_thread=False)
        self.connection.text_factory = lambda b: b.decode(errors = 'ignore')

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.file.close()
        self.connection.close()

    def list_tables(self) -> list[str]:
        cursor = self.connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        cursor.close()
        return [t[0] for t in tables]

    def _execute_pragma(self, command: str, table_name: str):
        cursor = self.connection.cursor()
        cursor.execute(f"PRAGMA {command}({table_name})")
        data = cursor.fetchall()
        cursor.close()
        return data

    def _build_column_definition(self, columns: list) -> list[str]:
        column_def = []

        for col in columns:
            col_name = col[1]
            col_type = col[2]
            col_notnull = col[3]
            col_default_val = col[4]

            col_type = _get_ansi_type(col_type)
            col_details = f"{INDENTATION}\"{col_name}\" {col_type}"

            if col_notnull:
                col_details = col_details + " NOT NULL"

            if col_default_val != None:
                # String literals in the schema must be enclosed in single quotes
                col_default_val = col_default_val.replace("\"", "'")
                col_details = col_details + f" DEFAULT {col_default_val}"

            column_def.append(col_details)

        return column_def

    def _build_primary_key_constraints(self, columns: list) -> list[str]:
        pk_constraints = []

        primary_keys = []
        for col in columns:
            col_name = col[1]
            col_pk = col[5]

            if col_pk:
                primary_keys.append(f"\"{col_name}\"")

        if primary_keys:
            primary_keys_str = ", ".join(primary_keys)
            pk_constraints.append(f"{INDENTATION}PRIMARY KEY ({primary_keys_str})")

        return pk_constraints

    def _build_foreign_key_constraints(self, table_name: str) -> list[str]:
        foreign_keys = self._execute_pragma('foreign_key_list', table_name)

        fk_composite = []
        # Aggregate composite foreign keys
        for fk in foreign_keys:
            seq = fk[1]
            from_column = f"\"{fk[3]}\""
            to_table = f"\"{fk[2]}\""
            to_column = f"\"{fk[4]}\""

            if fk[1] == 0:
                fk_composite.append(([from_column], to_table, [to_column]))
            else:
                # Composite foreign key columns are given as separate list items by pragma.
                # They must be merged, and following assert ensure that we are not making any invalid merges
                assert seq == len(fk_composite[-1][0]), "Invalid foreign key sequence"
                assert to_table == fk_composite[-1][1], "Invalid foreign key to_table"
                fk_composite[-1][0].append(from_column)
                fk_composite[-1][2].append(to_column)

        fk_constraints = []
        # Build foreign keys constraint
        for fk in fk_composite:
            from_column = ", ".join(fk[0])
            to_table = fk[1]
            to_column = ", ".join(fk[2])
            fk_constraints.append(f"{INDENTATION}FOREIGN KEY ({from_column}) REFERENCES {to_table} ({to_column})")

        return fk_constraints

    def _build_unique_constraints(self, table_name: str) -> list[str]:
        indexes = self._execute_pragma('index_list', table_name)

        unique_columns = []
        if indexes:
            for index in indexes:
                index_name = index[1]
                use_unique = index[2] == 1 and index[3] == 'u'
                # At index 2 - 1 = Unique, 0 = Not Unique
                # At index 3 - "u" indicates a unique index, and "c" indicates a unique index created to enforce a column constraint.
                # Note: Some unique constraints in cre_Drama_Workshop_Groups & cre_Theme_park would be dropped as they are primary keys
                if use_unique:
                    info = self._execute_pragma('index_info', index_name)[0]
                    unique_columns.append(info[2])

        unique_constraints = []
        for column_name in unique_columns:
            unique_constraints.append(f'{INDENTATION}UNIQUE ("{column_name}")')

        return unique_constraints

    def get_table_ddl(self, table_name: str) -> str:
        columns = self._execute_pragma('table_info', table_name)

        table_defs = []
        table_defs += self._build_column_definition(columns)
        table_defs += self._build_primary_key_constraints(columns)
        table_defs += self._build_foreign_key_constraints(table_name)
        table_defs += self._build_unique_constraints(table_name)

        defs_str = ",\n".join(table_defs)
        return f"""CREATE TABLE \"{table_name}\" (\n{defs_str}\n);"""

    def get_table_ddl1(self, name: str) -> str:
        cursor = self.connection.cursor()
        cursor.execute(f'SELECT sql FROM sqlite_master WHERE type="table" AND name="{name}"')
        ddl_str = cursor.fetchone()[0]
        cursor.close()
        return ddl_str

    def get_table_data(self, name: str, add_header: bool = True) -> list:
        data = []
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM {name};")

        if add_header:
            data.append([description[0] for description in cursor.description])

        rows = cursor.fetchall()
        for row in rows:
            decoded_row = tuple(cell.decode('utf-8', errors='replace') if isinstance(cell, bytes) else cell for cell in row)
            data.append(list(decoded_row))

        return data
