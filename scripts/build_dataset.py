from libs.source import SourceFile

SOURCE_FILE_PATH = './source/spider.zip'

with SourceFile(SOURCE_FILE_PATH) as source:
    dbs = source.get_dbs()
    print('Databases found: ', len(dbs))

print("Building dataset...")
