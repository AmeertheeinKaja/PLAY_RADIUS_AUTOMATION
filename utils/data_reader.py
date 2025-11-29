import json
import os

def load_test_data(filename):
    """Loads JSON test data from the testdata folder."""
    base_dir = os.path.join(os.getcwd(), "test_data")
    file_path = os.path.join(base_dir, filename)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Test data file not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)
