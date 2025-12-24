import pytest
from selenium.webdriver.common.by import By

from pages.login.login import LoginPage
from pages.common.loader import Loader
from pages.process.process_manager.create_process import CreateProcess
from pages.process.process_manager.process_filter import ProcessFilter
from pages.common.sidemenupage import SideMenuPage
from pages.common.open_filter_search import FilterSearch
from pages.process.process_manager.search_process import OpenProcess

from pages.process.process_manager.create_process import CreateProcess
from pages.process.channel_config.video.video_storage_config import VideoStorageConfig

from pages.login.logout import Logout
from utils.screenshot import Screenshot
from utils.logger import get_logger
from utils.data_reader import load_test_data

logger = get_logger(__name__)

@pytest.mark.usefixtures("driver_function")
class TestEmailEditConfigStorage:
    data=load_test_data("process/edit_process.json")
    @pytest.mark.parametrize("case", data.get('tests'))
    def test_chat_edit_storage(self, driver_function, case):

        driver = driver_function
        process_name = case["process_name"]
        storage_type = case["storage_type"]

        login = LoginPage(driver)
        loader = Loader(driver)
        side_menu = SideMenuPage(driver)
        filter_search = FilterSearch(driver)
        process_filter = ProcessFilter(driver)
        open_process = OpenProcess(driver)
        storage_cfg = VideoStorageConfig(driver)
        logout = Logout(driver)

        try:
            login.open()
            login.login()
            loader.load()

            side_menu.process()

            filter_search.filter()
            process_filter.apply_filter_by_name(process_name)
            open_process.view_process()
            loader.load()

            full_cfg = load_test_data("process/create_process.json")
            storage_json = full_cfg["channel_config"]["video"]["storage"]

            # Override storage type from test data
            storage_cfg.set_storage_type(storage_type)

            storage_cfg.edit_storage_config(storage_json)

            logout.logout()

        except Exception as e:
            Screenshot.take(driver, f"storage_edit_failure_{storage_type}")
            raise
