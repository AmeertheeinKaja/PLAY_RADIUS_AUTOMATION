import pytest

from flow.filter_flow import FilterFlow
from pages.login.login import LoginPage
from pages.common.loader import Loader
from pages.common.open_filter_search import FilterSearch
from pages.process.process_manager.process_filter import ProcessFilter # Assuming this class exists
from pages.common.sidemenupage import SideMenuPage
from pages.common.submit_search_filter import SubmitFilterSearch

from pages.login.logout import Logout
from utils.screenshot import Screenshot
from utils.logger import get_logger
from utils.data_reader import load_test_data# Assuming this utility exists

# ... existing imports ...

logger = get_logger(__name__)


@pytest.mark.usefixtures("driver_function")
class TestProcessFilter:
    def test_filter_process_by_name(self, driver_function):
        login = LoginPage(driver_function)
        loader = Loader(driver_function)
        logout = Logout(driver_function)
        side_menu = SideMenuPage(driver_function)
        open_filter = FilterSearch(driver_function)

        process_filter_page = ProcessFilter(driver_function)

        logger.info("Starting test_filter_process_by_name")

        logger.info("Opening login page...")
        login.open()
        logger.info("Login page opened.")

        logger.info("Attempting login...")
        login.login()
        logger.info("Login complete.")

        logger.info("Waiting for page to load after login...")
        loader.load()
        logger.info("Page loaded.")

        logger.info("Navigating to Process section via Side Menu...")
        side_menu.process()  # Assuming this navigates to the process list page
        logger.info("Navigated to Process section.")

        logger.info("Opening filter search section...")
        # Assuming filter_flow can be used for process filtering, or you have a dedicated flow
        open_filter.filter() # Open the filter search section
        logger.info("Filter search section opened.")

        logger.info("Reading test data for process filtering...")
        test_data = load_test_data("process/filter_process.json")
        process_name = test_data["processName"]
        logger.info(f"Test data loaded. Filtering by process name: {process_name}")

        logger.info("Applying the filter...")
        process_filter_page.apply_filter_by_name(process_name)
        logger.info("Filter applied.")

        # logger.info("Submitting filter search...")
        # submit_filter = SubmitFilterSearch(driver_function)
        # submit_filter.searchFilter()
        # logger.info("Filter search submitted.")

        # Add assertions here to verify the filtering
        logger.info("Verifying filtered processes...")
        assert process_filter_page.verify_filtered_processes(process_name), \
            f"Process filtering failed for name: {process_name}"
        logger.info(f"Successfully filtered and verified processes by name: {process_name}")

        logger.info("Logging out...")
        logout.logout()
        logger.info("Logout complete. Test finished.")


    def test_filter_process_by_code(self,driver_function):
        login = LoginPage(driver_function)
        loader = Loader(driver_function)
        logout = Logout(driver_function)
        side_menu = SideMenuPage(driver_function)
        action_filter = SubmitFilterSearch(driver_function)
        process_filter_page = ProcessFilter(driver_function)
        open_filter = FilterSearch(driver_function)

        logger.info("Starting test_filter_process_by_code")

        login.open()
        login.login()
        loader.load()
        logger.info("Login complete and page loaded.")

        side_menu.process()
        loader.load()
        logger.info("Navigated to Process section.")

        logger.info("Opening filter panel and applying filter by code...")
        test_data = load_test_data("process/filter_process.json")
        process_code = test_data["processCode"]  # Assuming "process_code" exists in your JSON

        open_filter.filter()
        process_filter_page.clear_and_type(process_filter_page._PROCESS_CODE_INPUT, process_code)
        logger.info(f"Entered process code: {process_code}")
        process_filter_page.click(process_filter_page._SUBMIT_FILTER_BUTTON)
        process_filter_page.loader.load()
        process_filter_page.wait_for_page_load()
        logger.info("Filter applied by code and page loaded.")

        logger.info("Verifying filtered processes by code...")
        assert process_filter_page.verify_filtered_processes(process_code), \
            f"Process filtering failed or verification returned false for code: {process_code}"
        logger.info(f"Successfully filtered and verified processes by code: {process_code}")

        logout.logout()
        logger.info("Logout complete. Test finished.")


    def test_filter_process_by_rating_enabled(self, driver_function):
        login = LoginPage(driver_function)
        loader = Loader(driver_function)
        logout = Logout(driver_function)
        side_menu = SideMenuPage(driver_function)
        process_filter_page = ProcessFilter(driver_function)
        open_filter = FilterSearch(driver_function)

        logger.info("Starting test_filter_process_by_rating_enabled")

        login.open()
        login.login()
        loader.load()
        side_menu.process()
        loader.load()
        logger.info("Navigated to Process section.")

        logger.info("Opening filter panel and applying filter by rating: Enabled...")
        open_filter.filter()
        process_filter_page.select_rating_element(
            rating_view="Enabled")  # You'll need to update apply_filter or create a new method for this
        process_filter_page.click(process_filter_page._SUBMIT_FILTER_BUTTON)
        process_filter_page.loader.load()
        process_filter_page.wait_for_page_load()
        logger.info("Filter applied by rating (Enabled) and page loaded.")

        # Verification will be different here. You'll need to check the 'Review & Ratings' column.
        # This will likely require a new verification method in ProcessFilter.
        # assert process_filter_page.verify_processes_by_rating_status("Enabled")
        logger.warning("Verification for rating status needs a dedicated method in ProcessFilter.")

        logout.logout()
        logger.info("Logout complete. Test finished.")


    def test_filter_process_by_rating_disabled(self, driver_function):
        login = LoginPage(driver_function)
        loader = Loader(driver_function)
        logout = Logout(driver_function)
        side_menu = SideMenuPage(driver_function)
        process_filter_page = ProcessFilter(driver_function)
        open_filter = FilterSearch(driver_function)

        logger.info("Starting test_filter_process_by_rating_disabled")

        login.open()
        login.login()
        loader.load()
        side_menu.process()
        loader.load()
        logger.info("Navigated to Process section.")

        logger.info("Opening filter panel and applying filter by rating: Disabled...")
        open_filter.filter()
        process_filter_page.select_rating_element(rating_view="Disabled")  # Update apply_filter or create a new method for this
        process_filter_page.click(process_filter_page._SUBMIT_FILTER_BUTTON)
        process_filter_page.loader.load()
        process_filter_page.wait_for_page_load()
        logger.info("Filter applied by rating (Disabled) and page loaded.")

        # Verification: assert process_filter_page.verify_processes_by_rating_status("Disabled")
        logger.warning("Verification for rating status needs a dedicated method in ProcessFilter.")

        logout.logout()
        logger.info("Logout complete. Test finished.")


    def test_clear_process_filter(self, driver_function):
        login = LoginPage(driver_function)
        loader = Loader(driver_function)
        logout = Logout(driver_function)
        side_menu = SideMenuPage(driver_function)
        process_filter_page = ProcessFilter(driver_function)
        open_filter = FilterSearch(driver_function)
        action_filter = SubmitFilterSearch(driver_function)

        logger.info("Starting test_clear_process_filter")

        login.open()
        login.login()
        loader.load()
        side_menu.process()
        loader.load()
        logger.info("Navigated to Process section.")
        open_filter.filter()

        logger.info("Applying a filter first...")
        test_data = load_test_data("process/filter_process.json")
        process_name = test_data["processName"]
        process_filter_page.apply_filter_by_name(process_name)
        logger.info("Filter applied.")

        # Optional: Verify filter was applied before clearing
        assert process_filter_page.verify_filtered_processes(process_name), \
            f"Pre-clear filter verification failed for name: {process_name}"
        logger.info("Pre-clear filter verified.")

        logger.info("Opening filter panel and clicking Clear button...")

        open_filter.filter()
        action_filter.clearFilter()
        open_filter.filter()

        # Make sure you have _CLEAR_FILTER_BUTTON defined in ProcessFilter.py
        # Example: _CLEAR_FILTER_BUTTON = (By.XPATH, "//button[normalize-space(text())='Clear']")

        process_filter_page.loader.load()
        process_filter_page.wait_for_page_load()
        logger.info("Filter cleared and page loaded.")

        # Verification: Check if filter inputs are empty
        assert process_filter_page.is_filter_input_empty(process_filter_page._PROCESS_NAME_INPUT), \
            "Process Name input field is not empty after clearing filter."
        assert process_filter_page.is_filter_input_empty(process_filter_page._PROCESS_CODE_INPUT), \
            "Process Code input field is not empty after clearing filter."
        # For the dropdown, you might want to check if the default "Choose" option is selected.
        # assert process_filter_page.get_selected_dropdown_text(process_filter_page._PROCESS_STATUS_SELECT) == "Choose"

        # Additional verification: Verify all processes are displayed (or default count)
        # This will require a new method to count/verify all processes.
        # assert process_filter_page.verify_all_processes_displayed()

        logger.info("Filter input fields verified as empty.")
        logout.logout()
        logger.info("Logout complete. Test finished.")


    def test_filter_no_matching_results(self, driver_function):
        login = LoginPage(driver_function)
        loader = Loader(driver_function)
        logout = Logout(driver_function)
        side_menu = SideMenuPage(driver_function)
        process_filter_page = ProcessFilter(driver_function)
        open_filter = FilterSearch(driver_function)

        logger.info("Starting test_filter_no_matching_results")

        login.open()
        login.login()
        loader.load()
        side_menu.process()
        loader.load()
        open_filter.filter()
        logger.info("Navigated to Process section.")

        logger.info("Applying filter with a non-existent process name...")
        non_existent_process = "NON_EXISTENT_PROCESS_XYZ"  # Use a unique name guaranteed not to exist
        process_filter_page.apply_filter_by_name(non_existent_process)
        logger.info(f"Filter applied with non-existent process name: {non_existent_process}")

        # Verification: Ensure "No records found" message is present
        assert process_filter_page.check_element_presence(process_filter_page._NO_RECORDS_MESSAGE, timeout=10), \
            "Expected 'No process found' message but it was not displayed."
        logger.info("'No process found' message correctly displayed.")

        # Optional: Assert that no process rows are visible


        logout.logout()
        logger.info("Logout complete. Test finished.")