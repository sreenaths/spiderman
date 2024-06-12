# SpiderMan
A comprehensive, high quality, human-annotated plain-text dataset for SQL AI tasks across diverse domains and complexity levels.

## Why SpiderMan
SpiderMan is an improved version of the [Spider 1.0](https://yale-lily.github.io/spider) dataset.

- The databases are made available in plain-text format instead of a set of sqlite files. This makes it easy for you to load the dataset into any database of your choice.
- Schema has been standardized - Corrected table ordering, column data-types, primary / foreign key constraints and indexes.
- Data has been corrected for schema based validations.
- Queries have been improved for successful execution in MySQL and other DB systems.

SpiderMan is split into 2 parts - Dataset and scripts.

## Dataset
The dataset comprises of 157 databases. Each of them come with their own respective schema, data and queries. We currently do not have queries that span across databases. Train-test split happens at the database level.

||Queries|Tables|Databases|
|-|-|-|-|
|Train|6726|699|137|
|Test|1034|80|20|
|Total|7760|779|157|

## Scripts
The scripts provided below make it easy to use the dataset. Follow the [Setup](#setup) section to get your system ready to run these scripts.

### Load Dataset
Creates schema of all the databases, and insert their data into a DB system. It accepts one argument - A SQLAlchemy 2.0 compatible URL to the destination database. More details on the URL is available [here](https://docs.sqlalchemy.org/en/20/core/engines.html#database-urls).
```
python scripts/load_dataset.py 'mysql://<username>:<password>@<host>:3306'

Eg: python ./scripts/load_dataset.py 'mysql://spiderman:spiderman@127.0.0.1:3306'
```

### Validate Queries
Once the dataset is loaded, you can run the following script to execute the queries. It checks successful completion of all the queries. Query results are not verified at this point.
```
python scripts/validate_queries.py 'mysql://<username>:<password>@<host>:3306'

Eg: python ./scripts/validate_queries.py 'mysql://spiderman:spiderman@127.0.0.1:3306'
```

### Scan Dataset
Following scripts goes through the dataset and aggregates various stats.
```
python scripts/scan_dataset.py
```

### Rebuild Dataset
Recreate dataset from [Spider 1.0](https://yale-lily.github.io/spider) zip. Current files in `./dataset` directory will be overwritten.
```
# Download a copy of the original zip from HuggingFace into ./source directory
python ./scripts/download_source.py

# Rebuild
python ./scripts/rebuild_dataset.py
```
9 databases from the source would be skipped as they do not have data - imdb, formula_1, music_2, yelp, academic, restaurants, scholar, sakila_1, geo.

## Setup
Following commands are for macOS.

### Create Environment
```
conda create --name spiderman-env python=3.12.2
conda activate spiderman-env
```

### Setup MySQL
```
# Install MySQL server
brew install mysql pkg-config

# Install MySQL library
pip install mysqlclient

# Create user and set privileges
mysql -u root
> CREATE USER 'spiderman'@'localhost' IDENTIFIED BY 'spiderman';
> GRANT ALL PRIVILEGES ON *.* TO 'spiderman'@'localhost';
```

### Install Dependencies
```
pip install -r requirements.txt
```

# Citation

If you find this to be useful, please consider citing:
```
@inproceedings{SpiderMan,
  title  = {SpiderMan: A Comprehensive Human-Annotated Dataset for SQL AI Tasks Across Diverse Domains and Complexity Levels},
  author = {Sreenath Somarajapuram},
  year   = 2024
}
```
SpiderMan is a refined version of the [Spider dataset](https://yale-lily.github.io/spider).
```
@inproceedings{Yu&al.18c,
  title     = {Spider: A Large-Scale Human-Labeled Dataset for Complex and Cross-Domain Semantic Parsing and Text-to-SQL Task},
  author    = {Tao Yu and Rui Zhang and Kai Yang and Michihiro Yasunaga and Dongxu Wang and Zifan Li and James Ma and Irene Li and Qingning Yao and Shanelle Roman and Zilin Zhang and Dragomir Radev}
  booktitle = "Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing",
  address   = "Brussels, Belgium",
  publisher = "Association for Computational Linguistics",
  year      = 2018
}
```

# License
- Dataset license : [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/legalcode)
- Scripts license : [Apache 2.0](https://apache.org/licenses/LICENSE-2.0.txt)
