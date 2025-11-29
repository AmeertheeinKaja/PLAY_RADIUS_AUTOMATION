from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.logger import get_logger
from utils.screenshot import Screenshot

logger = get_logger(__name__)

class Loader(BasePage):
    LOADER = (By.XPATH, "//div[@class='loader_holder']")


    def load(self):
        try:
            logger.info("Waiting for loader to disappear...")
            self.wait_loader_to_disappear(self.LOADER)
            print("Loader Stopped")
            logger.info("Loader Stopped.")

        except Exception as e:
            print(f"Failed to load: {e}")
            logger.exception(f"Failed to load: {e}")

