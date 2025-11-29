from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from pages.base_page import BasePage
# A dictionary to hold the base locators for each slider block
from pages.common.loader import Loader
from utils.logger import get_logger

logger = get_logger(__name__)


class TimeRangeFilter(BasePage):
    SLIDER_LOCATORS = {
        "Session Time": (By.XPATH, "//label[text()='Session Time']/following-sibling::div"),
        "Ring Time": (By.XPATH, "//label[text()='Ring Time']/following-sibling::div"),
        "Talk Time": (By.XPATH, "//label[text()='Talk Time']/following-sibling::div"),
        "Wrapup Time": (By.XPATH, "//label[text()='Wrapup Time']/following-sibling::div"),
    }

    # Locators for the handles *relative to the slider block*
    LOWER_HANDLE = (By.CSS_SELECTOR, ".noUi-handle-lower")
    UPPER_HANDLE = (By.CSS_SELECTOR, ".noUi-handle-upper")

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.actions = ActionChains(driver)

    def get_current_value(self, filter_name):
        """Read the currently selected lower slider value for the time-range filter."""

        # Each time slider usually has an input storing the actual value
        slider_input = self.wait_until_visible((
            By.XPATH,
            f"//label[text()='{filter_name}']/following::input[contains(@class,'range-value-lower')][1]"
        ))

        return slider_input.get_attribute("value")

    def set_slider_range(self, slider_name, handle_type, offset_x):
        """
        Adjusts a noUiSlider handle by dragging it a certain number of pixels
        and forces a JavaScript event to ensure the filter updates the search.
        """
        if slider_name not in self.SLIDER_LOCATORS:
            # NOTE: Using a hypothetical logger here based on your snippet
            # If logger is not defined, use print() instead.
            if hasattr(self, 'logger'):
                self.logger.info(f"Invalid slider name: {slider_name}")
            print(f"Error: Slider '{slider_name}' not recognized.")
            return

        try:
            # 1. Locate the main slider container
            slider_container_locator = self.SLIDER_LOCATORS[slider_name]
            slider_container = self.driver.find_element(*slider_container_locator)

            # 2. Locate the specific handle within the container
            if handle_type.lower() == 'lower':
                handle_locator = self.LOWER_HANDLE
            elif handle_type.lower() == 'upper':
                handle_locator = self.UPPER_HANDLE
            else:
                if hasattr(self, 'logger'):
                    self.logger.info(f"Invalid handle type: {handle_type}")
                print("Error: handle_type must be 'lower' or 'upper'.")
                return

            handle = slider_container.find_element(*handle_locator)

            # 3. Use ActionChains to drag the handle
            self.actions.drag_and_drop_by_offset(
                handle,
                offset_x,  # Move horizontally
                0  # Do not move vertically
            ).perform()

            # 4. 🔥 CRITICAL FIX: Trigger necessary JavaScript events after the drag.
            # This simulates releasing the mouse and signals the 'noUiSlider' library
            # and the application's change listener that the value has been set.
            self.driver.execute_script("arguments[0].dispatchEvent(new Event('mouseup', { bubbles: true }));", handle)
            self.driver.execute_script("arguments[0].dispatchEvent(new Event('change', { bubbles: true }));", handle)

            if hasattr(self, 'logger'):
                self.logger.info(f"✅ Adjusted {slider_name} ({handle_type}) by {offset_x} pixels and fired events.")
            print(f"✅ Adjusted {slider_name} ({handle_type}) by {offset_x} pixels. Filter should be applied.")

        except Exception as e:
            if hasattr(self, 'logger'):
                self.logger.info(f"Failed to adjust {slider_name} slider: {e}")
            print(f"🔥 Failed to adjust {slider_name} slider: {e}")