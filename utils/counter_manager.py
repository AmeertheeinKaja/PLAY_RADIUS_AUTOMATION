import json
import os

def get_next_process_number():
    counter_path = os.path.join("testdata", "counter.json")

    # Ensure the file exists
    if not os.path.exists(counter_path):
        with open(counter_path, "w") as f:
            json.dump({"process_counter": 0}, f, indent=2)

    # Read current counter
    with open(counter_path, "r") as f:
        counter = json.load(f)

    # Increment and save
    counter["process_counter"] += 1
    with open(counter_path, "w") as f:
        json.dump(counter, f, indent=2)

    return counter["process_counter"]
