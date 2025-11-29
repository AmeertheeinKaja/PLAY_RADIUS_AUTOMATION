from typing import Tuple
import time
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.logger import get_logger
from utils.screenshot import Screenshot

logger = get_logger(__name__)


class BasePage:
    """Base class providing reusable Selenium actions and waits."""

    def __init__(self, driver, timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # ------------------------------------------------------------
    # Core Element Interactions
    # ------------------------------------------------------------
    def click(self, locator: Tuple[str, str]):
        """Clicks an element after waiting until it's clickable."""
        try:
            element = self.wait_until_clickable(locator)
            element.click()
            logger.info(f"✅ Clicked element: {locator}")
        except Exception as e:
            self._handle_error("click", locator, e)

    def send_keys(self, locator: Tuple[str, str], text: str):
        """Clears an input field and sends text."""
        try:
            element = self.wait_until_visible(locator)
            element.clear()
            element.send_keys(text)
            logger.info(f"✏️ Sent keys to {locator}: {text}")
        except Exception as e:
            self._handle_error("send_keys", locator, e)

    def get_text(self, locator: Tuple[str, str], timeout: int = 5) -> str:
        """Waits for an element and returns its text content."""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            text = element.text.strip()
            logger.info(f"🟢 Text fetched from {locator}: '{text}'")
            return text
        except Exception as e:
            self._handle_error("get_text", locator, e)
            return ""

    # ------------------------------------------------------------
    # Wait Helpers
    # ------------------------------------------------------------
    def wait_until_clickable(self, locator: Tuple[str, str]):
        return self._wait_for_condition(EC.element_to_be_clickable(locator), "clickable", locator)

    def wait_until_visible(self, locator: Tuple[str, str],timeout:int=10):
        return self._wait_for_condition(EC.visibility_of_element_located(locator), "visible", locator)

    def wait_until_present(self, locator: Tuple[str, str]):
        return self._wait_for_condition(EC.presence_of_element_located(locator), "present", locator)

    def wait_invisible(self, locator: Tuple[str, str]):
        """Waits until element becomes invisible."""
        try:
            self.wait.until(EC.invisibility_of_element_located(locator))
            logger.info(f"🕓 Element became invisible: {locator}")
        except Exception as e:
            self._handle_error("wait_invisible", locator, e)

    # ------------------------------------------------------------
    # Special Waits
    # ------------------------------------------------------------
    def wait_loader_to_disappear(self, locator: Tuple[str, str], timeout: int = 10):
        """Waits for loader animation to disappear."""
        try:
            wait = WebDriverWait(self.driver, timeout)
            try:
                wait.until(EC.presence_of_element_located(locator))
                logger.info("🔄 Loader appeared.")
            except TimeoutException:
                logger.info("ℹ️ Loader did not appear, continuing.")
            wait.until(EC.invisibility_of_element_located(locator))
            logger.info("✅ Loader disappeared.")
        except Exception as e:
            self._handle_error("wait_loader_to_disappear", locator, e)

    def wait_until_clickable_modal(self, locator: Tuple[str, str], timeout: int = 30, retries: int = 1):
        """Retries until modal element is clickable."""
        for attempt in range(retries + 1):
            try:
                element = WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))
                logger.info(f"🟩 Modal element clickable: {locator}")
                return element
            except Exception as e:
                logger.warning(f"Retry {attempt + 1}/{retries + 1} failed for {locator}: {e}")
                if attempt == retries:
                    self._handle_error("wait_until_clickable_modal", locator, e)

    def wait_for_page_load(self, timeout: int = 30):
        """Waits for page readyState to be complete."""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            logger.info("🌐 Page fully loaded.")
        except Exception as e:
            logger.error(f"Page did not load completely: {e}", exc_info=True)
            raise

    def wait_for_filter_ui_ready(self, timeout: int = 10):
        """Waits for Filter UI fields to appear."""
        locator = (By.XPATH, "//input[contains(@id,'attributeValue_')]")
        try:
            WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))
            logger.info("✅ Filter UI ready.")
        except TimeoutException:
            logger.warning("⚠️ Filter UI not ready within timeout.")

    # ------------------------------------------------------------
    # Utility Functions
    # ------------------------------------------------------------
    def alert_is_present(self, timeout: int = 10):
        """Waits for browser alert and returns it."""
        try:
            alert = WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
            logger.info("🔔 Alert present.")
            return alert
        except Exception as e:
            self._handle_error("alert_is_present", ("alert", "alert_box"), e)

    def check_element_presence(self, locator: Tuple[str, str], timeout: int = 2) -> bool:
        """Checks if element is present (non-failing)."""
        try:
            WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False
        except Exception as e:
            logger.error(f"Error during presence check for {locator}: {e}", exc_info=True)
            return False

    # ------------------------------------------------------------
    # Internal Helpers
    # ------------------------------------------------------------
    def _wait_for_condition(self, condition, name: str, locator: Tuple[str, str]):
        """Internal helper for unified wait handling."""
        try:
            element = self.wait.until(condition)
            logger.info(f"🕓 Element {name}: {locator}")
            return element
        except Exception as e:
            self._handle_error(f"wait_until_{name}", locator, e)

    def _handle_error(self, action: str, locator: Tuple[str, str], error: Exception):
        """Centralized error handling with screenshot and logging."""
        name = locator[1].replace("/", "_") if len(locator) > 1 else str(locator)
        Screenshot.take(self.driver, f"{action}_error_{name}")
        logger.error(f"❌ {action} failed for {locator}: {error}", exc_info=True)
        raise error

    def wait_until_url_contains(self, substring, timeout=10):
        """
        Waits until the current URL contains the given substring.
        Useful for verifying navigation or redirects.
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.url_contains(substring)
            )
            return True
        except Exception as e:
            print(
                f"Timeout: URL did not contain '{substring}' within {timeout} seconds. Current URL: {self.driver.current_url}")
            return False
