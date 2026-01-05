import time

import pytest
from selenium.webdriver.common.by import By

from pages.login.login import LoginPage
from pages.login.logout import Logout
from pages.record.record_page import RecordPage
from pages.record.record_manager import RecordManager
from pages.filtering.filter_record_by_attribute import FilterByAttribute
from pages.common.open_filter_search import FilterSearch
from pages.common.submit_search_filter import SubmitFilterSearch
from utils.data_reader import load_test_data
from pages.common.sidemenupage import SideMenuPage

from pages.common.loader import Loader
@pytest.mark.usefixtures("driver_function")
class TestOpenRecordByID:
    def test_records(self, driver_function):
        full_cfg = load_test_data("process/create_process.json")
        """Verify All Records page loads after login."""

        login_page = LoginPage(driver_function)
        logout_page = Logout(driver_function)
        loader = Loader(driver_function)
        record_manager = RecordManager(driver_function)
        record_page = RecordPage(driver_function,full_cfg)
        filter_record = FilterByAttribute(driver_function)
        open_filter=FilterSearch(driver_function)
        filter_action=SubmitFilterSearch(driver_function)
        side_menu_page = SideMenuPage(driver_function)

        # Step 1: Open login page
        login_page.open()

        # Step 2: Login
        login_page.login()

        # Step 3: Wait for loader to disappear (page load)
        loader.load()
        open_filter.filter()
        filter_record.search("Record ID","ZT1766577430995NB")
        filter_action.searchFilter()
        record_manager.view_record()
        record_page.error_message=record_manager.toast_text
        record_page.record_info(record_page.error_message)
        # side_menu_page.record()
        # open_filter.filter()
        # filter_record.search("Record ID", "AM1765375699855QA")
        # filter_action.searchFilter()
        # record_manager.view_record()
        # record_page.open_record_from_sidebar("GL1765212080050QB")
        # record_page.open_process_page()
        # Step 4: Navigate to Records page

        # Step 5: Logout at end
        logout_page.logout()