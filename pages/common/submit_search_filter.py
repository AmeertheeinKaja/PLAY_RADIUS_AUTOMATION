from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.logger import get_logger
from pages.common.loader import Loader

logger = get_logger(__name__)

class SubmitFilterSearch(BasePage):
    FILTER_SEARCH = (By.XPATH, "//button[normalize-space(text())='Search']")
    CLEAR_FILTER = (By.XPATH, "//button[normalize-space(text())='Clear']")
    SUBMIT_SEARCH = (By.XPATH, "//button[normalize-space(text())='Submit']")
    CALL_LOGO = (By.XPATH, "//div[@class='pbi_content']//span[@title='Channel - Call']")
    CHAT_LOGO = (By.XPATH, "//div[@class='pbi_content']//span[@title='Channel - Chat']")
    EMAIL_LOGO = (By.XPATH, "//div[@class='pbi_content']//span[@title='Channel - Email']")
    VIDEO_LOGO = (By.XPATH, "//div[@class='pbi_content']//span[@title='Channel - Video']")

    def __init__(self, driver):
        super().__init__(driver)
        self.loader = Loader(driver)

    def searchFilter(self):
        try:
            search_btn=self.wait_until_clickable(self.FILTER_SEARCH)
            search_btn.click()
            self.loader.load()

            print("Searching ")
            logger.info(f"Searching")
        except Exception as e:
            print("Failed to search: {e}",e)
            logger.error("Failed to search: {e}",e)

    def clearFilter(self):
        try:
            clear_btn=self.wait_until_clickable(self.CLEAR_FILTER)
            clear_btn.click()
            self.loader.load()

            print("Clearing Filter ")
            logger.info(f"Clearing Filter")
        except Exception as e:
            print("Failed to clear filter: {e}",e)

            logger.error("Failed to clear filter: {e}",e)


    def get_record_type(self):
        if self.is_element_present(self.CALL_LOGO):
            return "Call"
        if self.is_element_present(self.CHAT_LOGO):
            return "Chat"
        if self.is_element_present(self.EMAIL_LOGO):
            return "Email"
        if self.is_element_present(self.VIDEO_LOGO):
            return "Video"

        return "Unknown"