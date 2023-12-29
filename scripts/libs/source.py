from zipfile import ZipFile
from pydantic import BaseModel


SOURCE_DIR = 'spider/database'
# Example sqlite file path: spider/database/academic/academic.sqlite


class File(BaseModel):
    name: str
    path: str


class SourceReader:
    path: str
    zip: ZipFile

    def __init__(self, path: str):
        self.path = path

    def __enter__(self):
        self.zip = ZipFile(self.path)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.zip.close()

    def list_files(self) -> list[File]:
        files = []
        file_list = self.zip.namelist()
        for file_path in file_list:
            if file_path.startswith(SOURCE_DIR) and file_path.endswith('.sqlite'):
                file_name = file_path.split("/")[2]
                files.append(File(name=file_name, path=file_path))
        return files

    def read_file(self, file: File) -> bytes:
        return self.zip.read(file.path)
