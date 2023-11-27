from zipfile import ZipFile
from pydantic import BaseModel

DB_DIR = 'spider/database'
# Example sqlite file path: spider/database/academic/academic.sqlite

class Database(BaseModel):
    name: str
    file_path: str

class SourceFile:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def __enter__(self):
        self.file = ZipFile(self.file_path)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.file.close()

    def get_dbs(self) -> list[Database]:
        dbs = []
        file_list = self.file.namelist()
        for file_path in file_list:
            if file_path.startswith(DB_DIR) and file_path.endswith('.sqlite'):
                db_name = file_path.split("/")[2]
                dbs.append(Database(name=db_name, file_path=file_path))
        return dbs
