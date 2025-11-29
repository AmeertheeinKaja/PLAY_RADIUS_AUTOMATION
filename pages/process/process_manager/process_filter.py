import logging
from typing import Tuple

from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from pages.common.loader import Loader

from pages.base_page import BasePage
from utils.data_reader import load_test_data
from utils.screenshot import Screenshot

logger = logging.getLogger(__name__)

# Load JSON only once
data = load_test_data("process/filter_process.json")


class ProcessFilter(BasePage):

    # Locators
    _PROCESS_NAME_INPUT = (By.ID, "processName")  # Changed from "processNameFilterInput"
    _PROCESS_CODE_INPUT = (By.ID, "processCode")  # Add if you also filter by code
    _PROCESS_STATUS_SELECT = (By.ID, "floatingSelect")  # Example for a select dropdown
    _SUBMIT_FILTER_BUTTON = (By.XPATH, "//button[normalize-space(text())='Submit']")
    _CLEAR_FILTER_BUTTON=(By.XPATH,"//button[normalize-space(text())='Clear']")# Based on log
    _FILTER_BUTTON_ICON_TO_OPEN_FILTER_PANEL = (By.XPATH,
                                                "//button[@title='Filter']")  # Assuming this opens the filter panel

    # This locator is crucial for verifying results
    _PROCESS_ROWS = (By.XPATH, "//table[contains(@class, 'rad_grid_table')]/tbody/tr")
    _PROCESS_NAME_IN_ROW = (By.XPATH, ".//td[1]//span[@class='record_title']")
      # Add this for no results scenario


    _NO_RECORDS_MESSAGE = (By.XPATH, "//td[contains(text(), 'No Process found')]")

    # Add a locator for the *first* process name element directly
    _FIRST_PROCESS_NAME_ELEMENT = (By.XPATH,
                                   "//table[contains(@class, 'rad_grid_table')]/tbody/tr[1]//td[1]//span[@class='record_title']")

    def __init__(self, driver):
        super().__init__(driver)
        self.loader= Loader(driver)

        # DEFAULT values from JSON
        self.processName = data.get("processName")
        self.processCode = data.get("processCode")

        rating_bool = data.get("ratingView")

        if rating_bool is True:
            self.ratingView = "Enabled"
        elif rating_bool is False:
            self.ratingView = "Disabled"
        else:
            self._initial_ratingView = "Choose"

        logger.info(f"Loaded defaults: Code={self.processCode}, Name={self.processName}, Rating={self.ratingView}")

    # ------------------------ POM Methods ------------------------

    def process_code_input(self):
        try:
            elem = self.wait_until_clickable(self._PROCESS_CODE_INPUT)
            elem.clear()
            elem.send_keys(self.processCode)
            logger.info(f"Entered Process Code: '{self.processCode}'")
        except Exception as e:
            logger.error(f"Failed to enter Process Code: {e}")
            raise

    def process_name_input(self):
        try:
            elem = self.wait_until_clickable(self._PROCESS_NAME_INPUT)
            elem.clear()
            elem.send_keys(self.processName)
            logger.info(f"Entered Process Name: '{self.processName}'")
        except Exception as e:
            logger.error(f"Failed to enter Process Name: {e}")
            raise

    def select_rating_element(self, rating_view: str = None): # <-- ADD THE PARAMETER
        """
        Selects an option from the Review & Ratings dropdown.
        If rating_view is provided, it overrides the default/JSON value.
        """
        target_rating_view = rating_view if rating_view is not None else self._initial_ratingView

        try:
            rating_element = self.wait_until_clickable(self._PROCESS_STATUS_SELECT)
            rating_dropdown = Select(rating_element)
            rating_dropdown.select_by_visible_text(target_rating_view) # Use the target_rating_view
            logger.info(f"Selected Rating View: '{target_rating_view}'")
        except Exception as e:
            logger.error(f"Failed to select Rating View '{target_rating_view}': {e}")
            raise

    def submit(self):
        try:
            submit_btn = self.wait_until_clickable(self._SUBMIT_FILTER_BUTTON)
            submit_btn.click()

            screenshot_name = "process_filter_form_filled"
            Screenshot.take(self.driver, screenshot_name)
            logger.info(f"Screenshot taken: {screenshot_name}.png")

        except Exception as e:
            logger.error(f"Submit button click failed: {e}")
            raise

    # ------------------------ Wrapper Method ------------------------

        # ... existing code ...

        def apply_filter(self, processCode=None, processName=None, ratingView=None):
            """
            Apply filter using either:
            - Passed parameters (override)
            - OR defaults loaded from JSON
            """

            # Override values if provided
            if processCode is not None:
                self.processCode = processCode
            if processName is not None:
                self.processName = processName
            target_rating_view_for_this_call = None
            if ratingView is not None:
                if ratingView is True:
                    target_rating_view_for_this_call = "Enabled"
                elif ratingView is False:
                    target_rating_view_for_this_call = "Disabled"
                else:
                    target_rating_view_for_this_call = "Choose"
            else:
                target_rating_view_for_this_call = self._initial_ratingView  # Fallback to initial if not overridden
            logger.info(
                f"Final Filter Data => Code: {self.processCode}, Name: {self.processName}, Rating: {target_rating_view_for_this_call}"
                # <--- Corrected here
            )
            # Execute filter steps
            self.process_code_input()
            self.process_name_input()
            self.select_rating_element(rating_view=target_rating_view_for_this_call)
            self.submit()
            self.loader.load()

    # ... rest of the file ...

    def open_filter_panel(self):
        """Opens the filter panel if it's not already open."""
        # You might need to check if the panel is already open before clicking
        if not self.check_element_presence(self._PROCESS_NAME_INPUT,
                                           timeout=2):  # Quick check if filter inputs are visible
            self.click(self._FILTER_BUTTON_ICON_TO_OPEN_FILTER_PANEL)
            self.wait_until_visible(self._PROCESS_NAME_INPUT)  # Wait for a specific input field to be visible
            logger.info("Filter panel opened.")
        else:
            logger.info("Filter panel already open.")

    def apply_filter_by_name(self, process_name: str):
        """Applies a filter by process name."""
        self.open_filter_panel()  # Ensure the panel is open

        self.clear_and_type(self._PROCESS_NAME_INPUT, process_name)  # Use clear_and_type
        logger.info(f"Entered process name: {process_name}")
        # Assuming you submit the filter after entering the name, otherwise you might need to click on submit_filter_button separately
        self.click(self._SUBMIT_FILTER_BUTTON)
        self.loader.load()  # Wait for a loader to disappear after applying filter
        self.wait_for_page_load()  # Wait for page to be ready after filter submission
        logger.info("Filter applied by name and page loaded.")


        # ... existing code ...

    def read_text(self):
        element = self.wait_until_visible(self._PROCESS_NAME_IN_ROW)
        return element.text.strip()

    def is_filter_input_empty(self, locator: Tuple[str, str], timeout: int = 5) -> bool:
        """
        Checks if a filter input field is empty by getting its 'value' attribute.
        """
        try:
            input_value = self.get_input_value(locator, timeout=timeout)
            is_empty = input_value == ""
            logger.info(f"Input field {locator} value is '{input_value}'. Is empty: {is_empty}")
            return is_empty
        except Exception as e:
            logger.error(f"Failed to check if input {locator} is empty: {e}", exc_info=True)
            return False

    def verify_filtered_processes(self, expected_process_name: str) -> bool:
        """
        Verifies that only processes matching the expected_process_name are displayed.
        """
        self.wait_for_page_load()  # Ensure the page is fully loaded after filtering

        # Check for "No records found" message first
        if self.check_element_presence(self._NO_RECORDS_MESSAGE, timeout=5):
            logger.info("No records found message is displayed.")
            return False

        # --- CRITICAL CHANGE HERE ---
        # Instead of waiting for generic rows, wait for the first specific process name to be visible
        try:
            self.wait_until_visible(self._FIRST_PROCESS_NAME_ELEMENT, timeout=20)
            logger.debug(f"First process name element found and visible: {self._FIRST_PROCESS_NAME_ELEMENT}")
        except Exception as e:
            logger.error(f"First process name element ({self._FIRST_PROCESS_NAME_ELEMENT}) did not become visible after filtering: {e}")
            Screenshot.take(self.driver, "first_process_name_not_visible")
            return False
        # --- END CRITICAL CHANGE ---


        process_names_on_page = []
        process_elements = self.find_elements(self._PROCESS_ROWS) # Use _PROCESS_ROWS to get ALL rows
        logger.debug(f"Number of process rows found by _PROCESS_ROWS after first element visible: {len(process_elements)}")

        if not process_elements:
            logger.warning("find_elements returned an empty list for _PROCESS_ROWS, even though first element was visible.")
            return False

        for i, element in enumerate(process_elements):
            try:
                name_element = element.find_element(*self._PROCESS_NAME_IN_ROW)
                extracted_name = name_element.text.strip()
                process_names_on_page.append(extracted_name)
                logger.debug(f"Extracted process name from row {i+1}: '{extracted_name}'")
            except Exception as e:
                logger.warning(f"Could not extract process name from row {i+1} using '{self._PROCESS_NAME_IN_ROW}': {e}")
                Screenshot.take(self.driver, f"extraction_fail_row_{i+1}")
                continue

        logger.info(f"Final list of process names extracted from page: {process_names_on_page}")
        logger.info(f"Expected process name for comparison: '{expected_process_name}'")

        if not process_names_on_page:
            logger.warning("No process names extracted from rows, leading to verification failure.")
            return False

        all_match = all(expected_process_name.lower() in name.lower() for name in process_names_on_page)

        if not all_match:
            logger.error(
                f"Mismatch in filtered processes. Expected to find '{expected_process_name.lower()}' in all names. "
                f"Actual names (lowercased for comparison): {[name.lower() for name in process_names_on_page]}")
            Screenshot.take(self.driver, "filtered_process_mismatch")
            return False

        logger.info(
            f"Successfully verified filtered processes. All displayed processes contain '{expected_process_name}'.")
        return True
