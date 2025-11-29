from pages.base_page import BasePage
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
import time

from selenium.webdriver.support.select import Select

from pages.base_page import BasePage

from utils.counter_manager import get_next_process_number
from utils.logger import get_logger

from utils.screenshot import Screenshot
from utils.data_reader import load_test_data
from utils.screenshot import Screenshot

data = load_test_data("versionData.json")
logger = get_logger()


class PublishVersion(BasePage):
    MODAL_CANCEL_BTN = (By.XPATH, "//button[@title='Cancel']")
    MODAL_PUBLISH_BTN = (By.XPATH, "//button[text()='Publish']")
    PUBLISH_CATEGORY_VERSION_BTN = (By.XPATH, "//button[@title='Publish Version']")

    def __init__(self, driver):
        super().__init__(driver)
        self.version_name = data.get("new", {}).get("name")
        self.interaction = data.get("new", {}).get("interaction")
        self.import_version_process = data.get("import", {}).get("process_name")
        self.import_version_version = data.get("import", {}).get("version")
        self.import_version_interaction = data.get("import", {}).get("interaction")
        self.import_version_name= data.get("import", {}).get("name")
        self.copy_version_version = data.get("copy", {}).get("version")
        self.copy_version_interaction = data.get("copy", {}).get("interaction")
        self.copy_version_name = data.get("copy", {}).get("name")

    def publish_version(self):



        publish_button = self.wait_until_clickable(self.PUBLISH_CATEGORY_VERSION_BTN)
        publish_button.click()

        try:
            # Wait for modal to appear
            modal_locator = (By.XPATH,
                             "//div[@role='dialog' and contains(@class,'modal') and contains(@class,'show')]")
            self.wait_until_clickable(modal_locator)

            modal_save_btn = self.wait_until_clickable(self.MODAL_PUBLISH_BTN)
            modal_save_btn.click()

            time.sleep(2)

            self.wait_invisible(modal_locator)

            # Wait for modal to disappear

            return True

        except TimeoutException:
            logger.warning("⚠️ Import Version modal not found or took too long to load.")
            return False
