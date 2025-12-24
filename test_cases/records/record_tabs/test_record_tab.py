import pytest

from pages.login.login import LoginPage
from pages.login.logout import Logout
from pages.common.loader import Loader
from pages.record.record_manager import RecordManager
from pages.filtering.filter_record_by_attribute import FilterByAttribute
from pages.common.open_filter_search import FilterSearch
from pages.common.submit_search_filter import SubmitFilterSearch
from pages.record.record_controls.record_page_tabs import RecordPageTabs


@pytest.mark.usefixtures("driver_function")
class TestRecordTabs:

    @pytest.mark.sanity
    def test_record_tabs_navigation(self, driver_function):

        login_page = LoginPage(driver_function)
        logout_page = Logout(driver_function)
        loader = Loader(driver_function)
        record_manager = RecordManager(driver_function)

        filter_record = FilterByAttribute(driver_function)
        open_filter = FilterSearch(driver_function)
        filter_action = SubmitFilterSearch(driver_function)
        record_tabs = RecordPageTabs(driver_function)

        # ---------------------------------------------------------
        # Step 1: Login
        # ---------------------------------------------------------
        login_page.open()
        login_page.login()
        loader.load()

        # ---------------------------------------------------------
        # Step 2: Apply filter and open record
        # ---------------------------------------------------------
        open_filter.filter()
        filter_record.search("Record ID", "CM1765375700109QA")
        filter_action.searchFilter()
        loader.load()

        record_manager.view_record()
        loader.load()

        # ---------------------------------------------------------
        # Step 3: Switch between valid tabs
        # ---------------------------------------------------------
        assert record_tabs.switch_tabs("ai_insights"), "Failed to switch to AI Insights"
        assert record_tabs.switch_tabs("comments"), "Failed to switch to Comments"
        assert record_tabs.switch_tabs("ratings"), "Failed to switch to Ratings"

        # ---------------------------------------------------------
        # Step 4: Open home tab based on channel (call/chat/email/video)
        # ---------------------------------------------------------
        assert record_tabs.open_home_tab(), "Failed to open HOME tab"

        # ---------------------------------------------------------
        # Step 5: Logout
        # ---------------------------------------------------------
        logout_page.logout()
        loader.load()

    def test_home_tab_dynamic(self, driver_function):
        """
        Open a record, switch to another tab, then move back to HOME tab dynamically
        based on detected channel and verify correctness.
        """
        record_tabs = RecordPageTabs(driver_function)
        loader = Loader(driver_function)
        login_page = LoginPage(driver_function)
        logout_page = Logout(driver_function)
        filter_record = FilterByAttribute(driver_function)
        open_filter = FilterSearch(driver_function)
        filter_action = SubmitFilterSearch(driver_function)
        record_manager = RecordManager(driver_function)

        # -------------------- Login and open record --------------------
        login_page.open()
        login_page.login()
        loader.load()

        open_filter.filter()
        filter_record.search("Record ID", "CM1765375700109QA")
        filter_action.searchFilter()
        loader.load()

        record_manager.view_record()
        loader.load()

        # -------------------- Detect current channel --------------------
        channel = record_tabs.find_channel()
        assert channel in record_tabs.RecordPageTabHandler.CHANNEL_TABS, f"Unknown channel: {channel}"

        allowed_tabs = record_tabs.RecordPageTabHandler.CHANNEL_TABS[channel]

        # -------------------- Switch to a different tab if exists --------------------
        # Exclude the home tab itself
        home_tab_name = record_tabs.RecordPageTabHandler.HOME_TAB_MAP[channel]
        other_tabs = [t for t in allowed_tabs if t != home_tab_name]

        if other_tabs:
            tab_to_switch = other_tabs[0]
            switched = record_tabs.switch_tabs(tab_to_switch)
            assert switched, f"Failed to switch to tab: {tab_to_switch}"

        # -------------------- Move back to HOME tab --------------------
        home_opened = record_tabs.open_home_tab()
        assert home_opened, f"Failed to open HOME tab '{home_tab_name}' for channel '{channel}'"

        # Optional: verify current tab is the expected HOME tab
        current_tab_locator = record_tabs.RecordPageTabHandler.TAB_MAP[home_tab_name]
        assert record_tabs.is_element_present(current_tab_locator), \
            f"HOME tab element '{home_tab_name}' is not present on the UI"

        # -------------------- Logout --------------------
        logout_page.logout()
        loader.load()

    def test_tab_click_failures(self, driver_function):
        """
        Simulate click failure scenario (JS fallback) and element not present
        """
        record_tabs = RecordPageTabs(driver_function)
        loader = Loader(driver_function)
        login_page = LoginPage(driver_function)
        logout_page = Logout(driver_function)
        filter_record = FilterByAttribute(driver_function)
        open_filter = FilterSearch(driver_function)
        filter_action = SubmitFilterSearch(driver_function)
        record_tabs = RecordPageTabs(driver_function)
        record_manager = RecordManager(driver_function)

        login_page.open()
        login_page.login()
        loader.load()

        # ---------------------------------------------------------
        open_filter.filter()
        filter_record.search("Record ID", "CM1765375700109QA")
        filter_action.searchFilter()
        loader.load()

        record_manager.view_record()
        loader.load()

        # Force a non-existent tab to simulate failure
        result = record_tabs.switch_tabs("non_existing_tab")
        assert not result, "Switching non-existing tab should fail gracefully"

        logout_page.logout()
        loader.load()

    def test_video_media_tab(self, driver_function):
        """
        Validate Media tab behavior for Video channel
        """
        record_tabs = RecordPageTabs(driver_function)
        loader = Loader(driver_function)
        login_page = LoginPage(driver_function)
        logout_page = Logout(driver_function)
        filter_record = FilterByAttribute(driver_function)
        open_filter = FilterSearch(driver_function)
        filter_action = SubmitFilterSearch(driver_function)
        record_manager = RecordManager(driver_function)

        # -------------------- Login and open video record --------------------
        login_page.open()
        login_page.login()
        loader.load()

        open_filter.filter()
        filter_record.search("Record ID", "101020800")  # Use a valid video record ID
        filter_action.searchFilter()
        loader.load()

        record_manager.view_record()
        loader.load()

        # -------------------- Detect channel --------------------
        channel = record_tabs.find_channel()
        assert channel == "video", f"Expected video channel but found '{channel}'"

        # -------------------- Media Tab --------------------
        media_tab_locator = record_tabs.RecordPageTabHandler.TAB_MAP["media"]
        assert record_tabs.is_element_present(media_tab_locator), "Media tab is not present for video channel"

        switched = record_tabs.switch_tabs("media")
        assert switched, "Failed to switch to Media tab"

        # Optional: verify loader has disappeared / page stabilized
        loader.load()

        # -------------------- Logout --------------------
        logout_page.logout()
        loader.load()

    def test_call_transcript_tab(self, driver_function):
        """
        Validate Transcript tab behavior for Call channel using open_home_tab()
        specifically handling disabled Transcript tab.
        """
        record_tabs = RecordPageTabs(driver_function)
        loader = Loader(driver_function)
        login_page = LoginPage(driver_function)
        logout_page = Logout(driver_function)
        filter_record = FilterByAttribute(driver_function)
        open_filter = FilterSearch(driver_function)
        filter_action = SubmitFilterSearch(driver_function)
        record_manager = RecordManager(driver_function)

        # -------------------- Login and open call record --------------------
        login_page.open()
        login_page.login()
        loader.load()

        open_filter.filter()
        filter_record.search("Record ID", "AM1765375699855QA")  # Valid call record ID
        filter_action.searchFilter()
        loader.load()

        record_manager.view_record()
        loader.load()

        # -------------------- Detect channel --------------------
        channel = record_tabs.find_channel()
        assert channel == "call", f"Expected call channel but found '{channel}'"

        # -------------------- Switch to another tab first (optional) --------------------
        allowed_tabs = record_tabs.RecordPageTabHandler.CHANNEL_TABS[channel]
        home_tab_name = record_tabs.RecordPageTabHandler.HOME_TAB_MAP[channel]
        other_tabs = [t for t in allowed_tabs if t != home_tab_name]
        if other_tabs:
            record_tabs.switch_tabs(other_tabs[0])
            loader.load()


        home_opened = record_tabs.open_home_tab()
        assert home_opened, "Failed to open HOME tab (Transcript) for call channel"



        # -------------------- Logout --------------------
        logout_page.logout()
        loader.load()

