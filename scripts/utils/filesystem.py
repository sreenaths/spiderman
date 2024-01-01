import csv
import os
import shutil


def clean_dir(path: str):
    if os.path.isdir(path):
        shutil.rmtree(path)


def create_missing_dir(file_path: str):
    output_directory = os.path.dirname(file_path)
    os.makedirs(output_directory, exist_ok=True)


def write_str(file_path: str, data: str):
    create_missing_dir(file_path)

    with open(file_path, "w", newline='') as str_file:
        str_file.write(data)


def write_csv(file_path: str, data: list[list]):
    create_missing_dir(file_path)

    with open(file_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(data)
