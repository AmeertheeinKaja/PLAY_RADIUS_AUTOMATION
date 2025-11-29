from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from pages.base_page import BasePage
from utils.logger import get_logger
from pages.common.loader import Loader


logger = get_logger(__name__)

class EditListAttribute(BasePage):
    EDIT_BTN = (By.XPATH, "(//button[text()='Edit'])[2]")

    def open_edit(self):
        btn = self.wait_until_clickable(self.EDIT_BTN)
        btn.click()
        logger.info("List edit panel opened")

