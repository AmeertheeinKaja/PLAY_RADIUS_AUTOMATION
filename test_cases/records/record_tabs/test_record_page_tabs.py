import time

import pytest

from pages.login.login import LoginPage
from pages.login.logout import Logout
from pages.record.record_manager import RecordManager
from pages.filtering.filter_record_by_attribute import FilterByAttribute
from pages.common.open_filter_search import FilterSearch
from pages.common.submit_search_filter import SubmitFilterSearch
from pages.record.record_controls.record_page_tabs import RecordPageTabs

from pages.common.loader import Loader

RECORD_IDS = [
    "AM1765375699855QA",
    "101020800",
    "CM1765375700109QA",
    "QU1765383423414EC",
    "PJ1765275884807SA",
]
@pytest.mark.usefixtures("driver_function")
class TestRecordTabs:
    def test_record_tabs(self, driver_function):


        login_page = LoginPage(driver_function)
        logout_page = Logout(driver_function)
        loader = Loader(driver_function)
        record_manager = RecordManager(driver_function)

        filter_record = FilterByAttribute(driver_function)
        open_filter=FilterSearch(driver_function)
        filter_action=SubmitFilterSearch(driver_function)
        record_tabs = RecordPageTabs(driver_function)


        # Step 1: Open login page
        login_page.open()

        # Step 2: Login
        login_page.login()

        # Step 3: Wait for loader to disappear (page load)
        loader.load()
        open_filter.filter()
        filter_record.search("Record ID","SS1753539105906BBH")
        filter_action.searchFilter()
        record_manager.view_record()
        record_tabs.switch_tabs("ai_insights")
        time.sleep(2)
        record_tabs.switch_tabs("comments")
        time.sleep(2)
        record_tabs.switch_tabs("ratings")
        time.sleep(2)
        record_tabs.open_home_tab()



        # Step 5: Logout at end
        logout_page.logout()

    @pytest.mark.parametrize("record_id", RECORD_IDS)
    def test_multi_record_tabs(self, driver_function, record_id):
        login_page = LoginPage(driver_function)
        logout_page = Logout(driver_function)
        loader = Loader(driver_function)
        record_manager = RecordManager(driver_function)

        filter_record = FilterByAttribute(driver_function)
        open_filter = FilterSearch(driver_function)
        filter_action = SubmitFilterSearch(driver_function)
        record_tabs = RecordPageTabs(driver_function)

        # Step 1: Open login page
        login_page.open()

        # Step 2: Login
        login_page.login()

        # Step 3: Wait for loader
        loader.load()

        # Step 4: Search record
        open_filter.filter()
        filter_record.search("Record ID", record_id)
        filter_action.searchFilter()

        # Step 5: View record
        record_manager.view_record()

        # Step 6: Switch tabs
        record_tabs.switch_tabs("ai_insights")
        time.sleep(1)
        record_tabs.switch_tabs("comments")
        time.sleep(1)
        record_tabs.switch_tabs("ratings")
        time.sleep(1)
        record_tabs.switch_tabs("media")
        record_tabs.open_home_tab()

        # Step 7: Logout
        logout_page.logout()