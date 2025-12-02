# pages/version/version_page.py
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.process.version.version_modal import VersionModal
from utils.logger import get_logger

logger = get_logger()


class VersionCallConfig(BasePage):

    # --- Locators ---
    CALL_VERSION_ACCORD = (By.XPATH, "//button[@id='call_version_accord']")
    IMPORT_CALL_VERSION = (By.XPATH, "//ul[@id='menuv_call']//button[@title='Import Version']")
    COPY_CALL_VERSION = (By.XPATH, "//ul[@id='menuv_call']//button[@title='Copy Version']")
    ADD_CALL_VERSION = (By.XPATH, "//ul[@id='menuv_call']//button[@title='Add Version']")


    def open_call_version_section(self):
        """Open Call Version Accordion"""
        btn = self.wait_until_clickable(self.CALL_VERSION_ACCORD)
        btn.click()
        logger.info("Opened Call Version section.")



    # ---------- OPEN MODALS ----------

    def open_import_version_modal(self):
        """Click Import Version and return modal handler"""
        self.wait_until_clickable(self.IMPORT_CALL_VERSION).click()
        logger.info("Import Version clicked.")
        return VersionModal(self.driver)

    def open_copy_version_modal(self):
        """Click Copy Version and return modal handler"""
        self.wait_until_clickable(self.COPY_CALL_VERSION).click()
        logger.info("Copy Version clicked.")
        return VersionModal(self.driver)

    def open_add_version_modal(self):
        """Click Add Version and return modal handler"""
        self.wait_until_clickable(self.ADD_CALL_VERSION).click()
        logger.info("Add Version clicked.")
        return VersionModal(self.driver)
