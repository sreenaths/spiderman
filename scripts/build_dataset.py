from core.source_processor import process_source
import core.dataset as dataset

from utils.filesystem import clean_dir


# Cleanup dataset
clean_dir(dataset.BASE_DIR)
print(f'Cleanup: {dataset.BASE_DIR} directory and its contents deleted.')

# Rebuild dataset
process_source()
print("Build completed successfully.")

# Scan generated dataset and print stats
print("\n")
dataset.scan()
