import pytest

from flow.filter_flow import FilterFlow
from pages.login.login import LoginPage
from pages.common.loader import Loader
from pages.common.open_filter_search import FilterSearch
from pages.process.process_manager.process_filter import ProcessFilter
from pages.process.process_manager.create_process import CreateProcess# Assuming this class exists
from pages.common.sidemenupage import SideMenuPage
from pages.process.process_manager.search_process import OpenProcess
from pages.process.channel_config.call.call_stt_config import CallSTTConfig
from pages.common.submit_search_filter import SubmitFilterSearch

from pages.login.logout import Logout
from utils.screenshot import Screenshot
from utils.logger import get_logger
from utils.data_reader import load_test_data# Assuming this utility exists

# ... existing imports ...

logger = get_logger(__name__)


@pytest.mark.usefixtures("driver_function")
class TestProcessFilter:
    def test_filter_process_by_name(self, driver_function):
        login = LoginPage(driver_function)
        loader = Loader(driver_function)
        logout = Logout(driver_function)
        side_menu = SideMenuPage(driver_function)
        open_filter = FilterSearch(driver_function)
        open_process = OpenProcess(driver_function)
        create_process = CreateProcess(driver_function)
        call_stt = CallSTTConfig(driver_function)

        process_filter_page = ProcessFilter(driver_function)

        logger.info("Starting test_filter_process_by_name")

        logger.info("Opening login page...")
        login.open()
        logger.info("Login page opened.")

        logger.info("Attempting login...")
        login.login()
        logger.info("Login complete.")

        logger.info("Waiting for page to load after login...")
        loader.load()
        logger.info("Page loaded.")

        logger.info("Navigating to Process section via Side Menu...")
        side_menu.process()  # Assuming this navigates to the process list page
        logger.info("Navigated to Process section.")




        create_process.create_process()
        call_stt.configure_stt()




        # logger.info("Submitting filter search...")
        # submit_filter = SubmitFilterSearch(driver_function)
        # submit_filter.searchFilter()
        # logger.info("Filter search submitted.")

        # Add assertions here to verify the filtering


        logger.info("Logging out...")
        logout.logout()
        logger.info("Logout complete. Test finished.")