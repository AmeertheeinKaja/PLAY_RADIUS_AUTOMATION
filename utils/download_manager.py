import shutil
from pathlib import Path

def clear_downloads_folder(folder="tests/downloads"):
    folder_path = Path(folder)
    if folder_path.exists():
        shutil.rmtree(folder_path)
    folder_path.mkdir(parents=True, exist_ok=True)
