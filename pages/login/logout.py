from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.logger import get_logger
from pages.common.loader import Loader
from utils.screenshot import Screenshot


logger = get_logger(__name__)

class Logout(BasePage):
    LOADER = (By.XPATH, "//div[@class='loader_holder']")
    PROFILE_ICON = (By.XPATH, "//img[@alt='Profile']")
    LOGOUT_BTN = (By.XPATH, "//button[@title='Logout']")
    TITLE=(By.XPATH, "//span[text()='Login']")


    def logout(self):
        # self.wait_invisible(self.LOADER)
        try:
            loader = Loader(self.driver)
            loader.load()

            # self.wait_until_clickable(*self.PROFILE_ICON)
            # self.wait_until_clickable(*self.LOGOUT_BTN)
            self.click(self.PROFILE_ICON)
            self.click(self.LOGOUT_BTN)

            logger.info(f"Logout Successfully.")
            Screenshot.take(self.driver, "Logout_Successfully")
            self.title = self.wait_until_visible(self.TITLE).text.strip()


        except Exception as e:
            print("Failed to logout: {e}",e)
            logger.error("Failed to logout: {e}",e)
