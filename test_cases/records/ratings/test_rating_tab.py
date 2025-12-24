import pytest

from pages.login.login import LoginPage
from pages.login.logout import Logout
from pages.record.record_manager import RecordManager
from pages.filtering.filter_record_by_attribute import FilterByAttribute
from pages.common.open_filter_search import FilterSearch
from pages.common.submit_search_filter import SubmitFilterSearch
from pages.record.record_controls.record_page_tabs import RecordPageTabs
from pages.record.rating_page import RatingPage
from pages.common.loader import Loader


@pytest.mark.usefixtures("driver_function")
class TestRatingPage:

    def test_rating_page(self, driver_function):

        login_page = LoginPage(driver_function)
        logout_page = Logout(driver_function)
        loader = Loader(driver_function)

        record_manager = RecordManager(driver_function)
        filter_record = FilterByAttribute(driver_function)
        open_filter = FilterSearch(driver_function)
        filter_action = SubmitFilterSearch(driver_function)

        record_tabs = RecordPageTabs(driver_function)
        rating_page = RatingPage(driver_function)

        # -------------------------------
        # Login
        # -------------------------------
        login_page.open()
        login_page.login()
        loader.load()

        # -------------------------------
        # Open Record
        # -------------------------------
        open_filter.filter()
        filter_record.search("Record ID", "PJ1765275884807SA")
        filter_action.searchFilter()
        loader.load()

        record_manager.view_record()
        loader.load()
        record_tabs.switch_tabs("ratings")
        loader.load()

        tabs = rating_page.get_all_tabs()

        for tab in tabs:
            rating_page.switch_to_tab(tab.text.strip())
            rating_page.answer_all_questions(strategy="random")

        rating_page.calculate_score()
        rating_page.submit_rating()

        # -------------------------------
        logout_page.logout()
