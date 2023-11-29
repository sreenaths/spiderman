import csv
import os
import shutil

def write_csv(file_path: str, data: list[list]):
    output_directory = os.path.dirname(file_path)
    os.makedirs(output_directory, exist_ok=True)

    with open(file_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(data)


def delete_dir(path: str):
    if os.path.isdir(path):
        shutil.rmtree(path)
        print(f'Directory and its contents deleted: {path}')
