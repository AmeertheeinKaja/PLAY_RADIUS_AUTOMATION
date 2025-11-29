import pytest

from pages.login.login import LoginPage
from pages.common.loader import Loader
from pages.common.open_filter_search import FilterSearch
from pages.filtering.filter_record_by_attribute import FilterByAttribute
from pages.common.submit_search_filter import SubmitFilterSearch
from pages.login.logout import Logout
from utils.screenshot import Screenshot
from utils.data_reader import load_test_data
# data=load_test_data("filter/DataFilterAttributes.json")
# filter_data=data["active"]



@pytest.mark.usefixtures("driver_function")
class TestFilterAttributes:

    def test_filter(self, driver_function):
        """
        Verify that:
        1. User can login
        2. Filter panel opens
        3. Missing filters get enabled
        4. Filters are applied successfully
        """

        login_page = LoginPage(driver_function)
        loader = Loader(driver_function)
        filter_search = FilterSearch(driver_function)
        filter_attribute = FilterByAttribute(driver_function)
        action_filter = SubmitFilterSearch(driver_function)
        logout = Logout(driver_function)

        try:
            # STEP 1: LOGIN
            login_page.open()
            login_page.login()
            loader.load()

            # STEP 2: OPEN FILTER PANEL
            filter_search.filter()

            # STEP 3: ENABLE missing filters
            enabled = filter_attribute.enable_missing()
            assert enabled is True, "Missing filters were not enabled successfully."

            # STEP 4: APPLY FILTER VALUES

            filter_attribute.filter()

            # STEP 5: SUBMIT FILTER
            action_filter.searchFilter()

            # STEP 6: REOPEN FILTER PANEL TO VALIDATE RESULTS
            filter_search.filter()
            action_filter.searchFilter()

            # If needed, add expected results validations here

            # STEP 7: LOGOUT
            logout.logout()

        except Exception:
            Screenshot.take(driver_function, "filter_attribute_test_failed")
            raise
