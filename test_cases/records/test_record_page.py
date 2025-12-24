import time

import pytest
from selenium.webdriver.common.by import By

from pages.login.login import LoginPage
from pages.login.logout import Logout
from pages.record.record_page import RecordPage
from pages.record.record_manager import RecordManager

from pages.common.loader import Loader
from utils.data_reader import load_test_data


@pytest.mark.usefixtures("driver_function")
class TestAllRecordPage:
    full_cfg = load_test_data("process/create_process.json")
    def test_records(self, driver_function):
        """Verify All Records page loads after login."""

        login_page = LoginPage(driver_function)
        logout_page = Logout(driver_function)
        loader = Loader(driver_function)
        record_manager = RecordManager(driver_function)
        record_page = RecordPage(driver_function)

        # Step 1: Open login page
        login_page.open()

        # Step 2: Login
        login_page.login()

        # Step 3: Wait for loader to disappear (page load)
        loader.load()
        record_manager.view_record()
        record_page.record_info()
        record_page.open_process_page()
        # Step 4: Navigate to Records page

        # Step 5: Logout at end
        logout_page.logout()