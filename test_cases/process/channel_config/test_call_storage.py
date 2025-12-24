import pytest

from pages.login.login import LoginPage
from pages.common.loader import Loader

from pages.process.process_manager.create_process import CreateProcess  # Assuming this class exists
from pages.common.sidemenupage import SideMenuPage

from pages.process.channel_config.call.call_storage_config import CallStorageConfig

from pages.login.logout import Logout

from utils.logger import get_logger
from utils.data_reader import load_test_data
logger = get_logger(__name__)


@pytest.mark.usefixtures("driver_function")
class TestCallConfigSA:
    def test_call_config_sa(self, driver_function):
        config = load_test_data("process/create_process.json")
        call_config = config["channel_config"]["call"]["storage"]


        driver = driver_function

        login = LoginPage(driver)
        loader = Loader(driver)
        logout = Logout(driver)
        side_menu = SideMenuPage(driver)
        create_process = CreateProcess(driver)

        call_storage = CallStorageConfig(
            driver
        )

        logger.info("Opening login page...")
        login.open()
        logger.info("Login page opened.")

        login.login()
        loader.load()

        side_menu.process()
        loader.load()

        create_process.create_process()
        loader.load()

        call_storage.storage_config(call_config)

        logout.logout()

