import json
import os


# ... existing code ...

def get_next_process_number():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Corrected "testdata" to "test_data"
    file_path = os.path.join(BASE_DIR, "test_data", "counter.json")

    # ... rest of the file ...

    print("Counter file path:", file_path)

    # Read JSON
    with open(file_path, "r") as f:
        data = json.load(f)

    # Increment
    data["process_counter"] += 1

    # Save back
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

    return data["process_counter"]
