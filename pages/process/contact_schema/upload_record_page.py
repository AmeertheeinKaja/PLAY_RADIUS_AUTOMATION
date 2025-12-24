import time
from pathlib import Path

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from pages.common.loader import Loader
from pages.base_page import BasePage
from utils.logger import get_logger
from utils.screenshot import Screenshot
from utils.csv_updater import update_csv_with_json
from utils.screenshot import Screenshot

logger = get_logger(__name__)


class UploadRecord(BasePage):
    TAB_UPLOAD_RECORD = (By.XPATH, "//*[@id='accordionExample']/ul/ul[5]/li/button/span[2]")
    UPLOAD_INPUT = (By.XPATH, "//input[@type='file']")
    TEMPLATE_BTN = (By.XPATH, "//button[@title='Download Template']")
    SUBMIT_BTN = (By.XPATH, "//span[text()='Submit']")
    RESET_BTN = (By.XPATH, "//button[text()='Reset']")
    CLOSE_BTN = (By.XPATH, "//button[@title='Close']")
    ERROR_COUNT=(By.XPATH, "//div[contains(@class, 'textmaroon')]//div[@class='number']")
    VIEW_ERROR_BTN=(By.XPATH, "//div[@title='View Errors']")
    OK_BUTTON = (By.XPATH, "//div[@class='action_end']//button[text()='Ok']")


    def __init__(self, driver):
        super().__init__(driver)
        self.loader = Loader(driver)

    # -------------------------
    # UI ACTIONS
    # -------------------------

    def open_upload(self):
        try:
            clicked = self.safe_click(self.TAB_UPLOAD_RECORD)

            if not clicked:
                logger.warning("Upload Record tab is disabled. Skipping upload.")
                Screenshot.take(self.driver, "Upload tab disabled")
                return False  # graceful exit

            self.loader.load()
            logger.info("Upload record page opened")
            Screenshot.take(self.driver, "Upload record page opened")
            return True

        except Exception as e:
            logger.error(f"Unexpected failure opening upload page: {e}")
            Screenshot.take(self.driver, "Upload record open failed")
            return False

    def submit(self):
        try:
            self.wait_until_clickable(self.SUBMIT_BTN).click()
            logger.info("Submit button clicked")
        except Exception as e:
            logger.error(f"Submit action failed: {e}")
            Screenshot.take(self.driver, "Submit failed")
            raise

    def download(self):
        clicked = self.safe_click(self.TEMPLATE_BTN)

        if not clicked:
            logger.warning("Download Template button not enabled. Skipping download.")
            Screenshot.take(self.driver, "Template button disabled")
            return False

        logger.info("Template download button clicked")
        Screenshot.take(self.driver, "Template download clicked")
        return True

    def reset(self):
        try:
            self.wait_until_clickable(self.RESET_BTN).click()
            logger.info("Reset button clicked")
        except Exception as e:
            logger.error(f"Reset action failed: {e}")
            Screenshot.take(self.driver, "Reset failed")
            raise

    def get_error_count(self, timeout=5) -> int:
        """
        Reads error count safely.
        Returns 0 if not present / invalid.
        """
        try:
            el = self.wait_until_visible(self.ERROR_COUNT, timeout=timeout)
            text = el.text.strip()

            count = int(text) if text.isdigit() else 0
            logger.info(f"Upload error count: {count}")
            return count

        except Exception as e:
            logger.warning(f"Error count not available: {e}")
            return 0

    def view_error(self):
        try:
            clicked = self.safe_click(self.VIEW_ERROR_BTN)
            if clicked:
                logger.info("View Errors opened successfully.")
                Screenshot.take(self.driver, "View Errors opened")
                return True
            else:
                logger.warning("View Errors button not clickable.")
                return False

        except Exception as e:
            logger.warning(f"View error failed: {e}")
            return False

    def is_submit_disabled(self) -> bool:
        try:
            btn = self.wait_until_present(self.SUBMIT_BTN)

            # presence check is the most reliable
            return btn.get_attribute("disabled") is  None

        except Exception:
            return False

    def check_and_open_errors(self):
        """
        Opens View Errors only if error count > 0,
        then clicks OK to close error modal.
        """
        count = self.get_error_count()

        if count > 0:
            logger.warning(f"{count} errors found after upload.")
            Screenshot.take(self.driver, "View Errors after upload")

            opened = self.view_error()
            if opened:
                Screenshot.take(f"error_upload")
                time.sleep(0.5)  # allow modal render
                self.click_error_ok()

            return True

        logger.info("No errors found after upload.")
        return False

    def close(self):
        try:
            self.wait_until_clickable(self.CLOSE_BTN).click()
            logger.info("Upload dialog closed")
        except Exception as e:
            logger.error(f"Close action failed: {e}")
            Screenshot.take(self.driver, "Close failed")
            raise

    def upload(self):
        try:
            latest_csv = self.get_latest_csv("tests/downloads")
            absolute_path = str(Path(latest_csv).resolve())

            upload_input = self.wait_until_visible(self.UPLOAD_INPUT)
            upload_input.send_keys(absolute_path)

            logger.info(f"Uploaded file successfully: {absolute_path}")
            Screenshot.take(self.driver, "File uploaded successfully")
        except Exception as e:
            logger.error(f"File upload failed: {e}")
            Screenshot.take(self.driver, "File upload failed")
            raise

    # -------------------------
    # FILE OPERATIONS
    # -------------------------

    def get_latest_csv(self, directory="tests/downloads", retries=3, wait=1) -> str:
        """
        Returns the latest downloaded CSV file.
        Retries in case file is still downloading.
        """
        try:
            directory = Path(directory)

            if not directory.exists():
                raise FileNotFoundError(f"Directory does not exist: {directory}")

            for attempt in range(retries):
                csv_files = list(directory.glob("*.csv"))

                if csv_files:
                    latest_file = max(csv_files, key=lambda f: f.stat().st_mtime)
                    logger.info(f"Latest CSV found: {latest_file}")
                    return str(latest_file)

                logger.warning(f"No CSV found, retrying ({attempt + 1}/{retries})")
                time.sleep(wait)

            raise FileNotFoundError("No CSV files found after retries")

        except Exception as e:
            logger.error(f"Error while fetching latest CSV: {e}")
            raise

    def download_and_update_csv(self,record_path):
        try:
            latest_csv = self.get_latest_csv("tests/downloads")
            json_file = "test_data/process/contact_schema/record_data.json"

            update_csv_with_json(latest_csv, json_file)
            logger.info(f"CSV updated successfully: {latest_csv}")
        except Exception as e:
            logger.error(f"CSV update failed: {e}")
            raise

    def safe_click(self, locator, retries=3, wait=1, allow_disabled=False):
        """
        Attempts to click an element safely.
        Returns True if clicked, False if skipped.
        """
        for attempt in range(retries):
            try:
                element = self.wait_until_present(locator)

                # check disabled attribute
                disabled = element.get_attribute("disabled")
                aria_disabled = element.get_attribute("aria-disabled")

                if not allow_disabled and (disabled or aria_disabled == "true"):
                    logger.warning(f"Element disabled: {locator}")
                    return False

                # scroll + JS click (most reliable)
                self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                time.sleep(0.2)
                self.driver.execute_script("arguments[0].click();", element)

                return True

            except TimeoutException:
                logger.warning(f"Retry click ({attempt + 1}/{retries}) for {locator}")
                time.sleep(wait)

        return False

    def click_error_ok(self):
        """
        Clicks OK button in error modal safely.
        """
        try:
            clicked = self.safe_click(self.OK_BUTTON, retries=2)

            if clicked:
                logger.info("Error modal OK clicked.")
                Screenshot.take(self.driver, "Error modal OK clicked")
                return True

            logger.warning("OK button not clickable.")
            return False

        except Exception as e:
            logger.warning(f"Click OK failed: {e}")
            return False

    def upload_process(self, record_path):
        """
        Executes upload flow ONLY if upload tab is enabled.
        Safely skips entire flow otherwise.
        """

        if not self.open_upload():
            logger.warning("Upload Record is disabled. Entire upload flow skipped.")
            return False

        if not self.download():
            logger.warning("Template download disabled. Upload flow skipped.")
            return False

        try:
            self.download_and_update_csv(record_path)
        except FileNotFoundError:
            logger.warning("CSV not available. Upload flow skipped.")
            return False

        try:
            self.upload()
        except Exception:
            logger.error("CSV upload failed.")
            return False

        self.submit()

        # ⭐ NEW STEP
        self.check_and_open_errors()

        logger.info("Upload process completed.")
        return True

    def is_upload_tab_disabled(self) -> bool:
        """
        Checks if Upload Record button is disabled.
        Does NOT click anything.
        Safe for test-only usage.
        """
        try:
            btn = self.driver.find_element(
                By.XPATH,
                "//*[@id='accordionExample']//button[.//span[normalize-space()='Upload Record']]"
            )

            disabled = btn.get_attribute("disabled")
            aria_disabled = btn.get_attribute("aria-disabled")

            return bool(disabled) or aria_disabled == "true"

        except Exception:
            return True  # treat as disabled if element not found
