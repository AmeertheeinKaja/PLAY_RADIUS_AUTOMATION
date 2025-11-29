from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from pages.base_page import BasePage
from utils.logger import get_logger
from pages.common.loader import Loader
from utils.screenshot import Screenshot

logger = get_logger(__name__)


class FilterSearch(BasePage):
    FILTER_BTN = (By.XPATH, "//button[@title='Filter']")

    def filter(self):
        try:
            loader = Loader(self.driver)
            # loader.load()
            # wait = WebDriverWait(driver, 10)

            #filter_button = wait.until(EC.element_to_be_clickable((By.XPATH, self.FILTER_BTN)))
            filter_button=self.wait_until_clickable(self.FILTER_BTN)
            filter_button.click()
            self.wait_for_filter_ui_ready()
            return True





            logger.info("Filter Showing")
            print("Filter Showing")
            Screenshot.take(self.driver, "Filter_Showing")
        except Exception as e:
            logger.error(f"Filter: {e}")
            print("Error during filtering",e)

