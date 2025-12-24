import pytest
from selenium.webdriver.common.by import By

from pages.login.login import LoginPage
from pages.common.loader import Loader
from pages.process.process_manager.create_process import CreateProcess
from pages.process.process_manager.process_filter import ProcessFilter
from pages.common.sidemenupage import SideMenuPage
from pages.common.open_filter_search import FilterSearch
from pages.process.process_manager.search_process import OpenProcess

from pages.process.channel_config.email.email_sa_config import EmailSAConfig
from pages.process.process_manager.create_process import CreateProcess


from pages.login.logout import Logout
from utils.process_factory import create_process_from_json
from utils.screenshot import Screenshot
from utils.logger import get_logger
from utils.data_reader import load_test_data

logger = get_logger(__name__)


@pytest.mark.usefixtures("driver_function")
class TestChatSAConfig:

    def test_chat_config_sa(self, driver_function):
        """
        Full STT configuration test (happy path)


        """

        full_cfg = load_test_data("process/create_process.json")
        stt_cfg = full_cfg["channel_config"]["email"]["sa"]

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

            sa_config = EmailSAConfig(
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
            create_process = create_process_from_json(driver_function)
            create_process.create_process()
            # filter_search.filter()
            # process_filter.apply_filter_by_name("SMK_PLAY_24OCT_A")
            # open_Process.view_process()
            loader.load()
            sa_config.config_sa()
            logout.logout()



        except Exception as e:
            Screenshot.take(driver, "test_email_config_sa_failure")
            logger.error("SA configuration failed", exc_info=True)
            raise

        finally:
            if logout:
                try:
                    logout.logout()
                except:
                    pass
