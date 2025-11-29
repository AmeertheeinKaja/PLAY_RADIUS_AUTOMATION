from selenium.webdriver.support import expected_conditions as EC

from selenium.common import NoAlertPresentException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

import time

from selenium.webdriver.support.wait import WebDriverWait

from pages.base_page import BasePage

from utils.counter_manager import get_next_process_number
from utils.logger import get_logger
from utils.data_reader import load_test_data
from utils.screenshot import Screenshot

data = load_test_data("updateProcessData.json")

from pages.common.loader import Loader


# from testdata.createProcessData import process_code,process_Name,review_rating,channel


logger = get_logger()


class EditProcess(BasePage):
    BASIC_SCOPE = "//div[@id='process-basic-info']"
    ADD_BTN = (By.XPATH, "//button[@id='add-entity']")
    PROCESS_CODE_FIELD = (By.XPATH, "//input[@name='processCode']")
    PROCESS_NAME_FIELD = (By.XPATH, "//input[@name='processName']")
    REVIEW_RATING_FIELD = (By.XPATH, "//input[@id='review']")
    CHANNEL_FIELD = (By.XPATH, "//input[@id='channel']")
    CHECKBOX_NAME = "showReviewRatings"
    STT_CHECKBOX_NAME = "isEnableSTT"
    EDIT_BTN = (By.XPATH, f"{BASIC_SCOPE}//button[@title='Edit']")

    SAVE_BTN = (By.XPATH, f"{BASIC_SCOPE}//button[@title='Save']")
    SA_SAVE_BTN = (By.XPATH, "//*[@id='sa-tab-call-pane']//button[@title='Save']")
    RESET_BTN = (By.XPATH, "//button[@title='Reset']")
    CHANNEL_MENU = (By.XPATH, "//*[@id='menuv1']/li/button[1]")
    channel_states = {"call": "", "chat": "checked", "email": "checked", "video": ""}
    channelPath = {
        "call": "//*[@id='process-basic-info']/div[2]/div/form/div/div/div[4]/div/div/div[1]/label",
        "chat": "//*[@id='process-basic-info']/div[2]/div/form/div/div/div[4]/div/div/div[2]/label",
        "email": "//*[@id='process-basic-info']/div[2]/div/form/div/div/div[4]/div/div/div[3]/label",
        "video": "//*[@id='process-basic-info']/div[2]/div/form/div/div/div[4]/div/div/div[4]/label"
    }

    def __init__(self, driver):
        super().__init__(driver)

        self.process_number = get_next_process_number()

        self.process_Name = data.get('process_name', '') + str(self.process_number)
        self.review_rating = data.get('review_rating', False)
        self.channel = data.get('channels', [])

    def edit_process(self, driver):
        try:
            loader = Loader(driver)
            loader.load()
            logger.info("Starting process edit flow")

            Screenshot.take(driver, "Before_Edit_Button_Click")

            self.click_edit_process_button(driver)
            logger.info("Clicked Edit button")

            Screenshot.take(driver, "After_Edit_Button_Click")

            self.edit_processData(driver)
            logger.info(f"Edited processName set to: {self.process_Name}")

            Screenshot.take(driver, "After_Edit_ProcessName")

            self.set_review_rating(driver)
            logger.info("Review rating toggled successfully")

            Screenshot.take(driver, "After_Set_Review_Rating")

            edit_channel_status = self.edit_channel(driver)
            logger.info(f"Channel edit result: {edit_channel_status}")

            Screenshot.take(driver, "After_Channel_Edit")

            self.save_process(driver)
            logger.info("Clicked Save button successfully")

            Screenshot.take(driver, f"After_Save_{self.process_Name}")

            logger.info(f"✅ Process edited successfully: {self.process_Name}")
            print("Process Edited Successfully")

        except Exception as e:
            logger.exception("❌ Error during editing process")
            Screenshot.take(driver, "Edit_Process_Error")
            print("Error during editing process:", e)

    def click_edit_process_button(self, driver):
        try:
            edit_process_button = self.wait_until_clickable(self.EDIT_BTN)
            edit_process_button.click()
            time.sleep(3)
            print("Added process is clicked")
        except Exception as e:
            print("Error click add process button", e)

    def edit_processData(self, driver):
        try:

            edit_process_name = self.driver.find_element(*self.PROCESS_NAME_FIELD)
            edit_process_name.clear()
            edit_process_name.send_keys(self.process_Name)

        except Exception as e:
            print("Error when  adding  process data", e)

    def set_review_rating(self, driver):
        try:
            toggle_review_rating = driver.find_element(By.NAME, self.CHECKBOX_NAME)
            current_state = toggle_review_rating.is_selected()
            if self.review_rating != current_state:
                toggle_review_rating.click()
                print("Action: Toggled review rating")
            else:
                print("Alread active Review rating")
        except Exception as e:
            print("Error when setting review rating", e)

    def save_process(self, driver):
        try:
            save_process_button = self.wait_until_clickable(self.SAVE_BTN)
            save_process_button.click()
            time.sleep(3)
            print("Process is saved")
        except Exception as e:

            print("Error click save process button", e)

    def edit_channel(self, driver):
        try:
            logger.info("Setting channel configuration")

            channels_to_be_enabled = set(self.channel)

            # --- Loop over all channels ---
            for channel_name, label_xpath in self.channelPath.items():
                checkbox_xpath = f"{label_xpath}/input | {label_xpath}/../input[1]"
                checkbox_locator = (By.XPATH, checkbox_xpath)
                checkbox_element = self.wait_until_present(checkbox_locator)

                if not checkbox_element:
                    logger.warning(f"Could not find checkbox element for channel: {channel_name}")
                    continue

                is_currently_enabled = checkbox_element.is_selected()
                should_be_enabled = channel_name in channels_to_be_enabled

                if should_be_enabled != is_currently_enabled:
                    label_locator = (By.XPATH, label_xpath)
                    clickable_element = self.wait_until_clickable(label_locator)
                    clickable_element.click()
                    time.sleep(0.5)
                    action = "Enabled" if should_be_enabled else "Disabled"
                    logger.info(f"Action: Toggled channel {channel_name} to {action}")
                else:
                    logger.debug(f"Channel {channel_name} already in desired state.")

            save_btn = self.wait_until_clickable(self.SAVE_BTN)
            save_btn.click()
            logger.info("Clicked Save button after editing channels")

            # --- After all toggles, check if popup appears ---
            try:
                logger.info("Waiting for Deactivate popup to appear...")

                # Wait for modal to be visible
                modal_locator = (By.XPATH,
                                 "//div[@role='dialog' and contains(@class,'modal') and contains(@class,'show')]")
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located(modal_locator))
                logger.info("Deactivate confirmation modal detected.")

                # Once modal is confirmed visible → now look for Deactivate button
                deactivate_btn_locator = (By.XPATH,
                                          "//button[normalize-space()='Deactivate'] | //button[contains(.,'Deactivate')]")
                deactivate_btn = WebDriverWait(driver, 5).until(EC.element_to_be_clickable(deactivate_btn_locator))

                driver.execute_script("arguments[0].click();", deactivate_btn)
                logger.info("Clicked 'Deactivate' button successfully.")
                Screenshot.take(driver, f"Deactivate_AfterClick_{self.process_Name}")

                time.sleep(1)

            except TimeoutException:
                logger.warning("⚠️ No Deactivate popup found within timeout.")
                Screenshot.take(driver, f"No_Popup_Found_{self.process_Name}")

            # --- Finally, click Save ---


            # --- Handle alert (if any) ---
            try:
                self.wait.until(EC.alert_is_present())
                alert = driver.switch_to.alert
                logger.info(f"Alert says: {alert.text}")
                alert.accept()
            except TimeoutException:
                logger.debug("No alert present after saving")

            return True

        except Exception:
            logger.error("Error when setting channel", exc_info=True)
            return False


