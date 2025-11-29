from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.common.loader import Loader
from utils.logger import get_logger
from utils.screenshot import Screenshot
from utils.data_reader import load_test_data

full_config = load_test_data("processData.json")
logger = get_logger(__name__)


class CallStorageConfig(BasePage):

    CALL_CONFIG_SCOPE = "//div[@id='media-configuration-call']"

    # Tabs
    TAB_STORAGE_TYPE = (By.XPATH, f"{CALL_CONFIG_SCOPE}//button[@id='home-tab-call']")

    # Radio buttons
    STORAGE_RADIO_HTTP = (By.XPATH, f"{CALL_CONFIG_SCOPE}//input[@name='type' and @value='http/https']")
    STORAGE_RADIO_SFTP = (By.XPATH, f"{CALL_CONFIG_SCOPE}//input[@name='type' and @value='sftp']")
    STORAGE_RADIO_FTP  = (By.XPATH, f"{CALL_CONFIG_SCOPE}//input[@name='type' and @value='ftp']")

    # HTTP fields
    STORAGE_HTTP_URL = (By.XPATH, f"{CALL_CONFIG_SCOPE}//input[@name='dirPath']")

    # SFTP fields
    STORAGE_SFTP_HOSTNAME = (By.XPATH, f"{CALL_CONFIG_SCOPE}//input[@name='host']")
    STORAGE_SFTP_PORT = (By.XPATH, f"{CALL_CONFIG_SCOPE}//input[@name='port']")
    STORAGE_SFTP_USERNAME = (By.XPATH, f"{CALL_CONFIG_SCOPE}//input[@name='user']")
    STORAGE_SFTP_PASSWORD = (By.XPATH, f"{CALL_CONFIG_SCOPE}//input[@name='password']")
    STORAGE_SFTP_DIR_PATH = (By.XPATH, f"{CALL_CONFIG_SCOPE}//input[@name='dirPath']")

    # FTP fields
    STORAGE_FTP_HOSTNAME = (By.XPATH, f"{CALL_CONFIG_SCOPE}//input[@name='host']")
    STORAGE_FTP_PORT = (By.XPATH, f"{CALL_CONFIG_SCOPE}//input[@name='port']")
    STORAGE_FTP_USERNAME = (By.XPATH, f"{CALL_CONFIG_SCOPE}//input[@name='user']")
    STORAGE_FTP_PASSWORD = (By.XPATH, f"{CALL_CONFIG_SCOPE}//input[@name='password']")
    STORAGE_FTP_DIR_PATH = (By.XPATH, f"{CALL_CONFIG_SCOPE}//input[@name='dirPath']")

    # Common buttons (global)
    STORAGE_RESET_BTN = (By.XPATH, f"{CALL_CONFIG_SCOPE}//button[@title='Reset']")
    STORAGE_SAVE_BTN  = (By.XPATH, f"{CALL_CONFIG_SCOPE}//button[@title='Save']")
    STORAGE_EDIT_BTN  = (By.XPATH, f"{CALL_CONFIG_SCOPE}//button[@title='Edit']")
    STORAGE_TEST_BTN  = (By.XPATH, f"{CALL_CONFIG_SCOPE}//button[@title='Test Connection']")

    def __init__(self, driver):
        super().__init__(driver)
        self.loader = Loader(driver)

        call_config = full_config.get("channel_config", {}).get("call", {})
        storage = call_config.get("storage", {})

        # Storage Type
        self.storage_type = storage.get("type", "")

        # HTTP
        self.httpurl = storage.get("http", {}).get("domain_url", "")

        # SFTP
        sftp = storage.get("sftp", {})
        self.sftp_host = sftp.get("hostName", "")
        self.sftp_port = str(sftp.get("port", ""))
        self.sftp_username = sftp.get("username", "")
        self.sftp_password = sftp.get("password", "")
        self.sftp_dir_path = sftp.get("dir_path", "")

        # FTP
        ftp = storage.get("ftp", {})
        self.ftp_host = ftp.get("hostName", "")
        self.ftp_port = str(ftp.get("port", ""))
        self.ftp_username = ftp.get("username", "")
        self.ftp_password = ftp.get("password", "")
        self.ftp_dir_path = ftp.get("dir_path", "")

    # ----------------------------------------------------
    # STORAGE MAIN ENTRY
    # ----------------------------------------------------
    def storage_config(self):
        self.storage_tab()

        if not self.storage_type:
            logger.warning("Storage type missing in JSON")
            return

        t = self.storage_type.lower()
        logger.info(f"Configuring storage type: {t}")

        if t == "http":
            self.http_config()
        elif t == "sftp":
            self.sftp_config()
        elif t == "ftp":
            self.ftp_config()
        else:
            logger.warning(f"Unknown storage type: {t}")

    # ----------------------------------------------------
    # HTTP STORAGE CONFIG
    # ----------------------------------------------------
    def http_config(self):
        try:
            self.http()
            field = self.driver.find_element(*self.STORAGE_HTTP_URL)
            field.clear()
            field.send_keys(self.httpurl)

            self.click_save()
            self.loader.load()
            Screenshot.take(self.driver, "http-configured")
            logger.info("HTTP storage configured successfully.")

        except Exception as e:
            logger.error(f"HTTP config error: {e}", exc_info=True)

    # ----------------------------------------------------
    # SFTP STORAGE CONFIG
    # ----------------------------------------------------
    def sftp_config(self):
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
            self.loader.load()
            Screenshot.take(self.driver, "sftp-configured")

        except Exception as e:
            logger.error(f"SFTP config error: {e}", exc_info=True)

    # ----------------------------------------------------
    # FTP STORAGE CONFIG
    # ----------------------------------------------------
    def ftp_config(self):
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
