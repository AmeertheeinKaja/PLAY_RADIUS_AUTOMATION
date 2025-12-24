import pytest
from selenium.webdriver.common.by import By

from pages.login.login import LoginPage
from pages.common.loader import Loader
from pages.process.process_manager.create_process import CreateProcess
from pages.process.process_manager.process_filter import ProcessFilter
from pages.common.sidemenupage import SideMenuPage
from pages.common.open_filter_search import FilterSearch
from pages.process.process_manager.search_process import OpenProcess
from pages.process.contact_schema.upload_record_page import UploadRecord

from pages.process.process_manager.create_process import CreateProcess


from pages.login.logout import Logout
from utils.download_manager import clear_downloads_folder
from utils.screenshot import Screenshot
from utils.logger import get_logger
from utils.data_reader import load_test_data

logger = get_logger(__name__)


@pytest.mark.usefixtures("driver_function")
class TestUploadRecord:

    def test_upload_record(self, driver_function):


        driver = driver_function
        record_path = load_test_data("process/contact_schema/record_data.json")


        logout = None

        try:
            login = LoginPage(driver)
            loader = Loader(driver)
            side_menu = SideMenuPage(driver)
            # create_process = CreateProcess(driver)
            filter_search = FilterSearch(driver)
            process_filter = ProcessFilter(driver)
            open_Process = OpenProcess(driver)
            upload_record = UploadRecord(driver)


            logout = Logout(driver)

            login.open()
            login.login()
            loader.load()

            side_menu.process()
            filter_search.filter()
            process_filter.apply_filter_by_name("SMK_PLAY_OCT28_A")
            open_Process.view_process()
            loader.load()
            clear_downloads_folder()


            upload_record.upload_process(record_path)
            loader.load()

            logout.logout()



        except Exception as e:
            Screenshot.take(driver, "test_upload_record")
            logger.error(" upload_record failed", exc_info=True)
            raise

        finally:
            if logout:
                try:
                    logout.logout()
                except:
                    pass
