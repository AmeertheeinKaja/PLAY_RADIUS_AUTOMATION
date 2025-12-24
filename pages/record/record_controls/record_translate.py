import time
from selenium.common import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from pages.base_page import BasePage
from pages.common.loader import Loader
from utils.screenshot import Screenshot
from utils.logger import get_logger

logger = get_logger(__name__)


class RecordTranslate(BasePage):

    TRANSLATE_BTN = (By.XPATH, "//i[contains(@class, 'icon-language') and contains(@class, 'dropdown-toggle')]")
    TRANSLATE_DROPDOWN_MENU = (By.CSS_SELECTOR, ".trans_lang_drop.lang_chat")
    TRANSLATE_SEARCH_INPUT = (By.XPATH, "//input[@placeholder='Search Language']")
    SEARCH_BUTTON = (By.XPATH, "//button[@id='searchBtn']")
    TRANSLATED_LANGUAGE_BTN = (By.XPATH, "//div[contains(@class,'stp_item')][2]/button")
    ORIGINAL_BTN = (By.XPATH, "//button[normalize-space()='Original']")

    def __init__(self, driver):
        super().__init__(driver)
        self.loader = Loader(driver)
        self.language = None
        self.translated_language = None

    def open_translate(self):
        try:
            logger.info("Opening translate dropdown.")
            translate_button = self.wait_until_clickable(self.TRANSLATE_BTN)
            translate_button.click()
            self.wait_until_present(self.TRANSLATE_DROPDOWN_MENU)
            self.loader.load()
            Screenshot.take("Translate_Dropdown_Opened", self.driver)
        except Exception as e:
            Screenshot.take("Error_OpenTranslate", self.driver)
            logger.error(f"Failed to open translate dropdown: {e}", exc_info=True)
            raise

    def select_language_by_text(self, language_name: str):
        try:
            self.language = language_name
            logger.info(f"Selecting language: {language_name}")

            lang_locator = (By.XPATH, f"//div[normalize-space()='{language_name}']")
            lang_element = self.wait_until_clickable(lang_locator)
            lang_element.click()
            self.loader.load()

            Screenshot.take(f"Language_{language_name}_Selected", self.driver)
        except TimeoutException:
            logger.error(f"Language '{language_name}' not found or not clickable.")
            raise
        except Exception as e:
            logger.error(f"Error selecting language: {e}", exc_info=True)
            raise

    def select_language_using_search(self, language_name: str):
        try:
            self.language = language_name
            logger.info(f"Searching and selecting language: {language_name}")

            search_icon = self.wait_until_present(self.SEARCH_BUTTON)
            search_icon.click()

            search_input = self.wait_until_present(self.TRANSLATE_SEARCH_INPUT)
            search_input.clear()
            search_input.send_keys(language_name)

            lang_locator = (
                By.XPATH,
                f"//div[contains(@class, 'lang') and contains(@class, 'col-12') and normalize-space()='{language_name}']"
            )
            lang_element = self.wait_until_clickable(lang_locator)
            lang_element.click()

            self.wait_invisible(lang_locator)
            self.loader.load()
            Screenshot.take(f"SearchSelect_{language_name}", self.driver)

            self.loader.load()
        except Exception as e:
            logger.error(f"Error searching/selecting language: {e}", exc_info=True)
            raise

    def click_original_btn(self):
        try:
            logger.info("Clicking Original button.")
            original_btn = self.wait_until_clickable(self.ORIGINAL_BTN)
            original_btn.click()
            self.loader.load()
        except Exception as e:
            logger.error(f"Error clicking Original button: {e}", exc_info=True)
            raise

    def get_translated_lang(self):
        try:
            logger.info("Fetching translated language text.")
            self.translated_language = self.wait_until_visible(self.TRANSLATED_LANGUAGE_BTN).text
            logger.info(f"Translated language: {self.translated_language}")
            return self.translated_language
        except Exception as e:
            logger.error(
                f"Error fetching translated language. Locator: {self.TRANSLATED_LANGUAGE_BTN}. Error: {e}",
                exc_info=True
            )
            raise
