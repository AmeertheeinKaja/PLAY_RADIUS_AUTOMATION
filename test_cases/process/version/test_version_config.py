import pytest

from flow.filter_flow import FilterFlow
from pages.login.login import LoginPage
from pages.common.loader import Loader
from pages.common.open_filter_search import FilterSearch
from pages.process.process_manager.process_filter import ProcessFilter

from pages.common.sidemenupage import SideMenuPage
from pages.process.process_manager.search_process import OpenProcess

from pages.process.version.version_config import VersionConfig

from pages.login.logout import Logout
from utils.screenshot import Screenshot
from utils.logger import get_logger
from utils.data_reader import load_test_data
from utils.counter_manager import get_next_process_number

logger = get_logger(__name__)

data = load_test_data("process/version/versionData.json")
@pytest.mark.usefixtures("driver_function")
class TestConfigVersion:

    def test_video_import_version(self, driver_function):
        login = LoginPage(driver_function)
        loader = Loader(driver_function)
        logout = Logout(driver_function)
        side_menu = SideMenuPage(driver_function)
        open_filter = FilterSearch(driver_function)
        process = OpenProcess(driver_function)
        version = VersionConfig(driver_function)

        process_filter_page = ProcessFilter(driver_function)

        logger.info("Starting test_import_version")

        login.open()
        login.login()
        loader.load()

        side_menu.process()
        open_filter.filter()

        test_data = load_test_data("process/filter_process.json")
        process_name = test_data["processName"]

        process_filter_page.apply_filter_by_name(process_name)

        process.view_process()
        version.perform("call","add",data["new"])







        logout.logout()
        logger.info("Logout complete. Test finished.")

        logout.logout()
        logger.info("Logout complete. Test finished.")
