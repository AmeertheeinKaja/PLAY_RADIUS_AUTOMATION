# pages/version/version_config.py
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.process.version.version_modal import VersionModal
from utils.logger import get_logger

logger = get_logger()


class VersionConfig(BasePage):

    CHANNEL_LOCATORS = {
        "call": {
            "ACCORD": (By.XPATH, "//button[@id='call_version_accord']"),
            "IMPORT": (By.XPATH, "//ul[@id='menuv_call']//button[@title='Import Version']"),
            "COPY":   (By.XPATH, "//ul[@id='menuv_call']//button[@title='Copy Version']"),
            "ADD":    (By.XPATH, "//ul[@id='menuv_call']//button[@title='Add Version']"),
        },
        "chat": {
            "ACCORD": (By.XPATH, "//button[@id='chat_version_accord']"),
            "IMPORT": (By.XPATH, "//ul[@id='menuv_chat']//button[@title='Import Version']"),
            "COPY":   (By.XPATH, "//ul[@id='menuv_chat']//button[@title='Copy Version']"),
            "ADD":    (By.XPATH, "//ul[@id='menuv_chat']//button[@title='Add Version']"),
        },
        "video": {
            "ACCORD": (By.XPATH, "//button[@id='video_version_accord']"),
            "IMPORT": (By.XPATH, "//ul[@id='menuv_video']//button[@title='Import Version']"),
            "COPY":   (By.XPATH, "//ul[@id='menuv_video']//button[@title='Copy Version']"),
            "ADD":    (By.XPATH, "//ul[@id='menuv_video']//button[@title='Add Version']"),
        },
        "email": {
            "ACCORD": (By.XPATH, "//button[@id='email_version_accord']"),
            "IMPORT": (By.XPATH, "//ul[@id='menuv_email']//button[@title='Import Version']"),
            "COPY":   (By.XPATH, "//ul[@id='menuv_email']//button[@title='Copy Version']"),
            "ADD":    (By.XPATH, "//ul[@id='menuv_email']//button[@title='Add Version']"),
        },
    }

    def __init__(self, driver):
        super().__init__(driver)
        self._active_channel = None
        self.last_toast = None

    def open_version_section(self, channel: str):
        channel = channel.lower()

        if channel not in self.CHANNEL_LOCATORS:
            raise ValueError(f"Unsupported channel: {channel}")

        self._active_channel = channel
        accord = self.CHANNEL_LOCATORS[channel]["ACCORD"]

        self.wait_until_clickable(accord).click()
        logger.info(f"Opened {channel.upper()} Version section.")
    def _get_locator(self, action: str):
        if not self._active_channel:
            raise RuntimeError("Channel not selected. Call open_version_section(channel) first.")

        return self.CHANNEL_LOCATORS[self._active_channel][action]

    def open_import_version_modal(self):
        self.wait_until_clickable(self._get_locator("IMPORT")).click()
        logger.info("Import Version clicked.")
        return VersionModal(self.driver)

    def open_copy_version_modal(self):
        self.wait_until_clickable(self._get_locator("COPY")).click()
        logger.info("Copy Version clicked.")
        return VersionModal(self.driver)

    def open_add_version_modal(self):
        self.wait_until_clickable(self._get_locator("ADD")).click()
        logger.info("Add Version clicked.")
        return VersionModal(self.driver)

    def toast_text(self):
        txt = self.capture_toast()
        self.last_toast = txt
        logger.info(f"Toast: {txt}")
        return txt

    def perform(self, channel: str, action: str, data: dict):
        """
        High-level version operation.
        action: add | import | copy
        """
        action = action.lower()
        channel = channel.lower()

        self.open_version_section(channel)

        if action == "add":
            modal = self.open_add_version_modal()
        elif action == "import":
            modal = self.open_import_version_modal()
        elif action == "copy":
            modal = self.open_copy_version_modal()
        else:
            raise ValueError(f"Unsupported action: {action}")

        modal.wait_for_modal()
        modal.fill(data)
        toast = modal.submit()
        modal.wait_for_modal_close()

        return toast