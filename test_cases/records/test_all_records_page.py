import time

import pytest
from selenium.webdriver.common.by import By

from pages.login.login import LoginPage
from pages.login.logout import Logout
from pages.record.record_manager import RecordManager

from pages.common.loader import Loader
@pytest.mark.usefixtures("driver_function")
class TestAllRecordPage:
    def test_all_records_page_loads_successfully(self, driver_function):
        """Verify All Records page loads after login."""

        login_page = LoginPage(driver_function)
        logout_page = Logout(driver_function)
        loader = Loader(driver_function)

        # Step 1: Open login page
        login_page.open()

        # Step 2: Login
        login_page.login()

        # Step 3: Wait for loader to disappear (page load)
        loader.load()

        # Step 4: Now we can add verification for All Records Page
        # Example check: page title, URL, or table visibility
        assert "all-records" in driver_function.current_url.lower(), \
            "Failed to load All Records page after login."

        # Step 5: Logout at end
        logout_page.logout()

    def test_ui_elements(self, driver_function):
        """Verify all important UI elements exist on All Records page."""

        login_page = LoginPage(driver_function)
        logout_page = Logout(driver_function)
        loader = Loader(driver_function)

        # Step 1: Login
        login_page.open()
        login_page.login()
        loader.load()

        # --------- UI ELEMENT CHECKS ---------

        # 1. Filters button
        filter_btn = driver_function.find_element(
            By.XPATH, "//button[@title='Filter']"
        )
        assert filter_btn.is_displayed(), "Filters button is not visible."

        # 2. Page number (pagination)
        page_number = driver_function.find_element(
            By.XPATH, "//a[text()='1']"
        )
        assert page_number.is_displayed(), "Pagination page number not visible."

        # 3. Table (records list)
        table = driver_function.find_element(
            By.XPATH, "//table"
        )
        assert table.is_displayed(), "Records table is missing."

        # 4. Columns
        headers = [
            "Process Code",
            "Record ID",
            "Session Time",
            "Talk Time",
            "Interaction Type",
            "Contact Address",
            "Start At"
        ]

        for header in headers:
            element = driver_function.find_element(
                By.XPATH, f"//th[contains(., '{header}')]"
            )
            assert element.is_displayed(), f"Column '{header}' is not visible."

        # 5. Pagination Next Button
        next_btn = driver_function.find_element(
            By.XPATH, "//span[@title='Next']"
        )
        assert next_btn.is_enabled(), "Next page button should be enabled."

        # -------------------------------------

        logout_page.logout()
    def test_table_scroll(self, driver_function):
        login_page = LoginPage(driver_function)
        logout_page = Logout(driver_function)
        loader = Loader(driver_function)

        # Login
        login_page.open()
        login_page.login()
        loader.load()

        # Scrollable div (reliable locator)
        scroll_div = driver_function.find_element(
            By.XPATH,
            "//div[@class='wrapper_main']//div[contains(@style,'overflow')]"
        )

        # Initial scroll height
        initial_scroll = driver_function.execute_script(
            "return arguments[0].scrollTop;", scroll_div
        )

        # Scroll to bottom
        driver_function.execute_script(
            "arguments[0].scrollTop = arguments[0].scrollHeight;", scroll_div
        )
        time.sleep(2)

        # Final scroll height
        final_scroll = driver_function.execute_script(
            "return arguments[0].scrollTop;", scroll_div
        )

        assert final_scroll > initial_scroll, "Scrolling did not happen!"

        # Verify last row visible
        last_row = driver_function.find_elements(
            By.CSS_SELECTOR, "table.rad_grid_table tbody tr"
        )[-1]

        assert last_row.is_displayed(), "Last row is not visible after scrolling!"

