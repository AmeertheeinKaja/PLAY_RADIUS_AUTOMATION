from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.logger import get_logger
from utils.read_properties import ReadConfig
from utils.screenshot import Screenshot
from pages.common.loader import Loader

logger = get_logger(__name__)


class LoginPage(BasePage):
    USERNAME = (By.ID, "loginForm.username")
    PASSWORD = (By.ID, "password")
    LOGIN_BTN = (By.ID, "loginForm.Login")
    DASHBOARD_UI=(By.XPATH,"//button[@title='Play']")
    ERROR_LOCATOR = (By.XPATH, "//*[@id='root']/div[2]/div/div/div/div[2]/div/div/div/span")
    ERROR_MESSAGE="Incorrect loginid or password."
    NETWORK_ERROR=(By.XPATH,"//*[@id='root']/div[2]/div/div/div/div[2]/div/div/div/span")

    def __init__(self, driver):
        super().__init__(driver)
        self.loader = Loader(self.driver)
        self.url = ReadConfig.get_login_url()

        self.username = ReadConfig.get_username()
        self.password = ReadConfig.get_password()

    def open(self):
        try:
            self.driver.get(self.url)
            self.wait_for_page_load()
            print(f"Opening: {self.url}")
            logger.info(f"Opening: {self.url}")
            # assert self.url in self.driver.current_url, (
            #     f"Expected URL part '{self.url}', but got '{self.driver.current_url}'"
            # )



        except Exception as e:

            logger.error(f"Failed to open: {self.url} - {e}")
            raise

    def login(self,username=None,password=None):
        try:
            if username is None:
                username = self.username
            if password is None:
                password = self.password

            login_user = self.wait_until_visible(self.USERNAME)
            login_user.clear()
            login_user.send_keys(username)

            login_pass = self.wait_until_visible(self.PASSWORD)
            login_pass.clear()
            login_pass.send_keys(password)


            login_btn = self.wait_until_visible(self.LOGIN_BTN)

            if not login_btn.is_enabled():
                logger.info("Login button is disabled — skipping click.")
                print("Login button is disabled — skipping click.")
                return

            login_btn.click()

            logger.info(f"Login submitted for user: {username}")
            self.loader.load()

            # self.wait_until_visible(self.DASHBOARD_UI)
            # self.wait_until_url_contains("/recording-list/all-records", timeout=15)




            logger.info(f"Login submitted successfully.")
            Screenshot.take(self.driver,f"Login Submitted successfully")

        except Exception as e:
            print(f"Failed to login: {self.url}", e)
            logger.error(f"Failed to login: {self.url} - {e}")
            raise

    def get_error_message(self):
        """Return the login error message text if visible."""
        try:
            error_element = self.wait_until_visible(self.ERROR_LOCATOR, timeout=5)
            return error_element.text.strip()
        except Exception:
            return ""

    def get_network_error(self):
        try:
            element = self.wait_until_visible(self.NETWORK_ERROR, timeout=10)
            return element.text.strip()
        except:
            return ""
