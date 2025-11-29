import time
from pathlib import Path

from selenium.webdriver.common.by import By
from pages.common.loader import Loader
from pages.base_page import BasePage
from utils.logger import get_logger

from utils.data_reader import load_test_data
from utils.screenshot import Screenshot
from utils.csv_updater import update_csv_with_json

data = load_test_data("uploadRecord.json")


logger = get_logger(__name__)


class UploadRecord(BasePage):
    TAB_CONTACT_SCHEMA = (By.XPATH, "//*[@id='accordionExample']/ul/ul[5]/li/button/span[2]")
    UPLOAD_INPUT = (By.XPATH, "//input[@type='file']")
    TEMPLATE_BTN=(By.XPATH,"//button[@title='Download Template']")
    SUBMIT_BTN=(By.XPATH,"//span[text()='Submit']")
    RESET_BTN=(By.XPATH,"//button[text()='Reset']")
    CLOSE_BTN=(By.XPATH,"//button[@title='Close']")


    def __init__(self, driver):
        super().__init__(driver)
        self.loader = Loader(driver)
        self.filepath=data["filepath"]
    def open_upload(self):
        tab_contact=self.wait_until_clickable(self.TAB_CONTACT_SCHEMA)
        tab_contact.click()
        self.loader.load()
        logger.info("Upload record page showing")
        Screenshot.take(self.driver,f"Upload record page showing")

    def submit(self):
        submit_btn=self.wait_until_clickable(self.SUBMIT_BTN)
        submit_btn.click()
        logger.info(f"Submit button clicked")

    def download(self):
        download_btn=self.wait_until_clickable(self.TEMPLATE_BTN)
        download_btn.click()
        logger.info(f"Clicked Template Download button ")

    def reset(self):
        reset_btn=self.wait_until_clickable(self.RESET_BTN)
        reset_btn.click()
        logger.info(f"Reset button clicked")

    def upload(self):
        latest_csv = self.get_latest_csv("tests/downloads")

        # Convert to absolute path
        absolute_path = str(Path(latest_csv).resolve())

        upload_input = self.wait_until_visible(self.UPLOAD_INPUT)
        upload_input.send_keys(absolute_path)

        logger.info(f"Uploaded file successfully: {absolute_path}")
        Screenshot.take(self.driver,f"Uploaded file successfully: {absolute_path}")

    def close(self):
        close_btn=self.wait_until_clickable(self.CLOSE_BTN)
        close_btn.click()

    import os
    from pathlib import Path

    def get_latest_csv(self, directory="tests/downloads", retries=3, wait=1) -> str:
        """
        Returns the latest downloaded CSV file from the given directory.
        Automatically retries in case the file is still being written.
        """

        directory = Path(directory)

        if not directory.exists():
            raise FileNotFoundError(f"Directory does not exist: {directory}")

        for attempt in range(retries):
            csv_files = list(directory.glob("*.csv"))

            if csv_files:
                latest_file = max(csv_files, key=lambda f: f.stat().st_mtime)
                logger.info(f"Found {len(csv_files)} CSV files. Latest: {latest_file}")
                return str(latest_file)

            logger.warning(f"No CSV found, retrying... ({attempt + 1}/{retries})")
            time.sleep(wait)

        raise FileNotFoundError("No CSV files found in downloads folder after retries.")

    def download_and_update_csv(self):
        latest_csv = self.get_latest_csv("tests/downloads")
        json_file = "testData/recordData.json"

        update_csv_with_json(latest_csv, json_file)
        logger.info(f"Updated latest CSV: {latest_csv}")
