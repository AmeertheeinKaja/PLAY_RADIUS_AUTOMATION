import pytest
from selenium.webdriver.common.by import By

from pages.login.login import LoginPage
from pages.common.loader import Loader
from pages.process.process_manager.create_process import CreateProcess
from pages.process.process_manager.process_filter import ProcessFilter
from pages.common.sidemenupage import SideMenuPage
from pages.common.open_filter_search import FilterSearch
from pages.process.process_manager.search_process import OpenProcess
from pages.process.channel_config.call.call_stt_config import CallSTTConfig
from pages.process.channel_config.call.call_sa_config import CallSAConfig
from pages.process.process_manager.create_process import CreateProcess
from pages.process.channel_config.call.call_storage_config import CallStorageConfig

from pages.login.logout import Logout
from utils.screenshot import Screenshot
from utils.logger import get_logger
from utils.data_reader import load_test_data

logger = get_logger(__name__)


@pytest.mark.usefixtures("driver_function")
class TestCallConfigSTT:

    # =========================================================
    # MAIN POSITIVE FLOW
    # =========================================================

    def test_call_config_stt(self, driver_function):
        """
        Full STT configuration test (happy path)


        """

        full_cfg = load_test_data("process/create_process.json")
        stt_cfg = full_cfg["channel_config"]["call"]["stt"]

        driver = driver_function
        logout = None

        try:
            login = LoginPage(driver)
            loader = Loader(driver)
            side_menu = SideMenuPage(driver)
            filter_search = FilterSearch(driver)
            process_filter = ProcessFilter(driver)
            open_Process =OpenProcess(driver)


            stt_config = CallSTTConfig(
                driver, speech_to_text=stt_cfg.get("speech_to_text"),
                sample_rate=stt_cfg.get("sample_rate"),
                engine_name=stt_cfg.get("engine_name"),
                bucket_name=stt_cfg.get("bucket_name"),
                bucket_dir=stt_cfg.get("bucket_dir"),
                keyFile=stt_cfg.get("keyFile"),
                audioFile=stt_cfg.get("audioFile"),
                conversion_mode=stt_cfg.get("conversion_mode")

            )
            logout = Logout(driver)

            login.open()
            login.login()
            loader.load()

            side_menu.process()
            filter_search.filter()
            process_filter.apply_filter_by_name("SMK_PLAY_24OCT_A")
            open_Process.view_process()
            loader.load()
            stt_config.reconfigure_stt()
            logout.logout()



        except Exception as e:
            Screenshot.take(driver, "test_call_config_stt_failure")
            logger.error("STT configuration failed", exc_info=True)
            raise

        finally:
            if logout:
                try:
                    logout.logout()
                except:
                    pass

    def test_call_config_sa(self, driver_function):
        """
        Full STT configuration test (happy path)


        """

        full_cfg = load_test_data("process/create_process.json")
        stt_cfg = full_cfg["channel_config"]["call"]["sa"]

        driver = driver_function
        logout = None

        try:
            login = LoginPage(driver)
            loader = Loader(driver)
            side_menu = SideMenuPage(driver)
            create_process=CreateProcess(driver)
            filter_search = FilterSearch(driver)
            process_filter = ProcessFilter(driver)
            open_Process =OpenProcess(driver)


            sa_config = CallSAConfig(
                driver, sentiment_analysis=stt_cfg.get("sentiment_analysis"),

                engine_name=stt_cfg.get("engine_name"),

                keyFile=stt_cfg.get("keyFile"),
                sentiment_text=stt_cfg.get("sentiment_text"),
                conversion_mode=stt_cfg.get("conversion_mode")

            )
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
            sa_config.reconfig_sa()
            logout.logout()



        except Exception as e:
            Screenshot.take(driver, "test_call_config_stt_failure")
            logger.error("STT configuration failed", exc_info=True)
            raise

        finally:
            if logout:
                try:
                    logout.logout()
                except:
                    pass

    def test_call_storage(self, driver_function):
        """
        Full STT configuration test (happy path)


        """

        full_cfg = load_test_data("process/create_process.json")
        storage_cfg = full_cfg["channel_config"]["call"]["storage"]

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
            storage_cfg= CallStorageConfig(driver)


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
            storage_json = full_cfg["channel_config"]["call"]["storage"]
            storage_page = CallStorageConfig(driver)

            storage_page.edit_storage_config(storage_json)
            logout.logout()



        except Exception as e:
            Screenshot.take(driver, "test_call_config_stt_failure")
            logger.error("STT configuration failed", exc_info=True)
            raise

        finally:
            if logout:
                try:
                    logout.logout()
                except:
                    pass