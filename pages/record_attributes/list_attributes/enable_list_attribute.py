from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import get_logger
from utils.data_reader import load_test_data
from pages.common.loader import Loader

logger = get_logger(__name__)

data = load_test_data("filter/list_attribute.json")
enable_list = data["enable_attributes"]


class EnableListAttribute(BasePage):

    UPDATE_BTN = (By.XPATH, "//button[text()='Update']")

    def __init__(self, driver):
        super().__init__(driver)
        self.loader = Loader(driver)

    def enable(self):
        try:
            for attr in enable_list:
                self._enable_single_attribute(attr)

            self._click_update_button()

            logger.info("All attributes enabled successfully.")

        except Exception as e:
            logger.error(f"Error enabling attributes: {e}")
            raise

    # ----- PRIVATE HELPERS ----- #

    def _enable_single_attribute(self, attr):
        try:
            span = (By.XPATH, f"//span[text()='{attr}']")
            span_el = self.wait_until_visible(span)

            label_el = span_el.find_element(By.XPATH, "./ancestor::label")
            input_id = label_el.get_attribute("for")
            input_el = self.driver.find_element(By.ID, input_id)

            # Skip if disabled
            if input_el.get_attribute("disabled"):
                logger.info(f"Skipping '{attr}' — disabled")
                return

            # Skip if already enabled
            if input_el.get_attribute("checked"):
                logger.info(f"Skipping '{attr}' — already enabled")
                return

            # Toggle checkbox
            label_el.click()
            logger.info(f"Enabled attribute: {attr}")

        except Exception as e:
            logger.warning(f"Failed enabling '{attr}': {e}")

    def _click_update_button(self):
        btn = self.wait_until_clickable(self.UPDATE_BTN)
        btn.click()

        # Wait for reload/state update
        self.loader.load()

