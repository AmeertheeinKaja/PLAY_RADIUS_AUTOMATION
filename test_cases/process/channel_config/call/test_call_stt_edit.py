import pytest
from selenium.webdriver.common.by import By

from pages.common.open_filter_search import FilterSearch
from pages.login.login import LoginPage
from pages.common.loader import Loader
from pages.process.process_manager.create_process import CreateProcess
from pages.common.sidemenupage import SideMenuPage
from pages.process.channel_config.call.call_stt_config import CallSTTConfig
from pages.login.logout import Logout
from pages.process.process_manager.process_filter import ProcessFilter
from pages.process.process_manager.search_process import OpenProcess
from utils.screenshot import Screenshot
from utils.logger import get_logger
from utils.data_reader import load_test_data

logger = get_logger(__name__)


@pytest.mark.usefixtures("driver_function")
class TestCallReconfigSTT:

    # =========================================================
    # MAIN POSITIVE FLOW
    # =========================================================

    def test_call_config_stt(self, driver_function):
        driver = driver_function
        logout = None

        try:
            data = load_test_data("process/create_process.json")
            stt_data = data["channel_config"]["call"]["stt"]

            login = LoginPage(driver)
            loader = Loader(driver)
            side_menu = SideMenuPage(driver)
            create_process = CreateProcess(driver)
            filter_search = FilterSearch(driver)
            process_filter = ProcessFilter(driver)
            open_Process = OpenProcess(driver)

            stt_config = CallSTTConfig(
                driver,
                speech_to_text=stt_data["speech_to_text"],
                bucket_name=stt_data["bucket_name"],
                bucket_dir=stt_data["bucket_dir"],
                sample_rate=stt_data["sample_rate"],
                engine_name=stt_data["engine_name"],
                keyFile=stt_data["keyFile"],
                audioFile=stt_data["audioFile"],
                conversion_mode=stt_data["conversion_mode"]
            )

            logout = Logout(driver)

            login.open()
            login.login()
            loader.load()

            side_menu.process()
            filter_search.filter()
            process_filter.apply_filter_by_name("SINGLKE_Q_INBPOUND")
            open_Process.view_process()
            loader.load()


            stt_config.reconfigure_stt()

            assert stt_config.last_toast == stt_config.MSG_TEST_SUCCESS

        except Exception:
            Screenshot.take(driver, "test_call_config_stt_failure")
            raise

        finally:
            if logout:
                logout.logout()
