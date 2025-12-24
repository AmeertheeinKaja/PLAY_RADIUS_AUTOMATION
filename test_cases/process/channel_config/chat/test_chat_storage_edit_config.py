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
from pages.process.channel_config.chat.chat_storage_config import ChatStorageConfig

from pages.login.logout import Logout
from utils.screenshot import Screenshot
from utils.logger import get_logger
from utils.data_reader import load_test_data

logger = get_logger(__name__)


@pytest.mark.usefixtures("driver_function")
class TestChatEditConfigStorage:


    def test_chat_edit_storage(self, driver_function):


        full_cfg = load_test_data("process/create_process.json")


        driver = driver_function
        logout = None

        try:
            login = LoginPage(driver)
            loader = Loader(driver)
            side_menu = SideMenuPage(driver)
            create_process = CreateProcess(driver)
            filter_search = FilterSearch(driver)
            process_filter = ProcessFilter(driver)
            open_Process = OpenProcess(driver)
            storage_cfg= ChatStorageConfig(driver)
            logout = Logout(driver)




            login.open()
            login.login()
            loader.load()



            side_menu.process()
            # create_process.create_process()
            filter_search.filter()
            process_filter.apply_filter_by_name("SMK_PLAY_24OCT_A")
            open_Process.view_process()
            loader.load()
            storage_json = full_cfg["channel_config"]["chat"]["storage"]

            storage_cfg.set_storage_type("ftp")
            storage_cfg.edit_storage_config(storage_json)
            logout.logout()



        except Exception as e:
            Screenshot.take(driver, "test_chat_config_storage_failure")
            logger.error("Storage configuration failed", exc_info=True)
            raise

        finally:
            if logout:
                try:
                    logout.logout()
                except:
                    pass

    def test_sftp_missing_fields(self, driver_function):
        driver = driver_function
        login = LoginPage(driver)
        logout = Logout(driver)
        loader = Loader(driver)

        side_menu = SideMenuPage(driver)
        filter_search = FilterSearch(driver)
        process_filter = ProcessFilter(driver)
        open_process = OpenProcess(driver)
        storage_cfg = ChatStorageConfig(driver)

        login.open()
        login.login()
        loader.load()

        side_menu.process()
        filter_search.filter()
        process_filter.apply_filter_by_name("SMK_PLAY_24OCT_A")
        open_process.view_process()
        loader.load()

        # Set storage type manually
        storage_cfg.set_storage_type("sftp")

        # Set intentionally wrong/empty fields
        invalid_data = {
            "sftp": {
                "hostName": "",
                "port": "",
                "username": "",
                "password": "",
                "dirPath": ""
            }
        }

        storage_cfg.edit_storage_config(invalid_data)

        # Assertions
        assert storage_cfg.get_error_message(storage_cfg.INVALID_HOST_PATH) == "This field is required"
        assert storage_cfg.get_error_message(storage_cfg.INVALID_PORT_PATH) == "This field is required"
        assert storage_cfg.get_error_message(storage_cfg.INVALID_USER_PATH) == "This field is required"
        assert storage_cfg.get_error_message(storage_cfg.INVALID_PASSWORD_PATH) == "This field is required"

        logout.logout()

    def test_ftp_missing_fields(self, driver_function):
        driver = driver_function
        login = LoginPage(driver)
        logout = Logout(driver)
        loader = Loader(driver)

        side_menu = SideMenuPage(driver)
        filter_search = FilterSearch(driver)
        process_filter = ProcessFilter(driver)
        open_process = OpenProcess(driver)
        storage_cfg = ChatStorageConfig(driver)

        login.open()
        login.login()
        loader.load()

        side_menu.process()
        filter_search.filter()
        process_filter.apply_filter_by_name("SMK_PLAY_24OCT_A")
        open_process.view_process()
        loader.load()

        # Set storage type manually
        storage_cfg.set_storage_type("ftp")

        # Set intentionally wrong/empty fields
        invalid_data = {
            "sftp": {
                "hostName": "",
                "port": "",
                "username": "",
                "password": "",
                "dirPath": ""
            }
        }

        storage_cfg.edit_storage_config(invalid_data)

        # Assertions
        assert storage_cfg.get_error_message(storage_cfg.INVALID_HOST_PATH) == "This field is required"
        assert storage_cfg.get_error_message(storage_cfg.INVALID_PORT_PATH) == "This field is required"
        assert storage_cfg.get_error_message(storage_cfg.INVALID_USER_PATH) == "This field is required"
        assert storage_cfg.get_error_message(storage_cfg.INVALID_PASSWORD_PATH) == "This field is required"

        logout.logout()

