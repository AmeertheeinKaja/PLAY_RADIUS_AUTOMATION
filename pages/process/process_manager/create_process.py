from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

import time
from pages.base_page import BasePage

from utils.counter_manager import get_next_process_number
from utils.logger import get_logger
from utils.data_reader import load_test_data
from utils.screenshot import Screenshot

data = load_test_data("process/create_process.json")

from pages.common.loader import Loader


# from testdata.createProcessData import process_code,process_Name,review_rating,channel


logger = get_logger()


class CreateProcess(BasePage):
    ADD_BTN = (By.XPATH, "//button[@id='add-entity']")
    PROCESS_CODE_FIELD = (By.XPATH, "//input[@name='processCode']")
    PROCESS_NAME_FIELD = (By.XPATH, "//input[@name='processName']")
    REVIEW_RATING_FIELD = (By.XPATH, "//input[@id='review']")
    CHANNEL_FIELD = (By.XPATH, "//input[@id='channel']")
    CHECKBOX_NAME = "showReviewRatings"
    STT_CHECKBOX_NAME = "isEnableSTT"
    CLOSE_BTN = (By.XPATH, "//button[@title='Close']")
    EDIT_BTN = (By.XPATH, "//button[@title='Edit']")

    SAVE_BTN = (By.XPATH, "//button[@title='Save']")
    SA_SAVE_BTN = (By.XPATH, "//*[@id='sa-tab-call-pane']//button[@title='Save']")
    RESET_BTN = (By.XPATH, "//button[@title='Reset']")
    CHANNEL_MENU = (By.XPATH, "//*[@id='menuv1']/li/button[1]")
    # Constants for Error Messages (using ALL_CAPS for constants)
    ERROR_PROCESS_CODE_TEXT = "Input should be between 4 and 32 characters long"
    ERROR_PROCESS_NAME_TEXT = "This field is required"
    ERROR_PROCESS_CODE_TEXT_LOCATOR = (By.XPATH,
                                       "//input[@name='processCode']/following-sibling::div[contains(@class, 'invalid-tooltip')]")
    ERROR_PROCESS_CODE_FORMAT_TEXT = "Start with alphabet, use only alphanumerics (A-Z, a-z, 0-9) and special characters (_, -)"

    ERROR_PROCESS_NAME_TEXT_LOCATOR = (By.XPATH,
                                       "//input[@name='processName']/following-sibling::div[contains(@class, 'invalid-tooltip')]")
    PROCESS_SUCCESS_TEXT = "Process saved successfully"
    PROCESS_FAILURE_TEXT = "Process failed to created"
    PROCESS_NAME_ALREADY_EXISTS_TEXT = "Process name already exists"
    channelPath = {
        "call": "//*[@id='process-basic-info']/div[2]/div/form/div/div/div[4]/div/div/div[1]/label",
        "chat": "//*[@id='process-basic-info']/div[2]/div/form/div/div/div[4]/div/div/div[2]/label",
        "email": "//*[@id='process-basic-info']/div[2]/div/form/div/div/div[4]/div/div/div[3]/label",
        "video": "//*[@id='process-basic-info']/div[2]/div/form/div/div/div[4]/div/div/div[4]/label"
    }

    def __init__(
            self,
            driver,
            process_code=None,
            process_name=None,
            review_rating=None,
            channels=None

    ):
        super().__init__(driver)
        self.loader = Loader(driver)
        self.last_toast = None

        self.process_number = get_next_process_number()

        # ✨ If parameter is passed → use it
        # ✨ Otherwise → fallback to JSON value
        base_code = process_code if process_code is not None else data.get("process_code", "")
        base_name = process_name if process_name is not None else data.get("process_name", "")

        self.process_code = f"{base_code}{self.process_number}"
        self.process_Name = f"{base_name}{self.process_number}"

        # Direct values (no need to append number)
        self.review_rating = review_rating if review_rating is not None else data.get("review_rating", False)
        self.channel = channels if channels is not None else data.get("channels", [])

    def create_process(
            self,
            process_code=None,
            process_name=None,
            review_rating=None,
            channels=None
    ):
        try:
            # --- Override values if passed ---
            if process_code is not None:
                self.process_code = f"{process_code}{self.process_number}"

            # Process Name
            if process_name is None:
                # auto-generate only when testcase does NOT supply a value
                self.process_name = f"{data.get('process_name', '')}{self.process_number}"
            else:
                # use EXACT value from testcase (even empty "")
                self.process_name = process_name if process_name == "" else f"{process_name}{self.process_number}"

            if review_rating is not None:
                self.review_rating = review_rating

            if channels is not None:
                self.channel = channels  # no number appended

            # --- Normal flow ---
            self.loader.load()
            self.click_add_process_button()
            self.add_process_code()
            self.add_process_name()
            self.set_review_rating()
            self.set_channel()
            self.click_save()
            self.loader.load()

            Screenshot.take(self.driver, f"Process_Created_{self.process_Name}")
            print("Process Created Successfully")

        except Exception as e:
            print("Error during creating process", e)

    def reset_process(self):
        reset_btn = self.wait_until_clickable(self.RESET_BTN)
        reset_btn.click()
        logger.info("Clicked Reset button")
        return True

    def click_save(self):
        save_btn = self.wait_until_clickable(self.SAVE_BTN)
        save_btn.click()
        try:
            self.wait.alert_is_present()
            alert = self.driver.switch_to.alert
            logger.info(f"Alert says: {alert.text}")
            alert.accept()
        except Exception:
            logger.debug("No alert present after saving")


        return self.toast_text()


    def close_btn(self):
        close_btn = self.wait_until_clickable(self.CLOSE_BTN)
        close_btn.click()
        logger.info("Clicked Close button")
        return True

    def toast_text(self):
        toast_text = self.capture_toast()
        self.last_toast = toast_text  # Store the value
        logger.info(f"Captured Toast: {toast_text}")
        return toast_text

    def click_add_process_button(self):
        try:
            add_process_button = self.wait_until_clickable(self.ADD_BTN)
            add_process_button.click()
            time.sleep(3)
            print("Added process is clicked")
        except Exception as e:
            print("Error click add process button", e)

    def add_process_name(self):
        try:
            field = self.wait_until_visible(self.PROCESS_NAME_FIELD)
            field.clear()

            # Always send EXACT value from create_process()
            field.send_keys(self.process_name)

            logger.info(f"Process Name entered: '{self.process_name}'")
        except Exception as e:
            logger.error(f"Error entering Process Name: {e}", exc_info=True)
            raise

    def add_process_code(self):
        try:
            add_process_code = self.driver.find_element(*self.PROCESS_CODE_FIELD)
            add_process_code.clear()
            add_process_code.send_keys(self.process_code)

        except Exception as e:
            logger.info("Error when  adding  process code", e)



    def set_review_rating(self):
        try:
            toggle_review_rating = self.driver.find_element(By.NAME, self.CHECKBOX_NAME)
            current_state = toggle_review_rating.is_selected()
            if self.review_rating != current_state:
                toggle_review_rating.click()
                print("Action: Toggled review rating")
            else:
                print("Alread active Review rating")
        except Exception as e:
            print("Error when setting review rating", e)

    def set_channel(self):
        try:
            logger.info("Setting channel configuration")
            # Normalize channel list
            if not isinstance(self.channel, (list, tuple)):
                if self.channel:
                    self.channel = [self.channel]
                    logger.info(f"Channel list set to {self.channel}")
                else:
                    logger.warning("No channels provided in configuration")
                    return False

            for ch in self.channel:
                xpath = self.channelPath.get(ch)
                if not xpath:
                    logger.warning(f"Unknown channel key: {ch}")
                    continue

                locator = (By.XPATH, xpath)
                element = self.wait_until_clickable(locator)

                logger.debug(f"Clicking channel: {ch}")
                try:
                    logger.debug(element.get_attribute("outerHTML"))
                except Exception:
                    pass

                element.click()
                time.sleep(0.5)





            # Wait for alert (if any) and accept


        except Exception:
            logger.error("Error when setting channel", exc_info=True)
            return False

    def get_error_message(self, locator):
        try:
            error_element = self.wait_until_visible(locator)
            return error_element.text.strip()
        except:
            return None

    def edit_process(self):
        try:
            edit_btn = self.wait_until_clickable(self.EDIT_BTN)
            edit_btn.click()
            logger.info("Clicked Edit button")
            return True
        except Exception as e:
            logger.error("Error clicking Edit button", exc_info=True)
            return False