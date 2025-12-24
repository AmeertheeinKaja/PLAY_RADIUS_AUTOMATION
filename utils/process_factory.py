from pages.process.process_manager.create_process import CreateProcess
from utils.data_reader import load_test_data
from utils.counter_manager import get_next_process_number

def create_process_from_json(driver, json_path="process/create_process.json"):
    data = load_test_data(json_path)

    process_number = get_next_process_number()

    process_code = f"{data['process_code']}{process_number}"
    process_name = f"{data['process_name']}{process_number}"

    page = CreateProcess(
        driver,
        process_code=process_code,
        process_name=process_name,
        review_rating=data.get("review_rating", False),
        channels=data.get("channels", [])
    )

    return page
