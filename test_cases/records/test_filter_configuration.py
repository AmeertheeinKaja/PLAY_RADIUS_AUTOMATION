import pytest

from flow.filter_flow import FilterFlow
from pages.login.login import LoginPage
from pages.common.loader import Loader
from pages.common.open_filter_search import FilterSearch
from pages.filtering.filter_record_by_attribute import FilterByAttribute
from pages.common.submit_search_filter import SubmitFilterSearch
from pages.login.logout import Logout
from utils.screenshot import Screenshot
from utils.logger import get_logger

logger = get_logger(__name__)


@pytest.mark.usefixtures("driver_function")
class TestFilterConfiguration:
    def test_clear_already_cleared_filter(self, driver_function):
        login = LoginPage(driver_function)
        loader = Loader(driver_function)
        logout = Logout(driver_function)

        login.open()
        login.login()
        loader.load()

        flow = FilterFlow(driver_function)
        flow.filter_search.filter()

        missing = flow.filter_attribute.enable_missing()
        flow.filter_search.filter()
        missing = flow.filter_attribute.enable_missing()


        # Test logic:
        assert  missing, f"Some active filters from JSON are missing in UI: {missing}"
        logout.logout()


