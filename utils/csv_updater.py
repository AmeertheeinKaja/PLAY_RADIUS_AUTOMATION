import json
import csv
import random
import string
import time
import uuid
from pathlib import Path

def update_csv_with_json(csv_path: str, json_path: str, output_path: str | None = None) -> str:
    csv_path = Path(csv_path)
    json_path = Path(json_path)
    output_path = Path(output_path) if output_path else csv_path

    # Extract process name from filename
    process_name = extract_process_name(csv_path.name)

    # 1. Read JSON
    with json_path.open("r", encoding="utf-8") as jf:
        json_data = json.load(jf)

    json_headers = json_data.get("headers", {}).copy()

    # ✅ Always update dynamic fields
    json_headers["process"] = process_name
    json_headers["recordId"] = generate_unique_record_id()
    json_headers["xsess.xsessid"] = generate_xsess_id()

    # 2. Read existing CSV
    with csv_path.open("r", newline='', encoding="utf-8") as cf:
        reader = csv.DictReader(cf)
        rows = list(reader)
        csv_headers = reader.fieldnames or []

    # 3. Merge headers
    updated_headers = list(csv_headers)
    for key in json_headers.keys():
        if key not in updated_headers:
            updated_headers.append(key)

    # 4. Update rows
    for row in rows:
        for key, value in json_headers.items():
            row[key] = value

    # 5. Write file
    with output_path.open("w", newline='', encoding="utf-8") as wf:
        writer = csv.DictWriter(wf, fieldnames=updated_headers)
        writer.writeheader()
        writer.writerows(rows)

    return str(output_path)



def extract_process_name(file_name: str) -> str:
    """
    Extracts full process name from filename.
    Example:
    68ad48afb7_SMK_PLAY_24OCT_A.csv → SMK_PLAY_24OCT_A
    """
    file_name = file_name.replace(".csv", "")
    parts = file_name.split("_", 1)  # split at first underscore only
    return parts[1] if len(parts) > 1 else ""

def generate_unique_record_id(prefix="SS") -> str:
    """
    Generates a unique recordId using epoch time + random suffix.
    Example: SS1753539105906_4831
    """
    millis = int(time.time() * 1000)
    suffix = ''.join(random.choices(string.digits, k=4))
    return f"{prefix}{millis}_{suffix}"

def generate_xsess_id() -> str:
    return uuid.uuid4().hex