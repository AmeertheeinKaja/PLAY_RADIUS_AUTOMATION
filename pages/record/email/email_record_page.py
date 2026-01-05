from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from pages.base_page import BasePage
from pages.common.loader import Loader
from utils.logger import get_logger

logger = get_logger(__name__)


class EmailPage(BasePage):

    # ==========================
    # LOCATORS
    # ==========================
    MAIL_ITEMS = (By.CSS_SELECTOR, ".pw_mail_list_item")
    MAIL_HEADER = (By.CSS_SELECTOR, ".pw_mail_list_item_header")
    MAIL_BODY = (By.CSS_SELECTOR, ".pw_mail_list_item_body")

    INTERACTION_ICON = (By.CSS_SELECTOR, ".sts.imoon")

    INBOUND_ICON = "icon-inbound"
    OUTBOUND_ICON = "icon-outbound"

    # ==========================
    # INIT
    # ==========================
    def __init__(self, driver):
        super().__init__(driver)
        self.loader = Loader(driver)

    # ==========================
    # BASIC CHECKS
    # ==========================
    def has_emails(self):
        mails = self.driver.find_elements(*self.MAIL_ITEMS)
        logger.info(f"📧 Email count: {len(mails)}")
        return len(mails) > 0

    # ==========================
    # OPEN / CLOSE
    # ==========================
    def open_mail(self, mail_item):
        body = mail_item.find_element(*self.MAIL_BODY)

        # Open only if closed
        if "d-none" in body.get_attribute("class"):
            header = mail_item.find_element(*self.MAIL_HEADER)
            header.click()
            self.loader.load()
            logger.info("📬 Mail opened")

        return mail_item

    def close_mail(self, mail_item):
        body = mail_item.find_element(*self.MAIL_BODY)

        # Close only if open
        if "d-none" not in body.get_attribute("class"):
            header = mail_item.find_element(*self.MAIL_HEADER)
            header.click()
            self.loader.load()
            logger.info("📪 Mail closed")

    def toggle_mail(self, mail_item):
        mail_item.find_element(*self.MAIL_HEADER).click()
        self.loader.load()

    # ==========================
    # FIRST MAIL HELPERS
    # ==========================
    def get_first_mail(self):
        return self.wait_until_visible(self.MAIL_ITEMS)

    def open_first_mail(self):
        mail = self.get_first_mail()
        return self.open_mail(mail)

    def close_first_mail(self):
        mail = self.get_first_mail()
        self.close_mail(mail)

    # ==========================
    # INTERACTION TYPE
    # ==========================
    def get_interaction_type(self, mail_item=None):
        """
        Returns: 'Inbound' | 'Outbound' | 'Unknown'
        """
        if not mail_item:
            mail_item = self.get_first_mail()

        icon = mail_item.find_element(*self.INTERACTION_ICON)
        icon_class = icon.get_attribute("class")

        if self.INBOUND_ICON in icon_class:
            logger.info("📥 Interaction Type: Inbound")
            return "Inbound"

        if self.OUTBOUND_ICON in icon_class:
            logger.info("📤 Interaction Type: Outbound")
            return "Outbound"

        logger.warning("❓ Interaction Type: Unknown")
        return "Unknown"

    # ==========================
    # ADVANCED
    # ==========================
    def close_all_open_mails(self):
        mails = self.driver.find_elements(*self.MAIL_ITEMS)

        for mail in mails:
            body = mail.find_element(*self.MAIL_BODY)
            if "d-none" not in body.get_attribute("class"):
                self.close_mail(mail)

        logger.info("📪 All expanded mails closed")
