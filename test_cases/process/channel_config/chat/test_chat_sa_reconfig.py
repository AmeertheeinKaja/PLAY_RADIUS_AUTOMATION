import pytest
from selenium.webdriver.common.by import By

from pages.login.login import LoginPage
from pages.common.loader import Loader
from pages.process.process_manager.create_process import CreateProcess
from pages.process.process_manager.process_filter import ProcessFilter
from pages.common.sidemenupage import SideMenuPage
from pages.common.open_filter_search import FilterSearch
from pages.process.process_manager.search_process import OpenProcess

from pages.process.channel_config.chat.chat_sa_config import ChatSAConfig

from pages.process.process_manager.create_process import CreateProcess


from pages.login.logout import Logout
from utils.screenshot import Screenshot
from utils.logger import get_logger
from utils.data_reader import load_test_data

logger = get_logger(__name__)


@pytest.mark.usefixtures("driver_function")
class TestChatSA:

    def test_chat_config_sa(self, driver_function):
        """
        Full STT configuration test (happy path)


        """

        full_cfg = load_test_data("process/create_process.json")
        sa_cfg = full_cfg["channel_config"]["chat"]["sa"]

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


            sa_config = ChatSAConfig(
                driver, sentiment_analysis=sa_cfg.get("sentiment_analysis"),

                engine_name=sa_cfg.get("engine_name"),

                keyFile=sa_cfg.get("keyFile"),
                sentiment_text=sa_cfg.get("sentiment_text"),
                conversion_mode=sa_cfg.get("conversion_mode")

            )
            logout = Logout(driver)

            login.open()
            login.login()
            loader.load()

            side_menu.process()
            # create_process.create_process()
            filter_search.filter()
            process_filter.apply_filter_by_name("SINGLKE_Q_INBPOUND")
            open_Process.view_process()
            loader.load()
            sa_config.reconfig_sa()
            # edit_chat_sa_config.edit_chat_sa()

            logout.logout()



        except Exception as e:
            Screenshot.take(driver, "test_chat_config_sa_failure")
            logger.error("SA configuration failed", exc_info=True)
            raise

        finally:
            if logout:
                try:
                    logout.logout()
                except:
                    pass
