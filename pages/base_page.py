# ... existing imports ...
import time
from typing import Tuple # Ensure this import is present at the top
from selenium.common import TimeoutException
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.logger import get_logger
from utils.screenshot import Screenshot

logger = get_logger(__name__)

class BasePage:
    """Base class providing reusable Selenium actions and waits."""

    def __init__(self, driver, timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout) # Default WebDriverWait object

    def click(self, locator: Tuple[str, str]):
        """Clicks an element after waiting until it's clickable."""
        try:
            element = self.wait_until_clickable(locator)
            element.click()
            logger.info(f"Clicked element: {locator}")
        except Exception as e:
            self._handle_error("click", locator, e)

    def send_keys(self, locator: Tuple[str, str], text: str):
        """Clears an input field and sends text."""
        try:
            element = self.wait_until_visible(locator)
            element.clear()
            element.send_keys(text)
            logger.info(f"Sent keys to {locator}: {text}")
        except Exception as e:
            self._handle_error("send_keys", locator, e)

    def get_text(self, locator: Tuple[str, str], timeout: int = 5) -> str:
        """Waits for an element and returns its text content."""
        try:
            # This method already uses its own WebDriverWait, make sure it's consistent
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            text = element.text.strip()
            logger.info(f"Text fetched from {locator}: '{text}'")
            return text
        except Exception as e:
            self._handle_error("get_text", locator, e)
            return ""

    def wait_until_clickable(self, locator: Tuple[str, str], timeout: int = None): # MODIFIED: Added timeout parameter
        """
        Waits until an element is clickable.
        If timeout is provided, it overrides the default BasePage timeout for this wait.
        """
        wait_obj = WebDriverWait(self.driver, timeout) if timeout is not None else self.wait
        return self._wait_for_condition(wait_obj, EC.element_to_be_clickable(locator), "clickable", locator)

    def wait_until_visible(self, locator: Tuple[str, str], timeout: int = None): # MODIFIED: Added timeout parameter
        """
        Waits until an element is visible.
        If timeout is provided, it overrides the default BasePage timeout for this wait.
        """
        wait_obj = WebDriverWait(self.driver, timeout) if timeout is not None else self.wait
        return self._wait_for_condition(wait_obj, EC.visibility_of_element_located(locator), "visible", locator)

    def wait_until_present(self, locator: Tuple[str, str], timeout: int = None): # MODIFIED: Added timeout parameter
        """
        Waits until an element is present in the DOM.
        If timeout is provided, it overrides the default BasePage timeout for this wait.
        """
        wait_obj = WebDriverWait(self.driver, timeout) if timeout is not None else self.wait
        return self._wait_for_condition(wait_obj, EC.presence_of_element_located(locator), "present", locator)


    def wait_invisible(self, locator: Tuple[str, str], timeout: int = None): # MODIFIED: Added timeout parameter
        """
        Waits until element becomes invisible.
        If timeout is provided, it overrides the default BasePage timeout for this wait.
        """
        wait_obj = WebDriverWait(self.driver, timeout) if timeout is not None else self.wait
        try:
            wait_obj.until(EC.invisibility_of_element_located(locator))
            logger.info(f"Element became invisible: {locator}")
        except Exception as e:
            self._handle_error("wait_invisible", locator, e)

    def wait_loader_to_disappear(self, locator: Tuple[str, str], timeout: int = 30,
                                 initial_check_timeout: int = 1):  # Increased default timeout for loader
        """
        Waits for loader animation to disappear.
        Includes a short initial check for loader presence to avoid long waits if loader doesn't appear,
        while ensuring the function completes its natural flow.
        """
        try:
            loader_present = False
            try:
                WebDriverWait(self.driver, initial_check_timeout).until(EC.presence_of_element_located(locator))
                loader_present = True
                logger.info("Loader appeared.")
            except TimeoutException:
                logger.debug(
                    f"Loader element {locator} did not appear within {initial_check_timeout}s. Assuming it's not present or disappeared quickly.")

            if loader_present:
                WebDriverWait(self.driver, timeout).until(
                    EC.invisibility_of_element_located(locator))  # Use the method's timeout
                logger.info("Loader disappeared.")
            else:
                logger.info(
                    "Loader was not observed during initial check, proceeding without waiting for invisibility.")

        except Exception as e:
            self._handle_error("wait_loader_to_disappear", locator, e)

    def wait_until_clickable_modal(self, locator: Tuple[str, str], timeout: int = 30, retries: int = 1):
        """Retries until modal element is clickable."""
        for attempt in range(retries + 1):
            try:
                # Use a local WebDriverWait here as this is a specific modal wait
                element = WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))
                logger.info(f"Modal element clickable: {locator}")
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
            logger.info("Page fully loaded.")
        except Exception as e:
            Screenshot.take(self.driver, "page_load_error")
            logger.error(f"Page did not load completely: {e}", exc_info=True)
            raise

    def wait_for_filter_ui_ready(self, timeout: int = 10):
        """Waits for Filter UI fields to appear."""
        locator = (By.XPATH, "//input[contains(@id,'attributeValue_')]")
        try:
            WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))
            logger.info("Filter UI ready.")
        except TimeoutException:
            logger.warning("Filter UI not ready within timeout.")

    def alert_is_present(self, timeout: int = 10):
        """Waits for browser alert and returns it."""
        try:
            alert = WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
            logger.info("Alert present.")
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
            Screenshot.take(self.driver, f"presence_check_error_{locator[1]}")
            return False

    def _wait_for_condition(self, wait_obj: WebDriverWait, condition, name: str, locator: Tuple[str, str]): # MODIFIED: Accepts wait_obj
        """Internal helper for unified wait handling."""
        try:
            element = wait_obj.until(condition) # Use the passed wait_obj
            logger.info(f"Element {name}: {locator}")
            return element
        except Exception as e:
            self._handle_error(f"wait_until_{name}", locator, e)

    def _handle_error(self, action: str, locator: Tuple[str, str], error: Exception):
        """Centralized error handling with screenshot and logging."""
        name = locator[1].replace("/", "_") if len(locator) > 1 else str(locator)
        Screenshot.take(self.driver, f"{action}_error_{name}")
        logger.error(f"{action} failed for {locator}: {error}", exc_info=True)
        raise error

    def wait_until_url_contains(self, substring, timeout: int = 10): # Added timeout type hint
        """
        Waits until the current URL contains the given substring.
        Useful for verifying navigation or redirects.
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.url_contains(substring)
            )
            logger.info(f"URL contains substring '{substring}' within {timeout} seconds.")
            return True
        except Exception as e:
            Screenshot.take(self.driver, f"url_contains_error_{substring}")
            logger.error(
                f"Timeout: URL did not contain '{substring}' within {timeout} seconds. Current URL: {self.driver.current_url}",
                exc_info=True
            )
            return False

    def clear_and_type(self, locator, text):
        try:
            element = self.wait_until_clickable(locator)
            element.click()
            element.send_keys(Keys.CONTROL, "a")
            element.send_keys(Keys.DELETE)
            element.send_keys(text)
            logger.info(f"Cleared and typed '{text}' in element: {locator}")
        except Exception as e:
            self._handle_error("clear_and_type", locator, e)

    def find_elements(self, locator):
        by, value = locator
        return self.driver.find_elements(by, value)

    def get_input_value(self, locator: Tuple[str, str], timeout: int = 5) -> str:
        """
        Waits for an input element to be visible and returns its 'value' attribute.
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            value = element.get_attribute("value")
            logger.info(f"Value fetched from input {locator}: '{value}'")
            return value if value is not None else ""
        except Exception as e:
            self._handle_error("get_input_value", locator, e)
            return ""

    def capture_toast(self, timeout=3):
        locator = (By.XPATH, "//div[@role='status']")
        end_time = time.time() + timeout
        last_valid = None

        while time.time() < end_time:
            elements = self.driver.find_elements(*locator)

            for el in elements:
                txt = el.text.strip()
                # Ignore Loading toast
                if txt and txt != "Loading...":
                    last_valid = txt

            time.sleep(0.1)

        if last_valid:
            logger.info(f"Toast captured (final): {last_valid}")
            return last_valid

        # fallback: return the last "Loading" if nothing else appears
        try:
            for el in self.driver.find_elements(*locator):
                txt = el.text.strip()
                if txt:
                    logger.info(f"Toast fallback: {txt}")
                    return txt
        except:
            pass

        logger.warning("Toast could not be captured.")
        return None

    def get_select(self, locator):
        element = self.wait_until_visible(locator)
        return Select(element)

    def is_element_present(self, locator):
        try:
            self.driver.find_element(*locator)
            return True
        except:
            return False

    def drag_scrollbar_slow(self, scroll_container):
        action = ActionChains(self.driver)
        start = scroll_container.location
        size = scroll_container.size

        start_x = start['x'] + size['width'] - 5
        start_y = start['y'] + 10

        end_y = start_y + size['height'] - 30

        steps = 10
        delta = (end_y - start_y) // steps

        action.move_to_element_with_offset(scroll_container, size['width'] - 5, 10)
        action.click_and_hold()

        for i in range(steps):
            action.move_by_offset(0, delta)
            action.pause(0.1)

        action.release().perform()

    def scroll_element_slow(self, element, step=300, pause=0.3):
        for _ in range(5):
            try:
                self.driver.execute_script(
                    "arguments[0].scrollTop += arguments[1];", element, step
                )
                time.sleep(pause)
            except Exception:
                break

    def is_clickable(self, locator, timeout=3):
        try:
            self.wait_until_clickable(locator, timeout=timeout)
            return True
        except:
            return False

    def scroll_and_click(self, locator, timeout=15):
        el = self.wait_until_present(locator, timeout=timeout)

        try:
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});", el
            )
        except:
            pass

        try:
            self.wait_until_clickable(locator, timeout=timeout).click()
            return
        except:
            pass

        try:
            self.driver.execute_script("arguments[0].click();", el)
            return
        except Exception as e:
            raise Exception(f"Cannot click element {locator} -> {e}")
