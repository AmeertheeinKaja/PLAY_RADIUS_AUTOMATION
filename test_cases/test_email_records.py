import time

import pytest
from selenium.webdriver.common.by import By

from pages.login.login import LoginPage
from pages.login.logout import Logout
from pages.record.ai_insights_page import AIInsightsPage
from pages.record.rating_page import RatingPage
from pages.record.record_controls.record_page_tabs import RecordPageTabs
from pages.record.record_page import RecordPage
from pages.record.record_manager import RecordManager
from pages.filtering.filter_record_by_attribute import FilterByAttribute
from pages.common.open_filter_search import FilterSearch
from pages.common.submit_search_filter import SubmitFilterSearch
from utils.data_reader import load_test_data
from pages.common.sidemenupage import SideMenuPage

from pages.common.loader import Loader
@pytest.mark.usefixtures("driver_function")
class TestEmailRecords:
    def test_email_records(self, driver_function):
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
        record_tabs = RecordPageTabs(driver_function)
        ai_insights_page = AIInsightsPage(driver_function)
        rating_page = RatingPage(driver_function)

        # Step 1: Open login page
        login_page.open()

        # Step 2: Login
        login_page.login()

        # Step 3: Wait for loader to disappear (page load)
        loader.load()
        open_filter.filter()
        filter_record.search("Channel","email")
        filter_record.search( "Interaction Type", "ob")
        # filter_record.search("Record ID","DY1766569181437AA")
        filter_action.searchFilter()
        record_manager.view_record()
        record_page.error_message = record_manager.toast_text
        record_page.process_current_record()

        # record_tabs.switch_tabs("ai_insights")
        # ai_insights_page.ai_insights_info()
        # record_tabs.switch_tabs("ratings")
        # record_tabs.switch_tabs("comments")

        # Step 5: Logout at end
        logout_page.logout()