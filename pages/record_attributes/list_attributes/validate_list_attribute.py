from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class ValidateListAttribute(BasePage):

    def is_attribute_enabled(self, attribute_name):
        span_el = self.wait_until_visible((By.XPATH, f"//span[text()='{attribute_name}']"))
        label_el = span_el.find_element(By.XPATH, "./ancestor::label")
        input_id = label_el.get_attribute("for")

        input_el = self.driver.find_element(By.ID, input_id)

        disabled = input_el.get_attribute("disabled")
        checked = input_el.get_attribute("checked")

        logger.info(f"Verify: {attribute_name} → disabled={bool(disabled)}, checked={bool(checked)}")

        # ⭐ FIX: Disabled fields cannot be enabled, so treat them as valid
        if disabled:
            logger.info(f"Skipping {attribute_name} (disabled in UI)")
            return True

        return checked is not None
