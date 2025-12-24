import pytest

from pages.login.login import LoginPage
from pages.login.logout import Logout
from pages.record.record_page import RecordPage
from pages.record.record_manager import RecordManager
from pages.filtering.filter_record_by_attribute import FilterByAttribute
from pages.common.open_filter_search import FilterSearch
from pages.common.submit_search_filter import SubmitFilterSearch
from utils.data_reader import load_test_data
from pages.common.sidemenupage import SideMenuPage
from pages.record.record_controls.record_navigator import RecordNavigator

from pages.common.loader import Loader
@pytest.mark.usefixtures("driver_function")
class TestRecordControls:
    def test_records_controls(self, driver_function):
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
        record_action=RecordNavigator(driver_function)
        side_menu_page = SideMenuPage(driver_function)

        # Step 1: Open login page
        login_page.open()

        # Step 2: Login
        login_page.login()

        # Step 3: Wait for loader to disappear (page load)
        loader.load()
        # open_filter.filter()
        # filter_record.search("Record ID","AM1765375699855QA")
        # filter_action.searchFilter()
        record_manager.view_record()
        record_action.navigate_next_record()
        record_action.navigate_next_record()
        record_action.navigate_next_record()
        record_action.navigate_prev_record()
        record_action.navigate_prev_record()
        record_action.navigate_prev_record()
        record_action.navigate_prev_record()
        record_action.close_record()


        # Step 5: Logout at end
        logout_page.logout()

    def test_records_iterate_all(self, driver_function):

        login_page = LoginPage(driver_function)
        logout_page = Logout(driver_function)
        loader = Loader(driver_function)
        record_manager = RecordManager(driver_function)

        filter_record = FilterByAttribute(driver_function)
        open_filter=FilterSearch(driver_function)
        filter_action=SubmitFilterSearch(driver_function)
        record_action=RecordHandler(driver_function)
        side_menu_page = SideMenuPage(driver_function)

        # Step 1: Open login page
        login_page.open()

        # Step 2: Login
        login_page.login()

        # Step 3: Wait for loader to disappear (page load)
        loader.load()
        # open_filter.filter()
        # filter_record.search("Record ID","AM1765375699855QA")
        # filter_action.searchFilter()
        record_manager.view_record()
        record_action.iterate_all_records()



        # Step 5: Logout at end
        logout_page.logout()