import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from utils.logger import get_logger
from pages.common.loader import Loader
from utils.screenshot import Screenshot

logger = get_logger(__name__)

class RecordManager(BasePage):
    ALLRECORD_BTN = (By.XPATH, "//button[@title='Records']")
    VIEW_RECORDS_BTN = (By.XPATH, "//tbody/tr[1]")
    CLOSE_RECORD_BTN = (By.XPATH, "//button[@title='Close']")
    RECORD_TABLE = (By.XPATH, "//table//tr")
    SCROLL_CONTAINER = (By.XPATH, "//div[@class='wrapper_main']//div[@style='width: 100%; overflow: auto;']")
    def __init__(self, driver):
        super().__init__(driver)
        self.toast_text = ""

    def record(self):
        """Opens the 'All Records' section."""
        try:
            logger.info("🔄 Attempting to open 'All Records' section...")

            loader = Loader(self.driver)
            loader.load()  # Ensure no pending loaders before clicking

            record_button = self.wait_until_clickable(self.ALLRECORD_BTN)
            self.driver.execute_script("arguments[0].click();", record_button)
            logger.info("✅ 'All Records' button clicked.")

            loader.load()  # Wait for any reloads
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(self.RECORD_TABLE)
            )

            logger.info("✅ 'All Records' view opened successfully.")
            print("All Records Showing")

        except Exception as e:
            Screenshot.take(self.driver, "Error_AllRecords")
            logger.error(f"❌ Error clicking 'All Records' button: {e}", exc_info=True)
            print(f"Error during clicking All Records: {e}")

    def view_record(self):
        """Opens the first record in the records table."""
        try:
            logger.info("🔍 Attempting to open the first record...")
            loader = Loader(self.driver)
            loader.load()

            view_record_button = self.wait_until_clickable(self.VIEW_RECORDS_BTN)
            self.driver.execute_script("arguments[0].click();", view_record_button)
            logger.info("✅ First record clicked.")

            self.toast_text =self.capture_toast()
            logger.info(f"Toast message after opening record: {self.toast_text }")



            Screenshot.take(self.driver, "View_Record")
            logger.info("✅ Record opened successfully.")
            print("Record is opened")

        except Exception as e:
            Screenshot.take(self.driver, "Error_ViewRecord")
            logger.error(f"❌ Error clicking View Record: {e}", exc_info=True)
            print(f"Error during clicking View Record: {e}")

    def close_record(self):
        """Closes the currently opened record."""
        try:
            logger.info("🧩 Attempting to close opened record...")
            loader = Loader(self.driver)
            loader.load()

            close_record_button = self.wait_until_clickable(self.CLOSE_RECORD_BTN)
            self.driver.execute_script("arguments[0].click();", close_record_button)
            logger.info("✅ 'Close' button clicked.")

            loader.load()
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(self.RECORD_TABLE)
            )

            logger.info("✅ Record closed successfully.")
            print("Record is closed")

        except Exception as e:
            Screenshot.take(self.driver, "Error_CloseRecord")
            logger.error(f"❌ Error clicking Close Record: {e}", exc_info=True)
            print(f"Error during clicking Close Record: {e}")

    def scroll_table_to_bottom(self):
        scroll_div = self.wait_until_visible(self.SCROLL_CONTAINER)
        self.driver.execute_script(
            "arguments[0].scrollTop = arguments[0].scrollHeight;", scroll_div
        )
        time.sleep(1)

    def scroll_table_to_top(self):
        table = self.wait_until_visible(self.SCROLL_CONTAINER)
        self.driver.execute_script("arguments[0].scrollTop = 0", table)

    def get_first_visible_row_text(self):
        rows = self.find_elements(self.SCROLL_CONTAINER)
        if rows:
            return rows[0].text.strip()
        return None