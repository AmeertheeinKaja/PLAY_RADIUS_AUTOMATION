import pytest

from flow.filter_flow import FilterFlow
from pages.login.login import LoginPage
from pages.common.loader import Loader
from pages.common.open_filter_search import FilterSearch
from pages.process.process_manager.process_filter import ProcessFilter
from pages.process.process_manager.create_process import CreateProcess  # Assuming this class exists
from pages.common.sidemenupage import SideMenuPage
from pages.process.process_manager.search_process import OpenProcess
from pages.process.channel_config.call.call_stt_config import CallSTTConfig
from pages.common.submit_search_filter import SubmitFilterSearch

from pages.login.logout import Logout
from utils.process_factory import create_process_from_json
from utils.screenshot import Screenshot
from utils.logger import get_logger
from utils.data_reader import load_test_data  # Assuming this utility exists

# ... existing imports ...

logger = get_logger(__name__)


@pytest.mark.usefixtures("driver_function")
class TestCreateProcess:
    def test_create_process(self, driver_function):
        login = LoginPage(driver_function)
        loader = Loader(driver_function)
        logout = Logout(driver_function)
        side_menu = SideMenuPage(driver_function)
        open_filter = FilterSearch(driver_function)
        open_process = OpenProcess(driver_function)
        create_process = CreateProcess(driver_function)

        process_filter_page = ProcessFilter(driver_function)
        login.open()
        login.login()
        loader.load()

        side_menu.process()
        create_process = create_process_from_json(driver_function)
        create_process.create_process()

        #




        logger.info("Logging out...")
        logout.logout()
        logger.info("Logout complete. Test finished.")