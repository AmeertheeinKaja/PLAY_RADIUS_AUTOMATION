from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from pages.base_page import BasePage
from utils.logger import get_logger
from pages.common.loader import Loader
from utils.data_reader import load_test_data
from utils.screenshot import Screenshot



logger = get_logger(__name__)

class OpenProcess(BasePage):
    ALLPROCESS_BTN=(By.XPATH, "//button[@title='Process']")
    PROCESS_SEARCH = (By.XPATH, "//input[@id='process_search_input']")
    SELECT_SEARCH = (By.XPATH, "//*[@id='root']/div[2]/div/div[3]/div/div/div[2]/div/div[2]/table/tbody/tr[1]")




    def process(self):
        try:
            loader = Loader(self.driver)
            loader.load()

            process_button=self.wait_until_clickable(self.ALLPROCESS_BTN)
            process_button.click()


            print("Process Showing")
            logger.info("Process Showing")

        except Exception as e:
            print("Error during clicking Process",e)
            logger.error("Error during clicking Process",e)

    def view_process(self):
        select_input = self.wait_until_clickable(self.SELECT_SEARCH)
        select_input.click()

    def search_by_code(self, processcode=None):
        loader = Loader(self.driver)
        try:
            logger.info(f"🔍 Searching for process code: {processcode}")

            # Wait for and enter process code
            process_input = self.wait_until_visible(self.PROCESS_SEARCH)
            process_input.clear()
            # process_input.send_keys(processcode)
            # logger.debug(f"Entered process code: {processcode}")

            for char in processcode:
                process_input.send_keys(char)
                # Short, non-blocking pause after each character
                time.sleep(1)  # 50


            # Click select/search button
            select_input = self.wait_until_clickable(self.SELECT_SEARCH)
            select_input.click()
            logger.info("✅ Process search triggered successfully")

            # Optional: wait for process result page or name
            # self.wait_until_visible((By.XPATH, f"//h1[contains(text(), '{process_code}')]"))

            # Take screenshot after success
            Screenshot.take(self.driver, f"Process_Search_{processcode}")
            logger.info(f"📸 Screenshot saved for process: {processcode}")

        except Exception as e:
            logger.error(f"❌ Error during process search for {processcode}: {e}", exc_info=True)
            print(f"Error during process search for {processcode}: {e}")


