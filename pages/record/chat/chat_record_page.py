from selenium.common import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.common.loader import Loader
from pages.record.record_controls.record_translate import RecordTranslate
from utils.logger import get_logger

logger = get_logger(__name__)


class ChatPage(BasePage):
    # -------------------- LOCATORS --------------------

    CHAT_MESSAGES = (By.CSS_SELECTOR, ".chat_messages .message_row")

    MESSAGE_COMMENT_BTN = (
        By.CSS_SELECTOR, ".items_btn[title='Comments']"
    )

    COMMENT_INPUT = (By.NAME, "comment")
    COMMENT_SUBMIT = (By.XPATH, "//button[normalize-space()='Comment']")

    # -------------------- INIT --------------------

    def __init__(self, driver):
        super().__init__(driver)
        self.loader = Loader(driver)
        self.translate = RecordTranslate(driver)

    # -------------------- DYNAMIC LOCATORS --------------------

    @staticmethod
    def MESSAGE_BY_TEXT(text):
        return (
            By.XPATH,
            f"//div[contains(@class,'chat_messages')]"
            f"//span[contains(@class,'message_text_value') and contains(.,'{text}')]"
            f"/ancestor::div[contains(@class,'message_row')]"
        )

    # -------------------- VALIDATIONS --------------------

    def has_messages(self):
        messages = self.driver.find_elements(*self.CHAT_MESSAGES)
        logger.info(f"💬 Chat message count: {len(messages)}")
        return len(messages) > 0

    # -------------------- COMMENTS --------------------

    def add_comment_to_first_message(self, comment_text):
        """
        Adds comment to the first chat message (hover-based UI)
        """
        message_row = self.wait_until_visible(self.CHAT_MESSAGES)

        ActionChains(self.driver).move_to_element(message_row).perform()
        logger.info("🖱️ Hovered on first chat message")

        comment_btn = message_row.find_element(*self.MESSAGE_COMMENT_BTN)
        self.wait_until_clickable(comment_btn).click()

        self.wait_until_visible(self.COMMENT_INPUT).send_keys(comment_text)
        self.wait_until_clickable(self.COMMENT_SUBMIT).click()

        self.loader.load()
        logger.info("✅ Comment added to first chat message")

    def add_comment_by_message_text(self, message_text, comment_text):
        """
        Adds comment to a specific message identified by text
        """
        message_row = self.wait_until_visible(
            self.MESSAGE_BY_TEXT(message_text)
        )

        ActionChains(self.driver).move_to_element(message_row).perform()
        logger.info(f"🖱️ Hovered on message: {message_text}")

        comment_btn = message_row.find_element(*self.MESSAGE_COMMENT_BTN)
        self.wait_until_clickable(comment_btn).click()

        self.wait_until_visible(self.COMMENT_INPUT).send_keys(comment_text)
        self.wait_until_clickable(self.COMMENT_SUBMIT).click()

        self.loader.load()
        logger.info(f"✅ Comment added to message: {message_text}")

    # -------------------- TRANSLATION --------------------

    def translate_chat(self, language, use_search=False):

        logger.info(f"🌐 Translating chat to: {language} (use_search={use_search})")
        """
        Translates chat using RecordTranslate component
        """
        self.translate.open_translate()

        if use_search:
            self.translate.select_language_using_search(language)
        else:
            self.translate.select_language_by_text(language)

        translated_lang = self.translate.get_translated_lang()
        logger.info(f"🌐 Chat translated to: {translated_lang}")
        return translated_lang

    def back_to_original(self):
        logger.info("🔙 Reverting chat to original language")

        try:
            self.translate.open_translate()

            if self.translate.is_original_btn_present():
                self.translate.click_original_btn()
                self.loader.load()
                logger.info("🔙 Reverted chat to original language")
            else:
                logger.warning("⚠️ Original button not present. Possibly already original.")

        except Exception as e:
            logger.error("❌ Failed to revert translation", exc_info=True)



