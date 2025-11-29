from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.common.loader import Loader
from utils.logger import get_logger
from utils.screenshot import Screenshot

logger = get_logger(__name__)


class SideMenuPage(BasePage):
    ALLPROCESS_BTN = (By.XPATH, "//button[@title='Process']")
    CONFIG_BTN = (By.XPATH, "//button[@title='Configurations']")
    ALLRECORD_BTN = (By.XPATH, "//button[@title='Records']")
    RECORD_TABLE = (By.XPATH, "//table//tr")

    def __init__(self, driver):
        super().__init__(driver)
        self.loader = Loader(driver)

    def process(self):
        try:

            self.loader.load()

            process_button = self.wait_until_clickable(self.ALLPROCESS_BTN)
            process_button.click()

            logger.info("Process Showing")
            Screenshot.take(self.driver, f"Process Showing")

        except Exception as e:
            print("Error during clicking Process", e)
            logger.error("Error during clicking Process", e)

    def config(self):
        try:
            logger.info("🧭 Attempting to open Configuration page...")

            config_button = self.wait_until_clickable(self.CONFIG_BTN)
            self.driver.execute_script("arguments[0].click();", config_button)
            logger.info("✅ Configuration button clicked.")

            self.loader.load()
            Screenshot.take(self.driver, f"Configuration button clicked")

        except Exception as e:
            logger.exception("❌ Error during clicking configuration")
            print("Error during clicking configuration", e)
            raise

    def record(self):
        """Opens the 'All Records' section."""
        try:
            logger.info("🔄 Attempting to open 'All Records' section...")

            record_button = self.wait_until_clickable(self.ALLRECORD_BTN)
            self.driver.execute_script("arguments[0].click();", record_button)
            logger.info("✅ 'All Records' button clicked.")

            self.loader.load()  # Wait for any reloads
            self.wait_until_visible(self.RECORD_TABLE)

            logger.info("✅ 'All Records' view opened successfully.")
            Screenshot.take(self.driver, f"All Records view opened successfully")

        except Exception as e:
            Screenshot.take(self.driver, "Error_AllRecords")
            logger.error(f"❌ Error clicking 'All Records' button: {e}", exc_info=True)
            print(f"Error during clicking All Records: {e}")
