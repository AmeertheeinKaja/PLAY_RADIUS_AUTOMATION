import time

import pytest

from flow.filter_flow import FilterFlow
from pages.login.login import LoginPage
from pages.common.loader import Loader
from pages.common.open_filter_search import FilterSearch
from pages.process.process_manager.process_filter import ProcessFilter

from pages.common.sidemenupage import SideMenuPage
from pages.process.process_manager.search_process import OpenProcess

from pages.process.version.version_chat_config import VersionChatConfig
from pages.process.category.version_process_config import VersionProcessConfig

from pages.login.logout import Logout

from utils.logger import get_logger
from utils.data_reader import load_test_data
from utils.counter_manager import get_next_process_number


logger = get_logger(__name__)
version_data = load_test_data("process/version/versionData.json")
question_data = load_test_data("process/category/questionData.json")


@pytest.mark.usefixtures("driver_function")
class TestCallVersion:

    # -------------------------------------------------------------------------
    # 🔧 COMMON SETUP HELPERS (Best Practice)
    # -------------------------------------------------------------------------
    def setup_common(self, driver):
        """Reusable setup for all tests."""
        self.login = LoginPage(driver)
        self.loader = Loader(driver)
        self.logout = Logout(driver)
        self.side_menu = SideMenuPage(driver)
        self.open_filter = FilterSearch(driver)
        self.process = OpenProcess(driver)
        self.version = VersionChatConfig(driver)
        self.process_filter_page = ProcessFilter(driver)

        self.login.open()
        self.login.login()
        self.loader.load()

        self.side_menu.process()
        self.open_filter.filter()

        test_data = load_test_data("process/filter_process.json")
        process_name = test_data["processName"]

        self.process_filter_page.apply_filter_by_name(process_name)
        self.process.view_process()
        self.version.open_chat_version_section()

    def test_add_chat_version_category(self, driver_function):
        self.setup_common(driver_function)

        categories = question_data["categories"]
        name_value = version_data["new"]["name"]

        vp = VersionProcessConfig(
            driver_function,
            categories=categories,
            version_name=name_value
        )

        modal = self.version.open_add_version_modal()
        modal.fill(version_data["new"])

        modal.submit()
        modal.wait_for_modal_close()

        modal.open_version()

        vp.add_all_categories()
        vp.publish_version()

        self.logout.logout()




