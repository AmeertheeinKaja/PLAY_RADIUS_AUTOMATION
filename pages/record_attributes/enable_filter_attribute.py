from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from pages.base_page import BasePage
from utils.logger import get_logger
from pages.common.loader import Loader
from utils.data_reader import load_test_data

# data = load_test_data("filter_attribute.json")
# enable_list = data["enable_attributes"]


logger = get_logger(__name__)

class EnableFilterAttribute(BasePage):

    def enable(self, attrList):
        try:
            UPDATE_BTN = (By.XPATH, "//button[text()='Update']")

            for attr in attrList:
                # Find span first
                ATTR_SPAN = (
                    By.XPATH,
                    f"(//form[@class='needs-validation'])[1]//span[normalize-space(text())='{attr}']"
                )

                span_el = self.wait_until_visible(ATTR_SPAN)

                # From span, go up to label, then get its "for" attribute
                label_el = span_el.find_element(By.XPATH, "./ancestor::label")
                checkbox_id = label_el.get_attribute("for")

                # Now find the actual checkbox <input>
                CHECKBOX = (By.ID, checkbox_id)
                checkbox_el = self.driver.find_element(*CHECKBOX)

                if not checkbox_el.is_selected():
                    # ONLY click if not selected
                    label_el.click()
                    logger.info(f"Enabled attribute: {attr}")
                    time.sleep(0.3)
                else:
                    logger.info(f"{attr} is already enabled. Skipping...")

            update_button = self.wait_until_clickable(UPDATE_BTN)
            update_button.click()
            print("attribute updated")
            logger.info("attribute updated")

        except Exception as e:
            print("Error during clicking Filter update", e)
            logger.error("Error during clicking Filter update", e)

    def enableSingleAttribute(self,attributeName):
        try:
            UPDATE_BTN =(By.XPATH,"//button[text()='Update']")
            # loader = Loader(driver)
            # loader.load()

            ENABLE_ATTR = (
                By.XPATH,
                f"(//form[@class='needs-validation'])[1]//span[normalize-space(text())='{attributeName}']"
            )

            try:
                attr_button = self.wait_until_clickable(ENABLE_ATTR)
                attr_button.click()
                logger.info(f"Enabled attribute: {attributeName}")
                time.sleep(0.5)
            except Exception as inner_e:
                logger.warning(f"Attribute '{attributeName}' not found or not clickable: {inner_e}")

            update_button = self.wait_until_clickable(UPDATE_BTN)
            update_button.click()

            print("attribute updated ")
            logger.info("attribute updated")

        except Exception as e:
            print("Error during clicking Filter update",e)
            logger.error("Error during clicking Filter update",e)
