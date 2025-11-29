import pytest

from pages.common.open_filter_search import FilterSearch
from pages.common.submit_search_filter import SubmitFilterSearch
from utils.data_reader import load_test_data

from pages.login.login import LoginPage
from pages.common.loader import Loader
from pages.filtering.filter_record_by_attribute import FilterByAttribute
from utils.screenshot import Screenshot
from pages.login.logout import Logout
from flow.filter_flow import FilterFlow
from utils.logger import get_logger

logger = get_logger(__name__)




@pytest.mark.usefixtures("driver_function")
class TestAttributeFilter:

    def test_filter(self, driver_function):
        login_page = LoginPage(driver_function)
        loader = Loader(driver_function)
        logout = Logout(driver_function)

        login_page.open()
        login_page.login()
        loader.load()


        filter_flow = FilterFlow(driver_function)

        # 🌟 One single call
        filter_flow.apply_filters()

        # Optional validation call
        filter_flow.validate_after_search()

        logout.logout()

    def test_missing_filters_enable(self, driver_function):
        login = LoginPage(driver_function)
        loader = Loader(driver_function)
        logout = Logout(driver_function)

        login.open()
        login.login()
        loader.load()

        flow = FilterFlow(driver_function)

        enabled = flow.filter_attribute.enable_missing()
        assert enabled is True, "Missing filters were NOT enabled."

        logout.logout()

    def test_filtered_results_match(self, driver_function):
        login = LoginPage(driver_function)
        loader = Loader(driver_function)
        logout = Logout(driver_function)

        login.open()
        login.login()
        loader.load()

        flow = FilterFlow(driver_function)
        flow.apply_filters()

        assert flow.is_result_matching() is True, "Filtered results not matching expected data."

        logout.logout()

    def test_clear_filter_resets_results(self, driver_function):
        login = LoginPage(driver_function)
        loader = Loader(driver_function)
        logout = Logout(driver_function)

        login.open()
        login.login()
        loader.load()

        flow = FilterFlow(driver_function)

        flow.apply_filters()
        flow.action_filter.clearFilter()

        # After clearing, row count should be back to default
        rows = flow.result_page.get_row_count()
        assert rows > 1, "Clear filter didn’t reset the list."

        logout.logout()

    def test_filter_panel_opens(self, driver_function):
        login = LoginPage(driver_function)
        loader = Loader(driver_function)
        logout = Logout(driver_function)

        login.open()
        login.login()
        loader.load()

        flow = FilterFlow(driver_function)

        opened = flow.filter_search.filter()
        assert opened is True, "Filter panel did not open."

        logout.logout()

    invalid_filters = [
        ("Interaction ID", "be76a2973345428b8fea29f5422eceeaaskkjhkj"),
        ("Dialed ID", "111132297"),
        ("Caller ID", "22399"),
        ("Process Code", "CODE_AUGUST_0437"),
    ]

    @pytest.mark.parametrize("field,value", invalid_filters)
    def test_filter_with_invalid_values(self, driver_function, field, value):
        login = LoginPage(driver_function)
        loader = Loader(driver_function)
        logout = Logout(driver_function)

        login.open()
        login.login()
        loader.load()

        flow = FilterFlow(driver_function)

        # open panel
        flow.filter_search.filter()

        # ensure THIS specific filter is enabled
        flow.filter_attribute.ensure_filter_enabled(field)

        # reopen panel again after enabling
        flow.filter_search.filter()

        # apply filter
        flow.filter_attribute.search(field, value)
        flow.action_filter.searchFilter()

        assert flow.result_page.is_no_data() is True, f"{field} with invalid value returned results!"

        logout.logout()

    def test_multiple_filters_applied_together(self, driver_function):
        login = LoginPage(driver_function)
        loader = Loader(driver_function)
        logout = Logout(driver_function)

        login.open()
        login.login()
        loader.load()

        flow = FilterFlow(driver_function)

        filters_to_apply = {
            "Process Code": "RADIUS_OIS",
            "Interaction Type": "ib"
        }

        flow.apply_multiple_filters(filters_to_apply)

        assert flow.is_result_matching() is True, "Results do not match all filter criteria!"

        logout.logout()

    def test_clear_already_cleared_filter(self, driver_function):
        login = LoginPage(driver_function)
        loader = Loader(driver_function)
        logout = Logout(driver_function)

        login.open()
        login.login()
        loader.load()

        flow = FilterFlow(driver_function)

        logger.info("Clearing already cleared filter")
        flow.action_filter.clearFilter()
        flow.action_filter.clearFilter()  # call again
        rows = flow.result_page.get_row_count()
        assert rows > 1, "Clearing an already cleared filter broke the table"
        logger.info("Clear already cleared filter works correctly")

        logout.logout()


