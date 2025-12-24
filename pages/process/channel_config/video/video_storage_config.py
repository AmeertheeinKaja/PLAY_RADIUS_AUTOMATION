from selenium.webdriver.common.bidi.storage import Storage
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.common.loader import Loader
from utils.logger import get_logger
from utils.screenshot import Screenshot



logger = get_logger(__name__)


class VideoStorageConfig(BasePage):

    VIDEO_CONFIG_SCOPE = "//div[@id='media-configuration-video']"

    # Tabs
    TAB_STORAGE_TYPE = (By.XPATH, f"{VIDEO_CONFIG_SCOPE}//button[@id='home-tab-video']")

    # Radio buttons
    STORAGE_RADIO_HTTP = (By.XPATH, f"{VIDEO_CONFIG_SCOPE}//input[@name='type' and @value='http/https']")
    STORAGE_RADIO_SFTP = (By.XPATH, f"{VIDEO_CONFIG_SCOPE}//input[@name='type' and @value='sftp']")
    STORAGE_RADIO_FTP  = (By.XPATH, f"{VIDEO_CONFIG_SCOPE}//input[@name='type' and @value='ftp']")

    # HTTP fields
    STORAGE_HTTP_URL = (By.XPATH, f"{VIDEO_CONFIG_SCOPE}//input[@name='dirPath']")
    STORAGE_HTTP_SUCCESS="Channel updated successfully"

    # SFTP fields
    STORAGE_SFTP_HOSTNAME = (By.XPATH, f"{VIDEO_CONFIG_SCOPE}//input[@name='host']")
    STORAGE_SFTP_PORT = (By.XPATH, f"{VIDEO_CONFIG_SCOPE}//input[@name='port']")
    STORAGE_SFTP_USERNAME = (By.XPATH, f"{VIDEO_CONFIG_SCOPE}//input[@name='user']")
    STORAGE_SFTP_PASSWORD = (By.XPATH, f"{VIDEO_CONFIG_SCOPE}//input[@name='password']")
    STORAGE_SFTP_DIR_PATH = (By.XPATH, f"{VIDEO_CONFIG_SCOPE}//input[@name='dirPath']")

    # FTP fields
    STORAGE_FTP_HOSTNAME = (By.XPATH, f"{VIDEO_CONFIG_SCOPE}//input[@name='host']")
    STORAGE_FTP_PORT = (By.XPATH, f"{VIDEO_CONFIG_SCOPE}//input[@name='port']")
    STORAGE_FTP_USERNAME = (By.XPATH, f"{VIDEO_CONFIG_SCOPE}//input[@name='user']")
    STORAGE_FTP_PASSWORD = (By.XPATH, f"{VIDEO_CONFIG_SCOPE}//input[@name='password']")
    STORAGE_FTP_DIR_PATH = (By.XPATH, f"{VIDEO_CONFIG_SCOPE}//input[@name='dirPath']")

    # Common buttons (global)
    STORAGE_RESET_BTN = (By.XPATH, f"{VIDEO_CONFIG_SCOPE}//button[@title='Reset']")
    STORAGE_SAVE_BTN  = (By.XPATH, f"{VIDEO_CONFIG_SCOPE}//button[@title='Save']")
    STORAGE_EDIT_BTN  = (By.XPATH, f"{VIDEO_CONFIG_SCOPE}//button[@title='Edit']")
    STORAGE_TEST_BTN  = (By.XPATH, f"{VIDEO_CONFIG_SCOPE}//button[@title='Test Connection']")

    ERROR_TEXT = "Connection failed. ERROR: sftp.connect: All configured authentication methods failed after 2 attempts"
    INVALID_INPUT_PATH = (By.XPATH, f"{VIDEO_CONFIG_SCOPE}//div[contains(@class, 'invalid-tooltip')]")
    INVALID_HOST_PATH=(By.XPATH, f"{VIDEO_CONFIG_SCOPE}//input[@name='host']/following-sibling::div[normalize-space()='This field is required']")
    INVALID_PORT_PATH = (By.XPATH,
                         f"{VIDEO_CONFIG_SCOPE}//input[@name='port']/following-sibling::div[normalize-space()='This field is required']")
    INVALID_PASSWORD_PATH = (By.XPATH,
                         f"{VIDEO_CONFIG_SCOPE}//input[@name='password']/following-sibling::div[normalize-space()='This field is required']")
    INVALID_USER_PATH = (By.XPATH,
                         f"{VIDEO_CONFIG_SCOPE}//input[@name='user']/following-sibling::div[normalize-space()='This field is required']")

    SUCCESS_TEXT="Channel updated successfully"



    def __init__(self, driver):
        super().__init__(driver)
        self.loader = Loader(driver)
        self.storage =None
        self.last_toast = None

    # ----------------------------------------------------
    # STORAGE MAIN ENTRY
    # ----------------------------------------------------

    def set_storage_type(self, storage_type: str):
        self.storage = storage_type.lower()
        logger.info(f"Setting storage type from test: {self.storage}")




    def _apply_storage_fields(self, storage_data):
        if self.storage == "http":
            self.http_config(storage_data.get("http", {}))
        elif self.storage == "sftp":
            self.sftp_config(storage_data.get("sftp", {}))
        elif self.storage == "ftp":
            self.ftp_config(storage_data.get("ftp", {}))

    def storage_config(self, storage_data):
        self._apply_storage_fields(storage_data)

    def edit_storage_config(self, storage_data):
        self.try_click_edit()
        self._apply_storage_fields(storage_data)

    def toast_text(self):
        toast_text = self.capture_toast()
        self.last_toast = toast_text  # Store the value
        logger.info(f"Captured Toast: {toast_text}")
        Screenshot.take(f"toast_{toast_text.replace(' ', '_')}")

        return toast_text
    # ----------------------------------------------------
    # HTTP STORAGE CONFIG
    # ----------------------------------------------------
    def http_config(self,http_data):
        self.httpurl = http_data.get("domain_url","")
        try:
            self.http()
            field = self.driver.find_element(*self.STORAGE_HTTP_URL)
            field.clear()
            field.send_keys(self.httpurl)

            self.click_save()
            self.toast_text()
            self.loader.load()
            Screenshot.take(self.driver, "http-configured")
            logger.info("HTTP storage configured successfully.")

        except Exception as e:
            logger.error(f"HTTP config error: {e}", exc_info=True)

    # ----------------------------------------------------
    # SFTP STORAGE CONFIG
    # ----------------------------------------------------
    def sftp_config(self,sftp_data):
        self.sftp_host = sftp_data.get("hostName","")
        self.sftp_port = sftp_data.get("port","")
        self.sftp_username = sftp_data.get("username","")
        self.sftp_password = sftp_data.get("password","")
        self.sftp_dir_path = sftp_data.get("dirPath","")
        try:
            self.sftp()

            self._fill(self.STORAGE_SFTP_HOSTNAME, self.sftp_host)
            self._fill(self.STORAGE_SFTP_PORT, self.sftp_port)
            self._fill(self.STORAGE_SFTP_USERNAME, self.sftp_username)
            self._fill(self.STORAGE_SFTP_PASSWORD, self.sftp_password)
            self._fill(self.STORAGE_SFTP_DIR_PATH, self.sftp_dir_path)

            self.click_test()
            self.wait_for_filter_ui_ready()

            self.click_save()
            self.toast_text()
            self.loader.load()
            Screenshot.take(self.driver, "sftp-configured")

        except Exception as e:
            logger.error(f"SFTP config error: {e}", exc_info=True)

    # ----------------------------------------------------
    # FTP STORAGE CONFIG
    # ----------------------------------------------------
    def ftp_config(self,ftp_data):
        self.ftp_host = ftp_data.get("hostName","")
        self.ftp_port = ftp_data.get("port","")
        self.ftp_username = ftp_data.get("username","")
        self.ftp_password = ftp_data.get("password","")
        self.ftp_dir_path = ftp_data.get("dirPath","")
        try:
            self.ftp()

            self._fill(self.STORAGE_FTP_HOSTNAME, self.ftp_host)
            self._fill(self.STORAGE_FTP_PORT, self.ftp_port)
            self._fill(self.STORAGE_FTP_USERNAME, self.ftp_username)
            self._fill(self.STORAGE_FTP_PASSWORD, self.ftp_password)
            self._fill(self.STORAGE_FTP_DIR_PATH, self.ftp_dir_path)

            self.click_test()
            self.wait_for_filter_ui_ready()

            self.click_save()
            self.toast_text()
            self.loader.load()
            Screenshot.take(self.driver, "ftp-configured")

        except Exception as e:
            logger.error(f"FTP config error: {e}", exc_info=True)

    # ----------------------------------------------------
    # INPUT FIELD FILLER
    # ----------------------------------------------------
    def _fill(self, locator, value):
        el = self.driver.find_element(*locator)
        el.clear()
        el.send_keys(value)

    # ----------------------------------------------------
    # COMMON BUTTON CLICKS
    # ----------------------------------------------------
    def click_save(self):
        self.wait_until_clickable(self.STORAGE_SAVE_BTN).click()

    def click_reset(self):
        self.wait_until_clickable(self.STORAGE_RESET_BTN).click()

    def click_edit(self):
        self.wait_until_clickable(self.STORAGE_EDIT_BTN).click()

    def click_test(self):
        self.wait_until_clickable(self.STORAGE_TEST_BTN).click()

    # ----------------------------------------------------
    # TABS & RADIO
    # ----------------------------------------------------
    def storage_tab(self):
        self.wait_until_clickable(self.TAB_STORAGE_TYPE).click()

    def http(self):
        self.driver.find_element(*self.STORAGE_RADIO_HTTP).click()

    def sftp(self):
        self.driver.find_element(*self.STORAGE_RADIO_SFTP).click()

    def ftp(self):
        self.driver.find_element(*self.STORAGE_RADIO_FTP).click()

    def wait_for_element_optional(self, locator, timeout=2):
        try:
            return self.wait_until_present(locator, timeout=timeout)
        except:
            return None

    def try_click_edit(self):
        try:
            if self.is_element_present(self.STORAGE_EDIT_BTN):
                logger.info("Edit button found. Clicking edit.")
                self.click_edit()
            else:
                logger.info("Edit button not found. Skipping edit click.")
        except Exception as e:
            logger.error(f"Error while trying to click edit: {e}", exc_info=True)

    def is_element_present(self, locator):
        try:
            self.driver.find_element(*locator)
            return True
        except:
            return False
    def get_error_message(self, locator):
        try:
            error_element = self.wait_until_visible(locator)
            return error_element.text.strip()
        except:
            return None

    def assert_success(self):
        if self.last_toast != self.SUCCESS_TEXT:
            raise AssertionError(f"Expected success toast but got: {self.last_toast}")
        logger.info("Storage updated successfully.")

    def assert_error(self, expected_message):
        if expected_message not in (self.last_toast or ""):
            raise AssertionError(
                f"Expected error: '{expected_message}', got: '{self.last_toast}'"
            )
