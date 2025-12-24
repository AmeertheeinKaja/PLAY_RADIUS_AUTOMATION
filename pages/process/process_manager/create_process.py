from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

import time
from pages.base_page import BasePage

from utils.counter_manager import get_next_process_number
from utils.logger import get_logger
from utils.data_reader import load_test_data
from utils.screenshot import Screenshot



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




        self.process_code = process_code
        self.process_Name = process_name

        # Direct values (no need to append number)
        self.review_rating = review_rating
        self.channel = channels

    def create_process(self):


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
            logger.info("Process Created Successfully")



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
            field.send_keys(self.process_Name)

            logger.info(f"Process Name entered: '{self.process_Name}'")
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

    def get_enabled_channels(self):
        """
        Returns list of channels that are currently enabled in UI
        Example: ["call", "email"]
        """

        enabled_channels = []

        try:
            # Grab ALL channel checkboxes
            checkboxes = self.driver.find_elements(
                By.XPATH,
                "//input[@name='activeChannels']"
            )

            for cb in checkboxes:
                try:
                    value = cb.get_attribute("value")  # call/chat/email/...
                    checked = cb.is_selected()

                    if checked:
                        enabled_channels.append(value)
                except Exception:
                    continue

            logger.info(f"Enabled channels detected: {enabled_channels}")

        except Exception as e:
            logger.error("Error while reading enabled channels", exc_info=True)

        return enabled_channels


    def ensure_channel_enabled(self, channel_name: str) -> bool:

        self.edit_process()
        logger.info(f"Ensuring channel enabled: {channel_name}")
        enabled_channels = self.get_enabled_channels()
        if channel_name in enabled_channels:
            logger.info(f"Channel '{channel_name}' already enabled.")
            return True
        logger.warning(f"Channel '{channel_name}' is disabled. Enabling now...")
        try:
            label_xpath = self.channelPath.get(channel_name)
            if not label_xpath:
                raise ValueError(f"No locator found for channel: {channel_name}")
            # Click label to toggle checkbox
            label = self.wait_until_clickable((By.XPATH, label_xpath))
            label.click()
            time.sleep(0.5)
            # Save
            save_btn = self.wait_until_clickable(self.SAVE_BTN)
            save_btn.click()
            Loader(self.driver).load()
            # Handle deactivate popup if it appears
            try:
                modal_locator = (
                    By.XPATH,
                    "//div[@role='dialog' and contains(@class,'modal') and contains(@class,'show')]"
                )
                self.wait_until_visible(modal_locator)


                deactivate_btn = self.wait_until_clickable((
                    By.XPATH,
                    "//button[normalize-space()='Deactivate'] | //button[contains(.,'Deactivate')]"
                ))
                self.driver.execute_script("arguments[0].click();", deactivate_btn)
                logger.info("Deactivate popup confirmed.")
                Loader(self.driver).load()

            except TimeoutException:
                logger.info("No deactivate popup appeared.")

            # Final verification
            enabled_channels = self.get_enabled_channels()
            if channel_name in enabled_channels:
                logger.info(f"Channel '{channel_name}' successfully enabled.")
                return True

            logger.error(f"Channel '{channel_name}' still disabled after attempt.")
            return False

        except Exception:
            logger.exception(f"Failed to enable channel '{channel_name}'")
            Screenshot.take(self.driver, f"enable_channel_failed_{channel_name}")
            return False
