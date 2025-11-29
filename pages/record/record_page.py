from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from pages.process.process_manager.search_process import OpenProcess
from pages.process.process_manager.process_filter import ProcessFilter
from pages.common.open_filter_search import FilterSearch
from pages.process.channel_config.call.call_stt_config import CallSTTConfig
from pages.common.loader import Loader
from utils.logger import get_logger
from utils.screenshot import Screenshot

logger = get_logger(__name__)


class RecordPage(BasePage):


    CALL_LOGO=(By.XPATH,"//div[@class='pbi_content']//span[@title='Channel - Call']")
    CHAT_LOGO = (By.XPATH, "//div[@class='pbi_content']//span[@title='Channel - Chat']")
    EMAIL_LOGO = (By.XPATH, "//div[@class='pbi_content']//span[@title='Channel - Email']")
    VIDEO_LOGO = (By.XPATH, "//div[@class='pbi_content']//span[@title='Channel - Video']")
    TOAST_LOCATOR = (By.XPATH, "//div[@role='status']")
    PROCESS_NAME = (
        By.XPATH,
        "//div[@class='col-6']/span[contains(@title,'Process Name')]"
    )
    error_text="Key file is missing."

    def __init__(self, driver):
        super().__init__(driver)
        self.loader = Loader(driver)
        self.open_process = OpenProcess(driver)
        self.open_filter = FilterSearch(driver)
        self.process_filter = ProcessFilter(driver)
        self.call_stt_config = CallSTTConfig(driver)
        self.process_name=""
        self.channel=""
        self.error_message=""

    def record_info(self):
        # Capture toast only once
        if not self.error_message:
            self.find_message()

        self.find_channel()
        self.find_process_name()
        self.handle_record_flow()

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

    def is_element_present(self, locator):
        try:
            self.driver.find_element(*locator)
            return True
        except:
            return False

    def find_channel(self):
        self.channel=self.get_record_type()
        logger.info(f"Record Channel is: {self.channel}")

    def find_message(self):
        if self.error_message:
            return self.error_message

        toast = self.capture_toast()
        if toast:
            self.error_message = toast

        return self.error_message

    def find_process_name(self):
        try:
            process_element = self.wait_until_visible(self.PROCESS_NAME)
            self.process_name = process_element.get_attribute("title").replace("Process Name - ", "")
            logger.info(f"Process Name is: {self.process_name}")
            return self.process_name
        except Exception as e:
            logger.error("Error retrieving Process Name", exc_info=True)
            Screenshot.take(self.driver, "Process_Name_Error")
            return None


    def capture_toast(self, timeout=10):  # Increased timeout for robustness
        try:
            # Wait for toast to appear (visibility)
            toast = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(self.TOAST_LOCATOR)
            )

            message = toast.text.strip()
            logger.info(f"TOAST APPEARED: {message}")

            # Wait for toast to disappear (invisibility)
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(self.TOAST_LOCATOR)
            )

            return message

        except Exception as e:
            # Note: A TimeoutException here is expected if no toast appears
            logger.warning("No toast captured within timeout.", exc_info=False)
            return None


    def open_process_page(self):
        self.open_process.process()
        self.open_filter.filter()
        self.process_filter.apply_filter(self.process_name)
        self.open_process.view_process()
        self.call_stt_config.open_stt_tab()
        self.call_stt_config.click_edit()
        self.call_stt_config.key_file_edit()
        self.call_stt_config.upload_key_file()
        self.call_stt_config.click_save()
        self.call_stt_config.click_test()

    def handle_record_flow(self):


        logger.info(f"Checking if error message matches expected error text...")
        logger.info(f"Expected Error Text: {self.error_text}")
        logger.info(f"Actual Error Text: {self.error_message}")

        if self.error_message == self.error_text:
            logger.info("⚠ Error message matched. Opening process page...")
            self.open_process_page()
        else:
            logger.info("ℹ No matching error message. Skipping process page opening.")
