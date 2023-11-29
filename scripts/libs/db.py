from tempfile import NamedTemporaryFile, _TemporaryFileWrapper
from sqlite3 import connect, Connection

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

    def read_table(self, name: str, add_header: bool = True) -> list:
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
