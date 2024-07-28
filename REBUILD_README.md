# SpiderMan - Rebuild
Recreate dataset from [Spider 1.0](https://yale-lily.github.io/spider) zip into `./dataset_source` directory. Current directory will be deleted and recreated.

### Download Source Zip
Download a copy of the original zip from HuggingFace into `./source` directory
```
python scripts/download_source.py
```
### Rebuild Dataset
```
python scripts/rebuild_dataset.py
```
9 databases from the source would be skipped as they do not have data. Skipped databases are imdb, formula_1, music_2, yelp, academic, restaurants, scholar, sakila_1, geo.