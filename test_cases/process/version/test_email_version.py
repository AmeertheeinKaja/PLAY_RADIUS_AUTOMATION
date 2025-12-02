import pytest

from flow.filter_flow import FilterFlow
from pages.login.login import LoginPage
from pages.common.loader import Loader
from pages.common.open_filter_search import FilterSearch
from pages.process.process_manager.process_filter import ProcessFilter

from pages.common.sidemenupage import SideMenuPage
from pages.process.process_manager.search_process import OpenProcess

from pages.process.version.version_email_config import VersionEmailConfig

from pages.login.logout import Logout
from utils.screenshot import Screenshot
from utils.logger import get_logger
from utils.data_reader import load_test_data
from utils.counter_manager import get_next_process_number

logger = get_logger(__name__)

data = load_test_data("process/version/versionData.json")
@pytest.mark.usefixtures("driver_function")
class TestEmailVersion:

    def test_email_import_version(self, driver_function):
        login = LoginPage(driver_function)
        loader = Loader(driver_function)
        logout = Logout(driver_function)
        side_menu = SideMenuPage(driver_function)
        open_filter = FilterSearch(driver_function)
        process = OpenProcess(driver_function)
        version = VersionEmailConfig(driver_function)

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

        version.open_email_version_section()
        modal = version.open_import_version_modal()

        modal.select_process("Campaign_ADD")
        modal.select_version("test3")
        modal.select_interaction("ib")
        modal.enter_version_name("Imported_"+ str(get_next_process_number()))

        modal.submit()
        modal.wait_for_modal_close()

        logout.logout()
        logger.info("Logout complete. Test finished.")


    def test_email_copy_version(self, driver_function):
        login = LoginPage(driver_function)
        loader = Loader(driver_function)
        logout = Logout(driver_function)
        side_menu = SideMenuPage(driver_function)
        open_filter = FilterSearch(driver_function)
        process = OpenProcess(driver_function)
        version = VersionEmailConfig(driver_function)

        process_filter_page = ProcessFilter(driver_function)

        logger.info("Starting test_copy_version")

        login.open()
        login.login()
        loader.load()

        side_menu.process()
        open_filter.filter()

        test_data = load_test_data("process/filter_process.json")
        process_name = test_data["processName"]

        process_filter_page.apply_filter_by_name(process_name)

        process.view_process()

        version.open_email_version_section()
        modal = version.open_copy_version_modal()

        modal.select_copy_version("Robot")
        modal.select_interaction("ib")
        modal.enter_copy_version_name("copy_version_"+ str(get_next_process_number()))

        modal.submit()
        modal.wait_for_modal_close()

        logout.logout()
        logger.info("Logout complete. Test finished.")

    def test_email_add_version_json(self, driver_function):
        login = LoginPage(driver_function)
        loader = Loader(driver_function)
        logout = Logout(driver_function)
        side_menu = SideMenuPage(driver_function)
        open_filter = FilterSearch(driver_function)
        process = OpenProcess(driver_function)
        version = VersionEmailConfig(driver_function)

        process_filter_page = ProcessFilter(driver_function)

        logger.info("Starting test_copy_version")

        login.open()
        login.login()
        loader.load()

        side_menu.process()
        open_filter.filter()

        test_data = load_test_data("process/filter_process.json")
        process_name = test_data["processName"]

        process_filter_page.apply_filter_by_name(process_name)

        process.view_process()

        version.open_email_version_section()
        modal = version.open_add_version_modal()

        modal.fill(data["new"])

        modal.submit()
        modal.wait_for_modal_close()

        logout.logout()
        logger.info("Logout complete. Test finished.")

    def test_email_add_version(self, driver_function):
        login = LoginPage(driver_function)
        loader = Loader(driver_function)
        logout = Logout(driver_function)
        side_menu = SideMenuPage(driver_function)
        open_filter = FilterSearch(driver_function)
        process = OpenProcess(driver_function)
        version = VersionEmailConfig(driver_function)

        process_filter_page = ProcessFilter(driver_function)

        logger.info("Starting test_copy_version")

        login.open()
        login.login()
        loader.load()

        side_menu.process()
        open_filter.filter()

        test_data = load_test_data("process/filter_process.json")
        process_name = test_data["processName"]

        process_filter_page.apply_filter_by_name(process_name)

        process.view_process()

        version.open_email_version_section()
        modal = version.open_add_version_modal()

        modal.enter_version_name("new_version"+ str(get_next_process_number()))
        modal.select_interaction("ib")

        modal.submit()
        modal.wait_for_modal_close()

        logout.logout()
        logger.info("Logout complete. Test finished.")