import time

from selenium.common import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from pages.base_page import BasePage
from pages.common.loader import Loader
from utils.screenshot import Screenshot
from utils.logger import get_logger

logger = get_logger(__name__)


class RecordNavigator(BasePage):

    NEXT_RECORD_BTN = (By.XPATH, "//button[@title='Next']")
    PREV_RECORD_BTN = (By.XPATH, "//button[@title='Back']")
    CLOSE_RECORD_BTN = (By.XPATH, "//button[@title='Close']")



    def __init__(self, driver):
        super().__init__(driver)
        self.loader = Loader(driver)

    # ----------------------------------------------------------------------
    # SAFE CLICK HELPER
    # ----------------------------------------------------------------------
    def safe_click(self, element, label="element"):
        """Clicks reliably using ActionChains with retry and fallback."""
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'})", element)
            ActionChains(self.driver).move_to_element(element).click().perform()
            logger.info(f"🖱️ Clicked {label} successfully.")
            return True

        except ElementClickInterceptedException:
            logger.warning(f"⚠️ Click intercepted for {label}, retrying with JS click...")
            try:
                self.driver.execute_script("arguments[0].click()", element)
                logger.info(f"🖱️ JS Click succeeded for {label}.")
                return True
            except Exception as e:
                logger.error(f"❌ JS click also failed for {label}: {e}", exc_info=True)
                return False

        except Exception as e:
            logger.error(f"❌ Failed to click {label}: {e}", exc_info=True)
            return False

    # ----------------------------------------------------------------------
    # BUTTON ENABLE/DISABLE CHECK
    # ----------------------------------------------------------------------
    def is_button_disabled(self, locator, label):
        """Robust detection for disabled buttons via attributes and class names."""
        try:
            btn = self.wait_until_present(locator)

            # 1. Standard Selenium property check
            if not btn.is_enabled():
                logger.info(f"ℹ️ {label} is DISABLED (native disabled).")
                return True

            # 2. Visual/CSS disabled check
            classes = btn.get_attribute("class").lower()
            if "disabled" in classes or "btn-disabled" in classes:
                logger.info(f"ℹ️ {label} is DISABLED (visual/CSS disabled).")
                return True

            return False

        except TimeoutException:
            logger.warning(f"⚠️ {label} not found in DOM.")
            return True  # Safe default: treat as disabled

        except Exception as e:
            logger.error(f"❌ Error checking {label}: {e}", exc_info=True)
            return True

    # ----------------------------------------------------------------------
    # UNIFIED INTERNAL NAVIGATION
    # ----------------------------------------------------------------------
    def _navigate(self, locator, label):
        """Internal handler for Next / Previous navigation."""
        if self.is_button_disabled(locator, label):
            logger.info(f"⛔ Cannot click {label}. It is disabled.")
            return False

        btn = self.wait_until_clickable(locator)

        if not self.safe_click(btn, label):
            Screenshot.take(self.driver, f"Error_Click_{label}")
            return False

        self.loader.load()
        Screenshot.take(f"{label}_Clicked", self.driver)

        logger.info(f"✅ {label} navigation completed.")
        return True

    # ----------------------------------------------------------------------
    # PUBLIC APIS
    # ----------------------------------------------------------------------
    def navigate_next_record(self):
        return self._navigate(self.NEXT_RECORD_BTN, "Next Record")

    def navigate_prev_record(self):
        return self._navigate(self.PREV_RECORD_BTN, "Previous Record")

    def close_record(self):
        btn = self.wait_until_clickable(self.CLOSE_RECORD_BTN)

        if self.safe_click(btn, "Close Record"):
            self.loader.load()
            Screenshot.take("Close_Record", self.driver)
            logger.info("✅ Record closed successfully.")

    def iterate_all_records(self, callback=None):
        """
        Iterates through all records starting from the currently opened record.
        Applies callback(record_index) at each record if provided.
        Stops when Next Record button becomes disabled.
        """
        record_index = 1

        logger.info("🔍 Starting record iteration...")

        while True:
            logger.info(f"\n📄 Processing Record #{record_index}")

            # 1. Run callback (your extraction logic)
            if callback:
                try:
                    callback(record_index)
                except Exception as e:
                    logger.error(f"❌ Callback failed for record {record_index}: {e}", exc_info=True)

            # 2. Check if next record is possible
            if self.is_button_disabled(self.NEXT_RECORD_BTN, "Next Record"):
                logger.info("🏁 No more records available. Stopping iteration.")
                break

            # 3. Navigate to next record
            success = self._navigate(self.NEXT_RECORD_BTN, "Next Record")
            Screenshot.take(self.driver, f"Next Record")

            if not success:
                logger.error("❌ Navigation to next record failed. Stopping iteration.")
                break

            record_index += 1

        logger.info("✔️ Finished iterating all records.")

