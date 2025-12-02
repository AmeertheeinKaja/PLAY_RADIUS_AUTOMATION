import pytest

from flow.filter_flow import FilterFlow
from pages.login.login import LoginPage
from pages.common.loader import Loader
from pages.common.open_filter_search import FilterSearch
from pages.process.process_manager.process_filter import ProcessFilter

from pages.common.sidemenupage import SideMenuPage
from pages.process.process_manager.search_process import OpenProcess

from pages.process.version.version_call_config import VersionCallConfig

from pages.login.logout import Logout

from utils.logger import get_logger
from utils.data_reader import load_test_data
from utils.counter_manager import get_next_process_number


logger = get_logger(__name__)
data = load_test_data("process/version/versionData.json")


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
        self.version = VersionCallConfig(driver)
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
        self.version.open_call_version_section()


    # -------------------------------------------------------------------------
    # ✔ Existing Basic Tests
    # -------------------------------------------------------------------------
    def test_import_version(self, driver_function):
        self.setup_common(driver_function)

        modal = self.version.open_import_version_modal()

        modal.select_process("Campaign_ADD")
        modal.select_version("test3")
        modal.select_interaction("ib")
        modal.enter_version_name("Imported_" + str(get_next_process_number()))

        modal.submit()
        modal.wait_for_modal_close()

        assert "Version imported successfully" in modal.last_toast

        self.logout.logout()

    def test_copy_version(self, driver_function):
        self.setup_common(driver_function)

        modal = self.version.open_copy_version_modal()

        modal.select_copy_version("Robot")
        modal.select_interaction("ib")
        modal.enter_copy_version_name("copy_version_"+ str(get_next_process_number()))

        modal.submit()
        modal.wait_for_modal_close()

        assert "Version copied successfully" in modal.last_toast

        self.logout.logout()

    def test_add_version_json(self, driver_function):
        self.setup_common(driver_function)

        modal = self.version.open_add_version_modal()
        modal.fill(data["new"])

        modal.submit()
        modal.wait_for_modal_close()

        assert "Version saved successfully" in modal.last_toast

        self.logout.logout()

    def test_add_version(self, driver_function):
        self.setup_common(driver_function)

        modal = self.version.open_add_version_modal()
        modal.enter_version_name("new_version" + str(get_next_process_number()))
        modal.select_interaction("ib")

        modal.submit()
        modal.wait_for_modal_close()

        assert "Version saved successfully" in modal.last_toast

        self.logout.logout()


    # -------------------------------------------------------------------------
    # 📌 IMPORT VERSION – Detailed Tests
    # -------------------------------------------------------------------------
    def test_import_version_with_all_valid_fields(self, driver_function):
        pass

    def test_import_version_from_different_process_same_version_name(self, driver_function):
        pass

    def test_import_version_with_non_existent_source_process(self, driver_function):
        pass

    def test_import_version_with_non_existent_source_version(self, driver_function):
        pass

    def test_import_version_with_duplicate_target_version_name(self, driver_function):
        pass

    def test_import_version_with_empty_new_version_name(self, driver_function):
        pass

    def test_import_version_with_invalid_new_version_name_format(self, driver_function):
        pass

    def test_import_version_without_selecting_process(self, driver_function):
        pass

    def test_import_version_without_selecting_version(self, driver_function):
        pass

    def test_import_version_without_selecting_interaction(self, driver_function):
        pass

    def test_import_version_new_version_name_max_length(self, driver_function):
        pass

    def test_cancel_import_version(self, driver_function):
        pass


    # -------------------------------------------------------------------------
    # 📌 COPY VERSION – Detailed Tests
    # -------------------------------------------------------------------------
    def test_copy_version_with_valid_new_name(self, driver_function):
        pass

    def test_copy_version_with_different_interaction(self, driver_function):
        pass

    def test_copy_non_existent_version(self, driver_function):
        pass

    def test_copy_version_with_duplicate_new_version_name(self, driver_function):
        pass

    def test_copy_version_with_empty_new_version_name(self, driver_function):
        pass

    def test_copy_version_with_invalid_new_version_name_format(self, driver_function):
        pass

    def test_copy_version_without_selecting_version_to_copy(self, driver_function):
        pass

    def test_copy_version_without_selecting_interaction(self, driver_function):
        pass

    def test_copy_version_new_version_name_max_length(self, driver_function):
        pass

    def test_cancel_copy_version(self, driver_function):
        pass

    def test_copy_version_multiple_times(self, driver_function):
        pass


    # -------------------------------------------------------------------------
    # 📌 ADD VERSION JSON – Detailed Tests
    # -------------------------------------------------------------------------
    def test_add_version_json_with_minimal_valid_data(self, driver_function):
        pass

    def test_add_version_json_with_all_valid_data(self, driver_function):
        pass

    def test_add_version_json_with_missing_required_fields(self, driver_function):
        pass

    def test_add_version_json_with_invalid_data_types(self, driver_function):
        pass

    def test_add_version_json_with_duplicate_version_name(self, driver_function):
        pass

    def test_add_version_json_with_malformed_json(self, driver_function):
        pass

    def test_add_version_json_with_unsupported_fields(self, driver_function):
        pass

    def test_add_version_json_version_name_max_length(self, driver_function):
        pass

    def test_add_version_json_empty_json_data(self, driver_function):
        pass


    # -------------------------------------------------------------------------
    # 📌 ADD VERSION – Detailed Tests
    # -------------------------------------------------------------------------
    def test_add_version_with_unique_name_and_valid_interaction(self, driver_function):
        pass

    def test_add_version_with_empty_version_name(self, driver_function):
        pass

    def test_add_version_with_duplicate_version_name(self, driver_function):
        pass

    def test_add_version_without_selecting_interaction(self, driver_function):
        pass

    def test_add_version_with_invalid_interaction(self, driver_function):
        pass

    def test_add_version_new_version_name_max_length(self, driver_function):
        pass
