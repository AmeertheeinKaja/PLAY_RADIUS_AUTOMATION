import pytest

from pages.login.login import LoginPage
from pages.login.logout import Logout
from pages.record.record_manager import RecordManager
from pages.filtering.filter_record_by_attribute import FilterByAttribute
from pages.common.open_filter_search import FilterSearch
from pages.common.submit_search_filter import SubmitFilterSearch
from pages.record.record_controls.record_page_tabs import RecordPageTabs
from pages.record.comments_page import CommentsPage
from utils.data_reader import load_test_data

from pages.common.loader import Loader

@pytest.mark.usefixtures("driver_function")
class TestComments:
    def test_comment(self, driver_function):


        login_page = LoginPage(driver_function)
        logout_page = Logout(driver_function)
        loader = Loader(driver_function)
        record_manager = RecordManager(driver_function)

        filter_record = FilterByAttribute(driver_function)
        open_filter=FilterSearch(driver_function)
        filter_action=SubmitFilterSearch(driver_function)
        record_tabs = RecordPageTabs(driver_function)
        comments = CommentsPage(driver_function)


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
        record_tabs.switch_tabs("comments")
        data = load_test_data("record/comments/commentData.json")

        # Add comments
        for text in data["add"]:
            comments.type_comment(text)
            comments.click_submit()


        # ────────────────────────────────────────────────────────────
        # -----------------------------------------------------
        # EDIT last comment
        # -----------------------------------------------------
        comments.edit_comment("This is my first comment")
        comments.type_comment("Updated text 1")
        comments.click_submit()

        comments.delete_comment("Customer asked for callback update")

        # -----------------------------------------------------
        # DELETE last comment AFTER DOM refresh
        # # -----------------------------------------------------
        # last_index = comments.get_comment_count()  # recalc index!
        # comments.delete_comment_by_index(last_index)

        # Step 5: Logout at end
        logout_page.logout()