import pytest

from pages.login.login import LoginPage
from pages.login.logout import Logout
from pages.record.record_manager import RecordManager
from pages.filtering.filter_record_by_attribute import FilterByAttribute
from pages.common.open_filter_search import FilterSearch
from pages.common.submit_search_filter import SubmitFilterSearch
from pages.record.record_controls.record_page_tabs import RecordPageTabs
from pages.record.comments_page import CommentsPage
from pages.common.loader import Loader


# -------------------------------------------------------
# FIXTURE: Login + Open Record + Switch to Comments tab
# -------------------------------------------------------
@pytest.fixture
def open_comments_tab(driver_function):
    login = LoginPage(driver_function)
    logout = Logout(driver_function)
    loader = Loader(driver_function)

    record_manager = RecordManager(driver_function)
    filter_record = FilterByAttribute(driver_function)
    open_filter = FilterSearch(driver_function)
    submit_filter = SubmitFilterSearch(driver_function)
    tabs = RecordPageTabs(driver_function)
    comments = CommentsPage(driver_function)

    # Login
    login.open()
    login.login()
    loader.load()

    # Open record
    open_filter.filter()
    filter_record.search("Record ID", "PJ1765275884807SA")
    submit_filter.searchFilter()
    record_manager.view_record()

    # Switch to comments
    tabs.switch_tabs("comments")

    yield comments

    # Logout after test
    logout.logout()


# -------------------------------------------------------
# TEST SUITE
# -------------------------------------------------------
class TestCommentsSuite:

    def test_add_comment_success(self, open_comments_tab):
        comments = open_comments_tab

        text = "Automation comment success"
        comments.type_comment(text)
        comments.click_submit()

        assert "saved" in comments.last_toast.lower()

    def test_edit_comment(self, open_comments_tab):
        comments = open_comments_tab

        original = "Original comment"
        updated = "Updated automated comment"

        # Ensure comment exists
        comments.type_comment(original)
        comments.click_submit()

        # Edit
        comments.edit_comment(original)
        comments.type_comment(updated)
        comments.click_submit()

        assert "updated" in comments.last_toast.lower()

    def test_delete_comment(self, open_comments_tab):
        comments = open_comments_tab

        text = "Delete me"
        comments.type_comment(text)
        comments.click_submit()

        comments.delete_comment(text)

        assert (
            "deleted" in comments.last_toast.lower()
            or "saved" in comments.last_toast.lower()
        )

    def test_duplicate_comment_first_instance(self, open_comments_tab):
        comments = open_comments_tab

        duplicate = "Same comment duplicate"

        # Add twice
        comments.type_comment(duplicate)
        comments.click_submit()

        comments.type_comment(duplicate)
        comments.click_submit()

        # Delete first occurrence only
        comments.delete_comment(duplicate)

        # Second should still be editable
        comments.edit_comment(duplicate)

    def test_clear_comment_textarea(self, open_comments_tab):
        comments = open_comments_tab

        comments.type_comment("Some text to clear")
        comments.click_clear()

        # textarea should be empty
        textarea = comments.wait_until_visible(comments.ADD_TEXT_AREA)
        assert textarea.get_attribute("value") == ""
