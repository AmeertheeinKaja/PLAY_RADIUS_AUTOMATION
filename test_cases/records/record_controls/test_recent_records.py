import pytest

from pages.login.login import LoginPage
from pages.login.logout import Logout
from pages.record.record_manager import RecordManager
from pages.filtering.filter_record_by_attribute import FilterByAttribute
from pages.common.open_filter_search import FilterSearch
from pages.common.submit_search_filter import SubmitFilterSearch
from pages.common.sidemenupage import SideMenuPage
from pages.record.record_controls.record_navigator import RecordNavigator
from pages.record.record_controls.record_recent_record import RecentRecordsMenu

from pages.common.loader import Loader
@pytest.mark.usefixtures("driver_function")
class TestRecentRecords:
    def test_recent_records(self, driver_function):
        login_page = LoginPage(driver_function)
        logout_page = Logout(driver_function)
        loader = Loader(driver_function)
        record_manager = RecordManager(driver_function)

        filter_record = FilterByAttribute(driver_function)
        open_filter = FilterSearch(driver_function)
        filter_action = SubmitFilterSearch(driver_function)
        side_menu_page = SideMenuPage(driver_function)
        recent_records_menu = RecentRecordsMenu(driver_function)

        # Step 1: Login
        login_page.open()
        login_page.login()
        loader.load()

        # ---- Helper function for filtering + viewing ---- #
        def open_record(record_id):
            side_menu_page.record()
            open_filter.filter()
            filter_record.search("Record ID", record_id)
            filter_action.searchFilter()
            record_manager.view_record()


        # Open 4 different records to populate recent list
        open_record("AM1765375699855QA")
        open_record("BM1765375700009QA")
        open_record("GT1765361493705UC")
        open_record("BA1765360397852PC")

        # ---- Validate Recent Records Menu clicks ---- #
        recent_records_menu.click_record_by_href_id("AM1765375699855QA")
        loader.load()

        recent_records_menu.click_record_by_href_id("GT1765361493705UC")
        loader.load()

        recent_records_menu.click_record_by_href_id("BM1765375700009QA")
        loader.load()

        # Step 5: Logout
        logout_page.logout()