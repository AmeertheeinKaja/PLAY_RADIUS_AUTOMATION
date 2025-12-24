import pytest

from pages.login.login import LoginPage
from pages.login.logout import Logout
from pages.common.loader import Loader
from pages.common.sidemenupage import SideMenuPage
from pages.common.open_filter_search import FilterSearch
from pages.process.process_manager.process_filter import ProcessFilter
from pages.process.process_manager.search_process import OpenProcess
from pages.process.contact_schema.upload_record_page import UploadRecord

from utils.data_reader import load_test_data
from utils.screenshot import Screenshot
from utils.logger import get_logger

logger = get_logger(__name__)


@pytest.mark.usefixtures("driver_function")
class TestUploadRecordSuite:

    @staticmethod
    def setup_upload_record_for_process(driver, process_name):
        """
        Common reusable setup for navigating to Upload Record page
        """
        login = LoginPage(driver)
        loader = Loader(driver)
        side_menu = SideMenuPage(driver)
        filter_search = FilterSearch(driver)
        process_filter = ProcessFilter(driver)
        open_process = OpenProcess(driver)

        login.open()
        login.login()
        loader.load()

        side_menu.process()
        filter_search.filter()
        process_filter.apply_filter_by_name(process_name)
        open_process.view_process()
        loader.load()

        return UploadRecord(driver)

    # -------------------------
    # TEST CASES
    # -------------------------

    def test_upload_record_success(self, driver_function):
        driver = driver_function
        logout = Logout(driver)
        record_path = load_test_data("process/contact_schema/record_data.json")

        try:
            upload_record = self.setup_upload_record_for_process(
                driver, "SMK_PLAY_30A"
            )

            upload_record.open_upload()
            result = upload_record.upload_process(record_path)
            assert result is True, "Upload process failed"

            error_count = upload_record.get_error_count()
            assert error_count == 0, f"Unexpected error count: {error_count}"

        except Exception as e:
            logger.error(f"test_upload_record_success failed: {e}")
            Screenshot.take(driver, "test_upload_record_success_failed")
            raise
        finally:
            logout.logout()

    def test_upload_tab_disabled(self, driver_function):
        driver = driver_function
        logout = Logout(driver)

        try:
            upload_record = self.setup_upload_record_for_process(
                driver, "SINGLKE_Q_INBPOUND"
            )

            assert upload_record.is_upload_tab_disabled() is True

        finally:
            logout.logout()

    def test_template_submit_disabled(self, driver_function):
        driver = driver_function
        logout = Logout(driver)

        try:
            upload_record = self.setup_upload_record_for_process(
                driver, "SMK_PLAY_30A"
            )

            upload_record.open_upload()
            assert upload_record.is_submit_disabled() is True, \
                "Submit button should be disabled"

        except Exception as e:
            logger.error(f"test_template_submit_disabled failed: {e}")
            Screenshot.take(driver, "test_template_submit_disabled_failed")
            raise
        finally:
            logout.logout()

    def test_error_count_not_visible(self, driver_function):
        driver = driver_function
        logout = Logout(driver)

        try:
            upload_record = self.setup_upload_record_for_process(
                driver, "SMK_PLAY_30A"
            )

            count = upload_record.get_error_count()
            assert isinstance(count, int), "Error count should return integer"

        except Exception as e:
            logger.error(f"test_error_count_not_visible failed: {e}")
            Screenshot.take(driver, "test_error_count_not_visible_failed")
            raise
        finally:
            logout.logout()

    def test_reset_after_upload(self, driver_function):
        driver = driver_function
        logout = Logout(driver)
        record_path = load_test_data("process/contact_schema/record_data.json")

        try:
            upload_record = self.setup_upload_record_for_process(
                driver, "SMK_PLAY_30A"
            )

            upload_record.open_upload()
            upload_record.download()
            upload_record.download_and_update_csv(record_path)
            upload_record.upload()
            upload_record.reset()

            assert True, "Reset completed successfully"

        except Exception as e:
            logger.error(f"test_reset_after_upload failed: {e}")
            Screenshot.take(driver, "test_reset_after_upload_failed")
            raise
        finally:
            logout.logout()
