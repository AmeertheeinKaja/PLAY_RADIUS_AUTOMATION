import pytest

from pages.login.login import LoginPage
from pages.login.logout import Logout
from pages.record.record_manager import RecordManager
from pages.filtering.filter_record_by_attribute import FilterByAttribute
from pages.common.open_filter_search import FilterSearch
from pages.common.submit_search_filter import SubmitFilterSearch
from pages.record.record_controls.record_page_tabs import RecordPageTabs
from pages.record.ai_insights_page import AIInsightsPage

from pages.common.loader import Loader

@pytest.mark.usefixtures("driver_function")
class TestAIInsights:
    def test_ai_insight(self, driver_function):


        login_page = LoginPage(driver_function)
        logout_page = Logout(driver_function)
        loader = Loader(driver_function)
        record_manager = RecordManager(driver_function)

        filter_record = FilterByAttribute(driver_function)
        open_filter=FilterSearch(driver_function)
        filter_action=SubmitFilterSearch(driver_function)
        record_tabs = RecordPageTabs(driver_function)
        ai_insights_page = AIInsightsPage(driver_function)


        # Step 1: Open login page
        login_page.open()

        # Step 2: Login
        login_page.login()

        # Step 3: Wait for loader to disappear (page load)
        loader.load()
        open_filter.filter()
        filter_record.search("Record ID","PJ1765275884807SA")
        filter_action.searchFilter()
        record_manager.view_record()
        record_tabs.switch_tabs("ai_insights")
        ai_insights_page.ai_insights_info()




        # Step 5: Logout at end
        logout_page.logout()