# More Dialects

## Apache Hive

### Install Dependent Libraries
```
pip install sasl thrift_sasl pyhive
```

### Load Dataset
```
python ./scripts/load_dataset.py 'hive://hive:<username>@<address>:10000?auth=CUSTOM'
```
