from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from pages.base_page import BasePage
from utils.logger import get_logger
from pages.common.loader import Loader


logger = get_logger(__name__)

class EditFilterAttribute(BasePage):
    EDIT_BTN =(By.XPATH, "//*[@id='root']/div[2]/div/div[3]/div/div/div/div/form[1]/div[6]/div[2]/div/button")
    # ENABLE_ATTR = f"(//form[@class='needs-validation'])[1]//span[text()='{attributeName}']"
    UPDATE_BTN = "//button[text()='Update']"

    def edit(self):
        try:
            # loader = Loader(driver)
            # loader.load()

            edit_button=self.wait_until_clickable(self.EDIT_BTN)
            edit_button.click()
            # time.sleep(1)

            print("Edit button is clicked")
            logger.info("Edit button is clicked")

        except Exception as e:
            print("Error during clicking Filter Edit",e)
            logger.error("Error during clicking Filter Edit",e)
