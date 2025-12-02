import pytest

from flow.filter_flow import FilterFlow
from pages.login.login import LoginPage
from pages.common.loader import Loader
from pages.common.open_filter_search import FilterSearch
from pages.process.process_manager.process_filter import ProcessFilter
from pages.process.process_manager.create_process import CreateProcess  # Assuming this class exists
from pages.common.sidemenupage import SideMenuPage
from pages.process.process_manager.search_process import OpenProcess
from pages.process.channel_config.call.call_stt_config import CallSTTConfig
from pages.common.submit_search_filter import SubmitFilterSearch

from pages.login.logout import Logout
from utils.screenshot import Screenshot
from utils.logger import get_logger
from utils.data_reader import load_test_data  # Assuming this utility exists

# ... existing imports ...

logger = get_logger(__name__)


@pytest.mark.usefixtures("driver_function")
class TestCreateProcess:
    def test_create_process(self, driver_function):
        login = LoginPage(driver_function)
        loader = Loader(driver_function)
        logout = Logout(driver_function)
        side_menu = SideMenuPage(driver_function)
        open_filter = FilterSearch(driver_function)
        open_process = OpenProcess(driver_function)
        create_process = CreateProcess(driver_function)

        process_filter_page = ProcessFilter(driver_function)

        logger.info("Starting test_filter_process_by_name")

        logger.info("Opening login page...")
        login.open()
        logger.info("Login page opened.")

        logger.info("Attempting login...")
        login.login()
        logger.info("Login complete.")

        logger.info("Waiting for page to load after login...")
        loader.load()
        logger.info("Page loaded.")

        logger.info("Navigating to Process section via Side Menu...")
        side_menu.process()  # Assuming this navigates to the process list page
        logger.info("Navigated to Process section.")

        create_process.create_process(
            process_code="Custom_",
            process_name="MyProcess_",
            review_rating=False,
            channels=["email"]
        )

        #
        create_process.create_process()

        assert create_process.last_toast == create_process.PROCESS_SUCCESS_TEXT

        logger.info("Logging out...")
        logout.logout()
        logger.info("Logout complete. Test finished.")

    def test_process_name_already_exist(self, driver_function):
        login = LoginPage(driver_function)
        loader = Loader(driver_function)
        logout = Logout(driver_function)
        side_menu = SideMenuPage(driver_function)
        open_filter = FilterSearch(driver_function)
        open_process = OpenProcess(driver_function)
        create_process = CreateProcess(driver_function)

        process_filter_page = ProcessFilter(driver_function)

        logger.info("Starting test_filter_process_by_name")

        logger.info("Opening login page...")
        login.open()
        logger.info("Login page opened.")

        logger.info("Attempting login...")
        login.login()
        logger.info("Login complete.")

        logger.info("Waiting for page to load after login...")
        loader.load()
        logger.info("Page loaded.")

        logger.info("Navigating to Process section via Side Menu...")
        side_menu.process()  # Assuming this navigates to the process list page
        logger.info("Navigated to Process section.")

        create_process.create_process(
            process_code="SMK_PLAY_24OCT_A",
            process_name="SMK_PLAY_24OCT_A",
            review_rating=False,
            channels=["email"]
        )





        assert create_process.last_toast == create_process.PROCESS_NAME_ALREADY_EXISTS_TEXT
        create_process.close_btn()

        logger.info("Logging out...")
        logout.logout()
        logger.info("Logout complete. Test finished.")

    def test_create_process_with_default_json_data(self, driver_function):
        """Create Process with default JSON data"""

        login = LoginPage(driver_function)
        loader = Loader(driver_function)
        logout = Logout(driver_function)
        side_menu = SideMenuPage(driver_function)
        open_filter = FilterSearch(driver_function)
        open_process = OpenProcess(driver_function)
        create_process_page = CreateProcess(driver_function)

        process_filter_page = ProcessFilter(driver_function)

        logger.info("Starting test_filter_process_by_name")

        logger.info("Opening login page...")
        login.open()
        logger.info("Login page opened.")

        logger.info("Attempting login...")
        login.login()
        logger.info("Login complete.")

        logger.info("Waiting for page to load after login...")
        loader.load()
        logger.info("Page loaded.")

        logger.info("Navigating to Process section via Side Menu...")
        side_menu.process()  # Assuming this navigates to the process list page
        logger.info("Navigated to Process section.")
        create_process_page.create_process(
            process_code="AUTO_DEFAULT_CODE",
            process_name="AUTO_DEFAULT_NAME",
            review_rating=True,
            channels=["chat"]
        )
        assert create_process_page.last_toast == create_process_page.PROCESS_SUCCESS_TEXT

        logger.info("Logging out...")
        logout.logout()
        logger.info("Logout complete. Test finished.")
        # Add assertions here

    def test_create_process_by_passing_custom_parameters(self, driver_function):
        """Create Process by passing custom parameters"""

        login = LoginPage(driver_function)
        loader = Loader(driver_function)
        logout = Logout(driver_function)
        side_menu = SideMenuPage(driver_function)
        open_filter = FilterSearch(driver_function)
        open_process = OpenProcess(driver_function)
        create_process_page = CreateProcess(driver_function)

        process_filter_page = ProcessFilter(driver_function)

        logger.info("Starting test_filter_process_by_name")

        logger.info("Opening login page...")
        login.open()
        logger.info("Login page opened.")

        logger.info("Attempting login...")
        login.login()
        logger.info("Login complete.")

        logger.info("Waiting for page to load after login...")
        loader.load()
        logger.info("Page loaded.")

        logger.info("Navigating to Process section via Side Menu...")
        side_menu.process()  # Assuming this navigates to the process list page
        logger.info("Navigated to Process section.")
        create_process_page.create_process(
            process_code="CUSTOM_CODE",
            process_name="Custom Process Name",
            review_rating=False,
            channels=["email"]
        )
        assert create_process_page.last_toast == create_process_page.PROCESS_SUCCESS_TEXT

        logger.info("Logging out...")
        logout.logout()
        logger.info("Logout complete. Test finished.")

    def test_create_process_with_multiple_channels(self, driver_function):
        """Create Process with multiple channels"""

        login = LoginPage(driver_function)
        loader = Loader(driver_function)
        logout = Logout(driver_function)
        side_menu = SideMenuPage(driver_function)
        open_filter = FilterSearch(driver_function)
        open_process = OpenProcess(driver_function)
        create_process_page = CreateProcess(driver_function)

        process_filter_page = ProcessFilter(driver_function)

        logger.info("Starting test_filter_process_by_name")

        logger.info("Opening login page...")
        login.open()
        logger.info("Login page opened.")

        logger.info("Attempting login...")
        login.login()
        logger.info("Login complete.")

        logger.info("Waiting for page to load after login...")
        loader.load()
        logger.info("Page loaded.")

        logger.info("Navigating to Process section via Side Menu...")
        side_menu.process()  # Assuming this navigates to the process list page
        logger.info("Navigated to Process section.")
        create_process_page.create_process(
            process_code="MULTI_CHANNEL_CODE_1",
            process_name="Multi Channel Process_1",
            review_rating=True,
            channels=["call", "chat", "email"]
        )
        assert create_process_page.last_toast == create_process_page.PROCESS_SUCCESS_TEXT

        logger.info("Logging out...")
        logout.logout()
        logger.info("Logout complete. Test finished.")
        # Add assertions here

    def test_create_process_with_review_rating_false(self, driver_function):
        """Create Process with review_rating = False"""

        login = LoginPage(driver_function)
        loader = Loader(driver_function)
        logout = Logout(driver_function)
        side_menu = SideMenuPage(driver_function)
        open_filter = FilterSearch(driver_function)
        open_process = OpenProcess(driver_function)
        create_process_page = CreateProcess(driver_function)

        process_filter_page = ProcessFilter(driver_function)

        logger.info("Starting test_filter_process_by_name")

        logger.info("Opening login page...")
        login.open()
        logger.info("Login page opened.")

        logger.info("Attempting login...")
        login.login()
        logger.info("Login complete.")

        logger.info("Waiting for page to load after login...")
        loader.load()
        logger.info("Page loaded.")

        logger.info("Navigating to Process section via Side Menu...")
        side_menu.process()  # Assuming this navigates to the process list page
        logger.info("Navigated to Process section.")
        create_process_page.create_process(
            process_code="NO_REVIEW_CODE",
            process_name="No Review Process",
            review_rating=False,
            channels=["chat"]
        )
        assert create_process_page.last_toast == create_process_page.PROCESS_SUCCESS_TEXT

        logger.info("Logging out...")
        logout.logout()
        logger.info("Logout complete. Test finished.")

    def test_required_field_validation_on_save(self, driver_function):
        login = LoginPage(driver_function)
        create_process = CreateProcess(driver_function)
        loader = Loader(driver_function)
        logout = Logout(driver_function)
        side_menu = SideMenuPage(driver_function)

        # Login
        login.open()
        login.login()
        loader.load()

        # Navigate to Process Page
        side_menu.process()
        create_process.click_add_process_button()
        # Open create-process page
        create_process.reset_process()

        # Click Save without entering any fields
        create_process.click_save()

        error_msg = create_process.get_error_message(
            create_process.ERROR_PROCESS_CODE_TEXT_LOCATOR
        )

        # Assert required validation messages
        assert error_msg== "This field is required"


        # Ensure no toast message
        assert create_process.last_toast is None

        # Logout
        logout.logout()

    def test_process_code_max_length_validation(self, driver_function):
        """Process Code max length validation"""

        login = LoginPage(driver_function)
        loader = Loader(driver_function)
        logout = Logout(driver_function)
        side_menu = SideMenuPage(driver_function)
        open_filter = FilterSearch(driver_function)
        open_process = OpenProcess(driver_function)
        create_process_page = CreateProcess(driver_function)

        process_filter_page = ProcessFilter(driver_function)

        logger.info("Starting test_filter_process_by_name")

        logger.info("Opening login page...")
        login.open()
        logger.info("Login page opened.")

        logger.info("Attempting login...")
        login.login()
        logger.info("Login complete.")

        logger.info("Waiting for page to load after login...")
        loader.load()
        logger.info("Page loaded.")

        logger.info("Navigating to Process section via Side Menu...")
        side_menu.process()  # Assuming this navigates to the process list page
        logger.info("Navigated to Process section.")
        long_code = "A" * 256  # Assuming max length is 256
        create_process_page.create_process(
            process_code=long_code,
            process_name="Long Code Process Name",
            review_rating=False,
            channels=["chat"]
        )
        error_msg = create_process_page.get_error_message(
            create_process_page.ERROR_PROCESS_CODE_TEXT_LOCATOR
        )

        assert error_msg == create_process_page.ERROR_PROCESS_CODE_TEXT

        # Add assertions here for validation message or trimming
        logger.info("Logging out...")
        logout.logout()
        logger.info("Logout complete. Test finished.")

    def test_empty_process_code(self, driver_function):
        """Empty Process Code"""

        login = LoginPage(driver_function)
        loader = Loader(driver_function)
        logout = Logout(driver_function)
        side_menu = SideMenuPage(driver_function)
        open_filter = FilterSearch(driver_function)
        open_process = OpenProcess(driver_function)
        create_process_page = CreateProcess(driver_function)

        process_filter_page = ProcessFilter(driver_function)

        logger.info("Starting test_filter_process_by_name")

        logger.info("Opening login page...")
        login.open()
        logger.info("Login page opened.")

        logger.info("Attempting login...")
        login.login()
        logger.info("Login complete.")

        logger.info("Waiting for page to load after login...")
        loader.load()
        logger.info("Page loaded.")

        logger.info("Navigating to Process section via Side Menu...")
        side_menu.process()  # Assuming this navigates to the process list page
        logger.info("Navigated to Process section.")
        create_process_page.create_process(
            process_code="",
            process_name="Empty Code Process",
            review_rating=False,
            channels=["chat"]
        )
        error_msg = create_process_page.get_error_message(
            create_process_page.ERROR_PROCESS_CODE_TEXT_LOCATOR
        )

        assert error_msg == create_process_page.ERROR_PROCESS_CODE_TEXT

        logger.info("Logging out...")
        logout.logout()
        logger.info("Logout complete. Test finished.")

    def test_empty_process_name(self, driver_function):
        """Empty Process Name"""

        login = LoginPage(driver_function)
        loader = Loader(driver_function)
        logout = Logout(driver_function)
        side_menu = SideMenuPage(driver_function)
        open_filter = FilterSearch(driver_function)
        open_process = OpenProcess(driver_function)
        create_process_page = CreateProcess(driver_function)

        process_filter_page = ProcessFilter(driver_function)

        logger.info("Starting test_filter_process_by_name")

        logger.info("Opening login page...")
        login.open()
        logger.info("Login page opened.")

        logger.info("Attempting login...")
        login.login()
        logger.info("Login complete.")

        logger.info("Waiting for page to load after login...")
        loader.load()
        logger.info("Page loaded.")

        logger.info("Navigating to Process section via Side Menu...")
        side_menu.process()  # Assuming this navigates to the process list page
        logger.info("Navigated to Process section.")
        create_process_page.create_process(
            process_code="EMPTY_NAME_CODE",
            process_name="",
            review_rating=False,
            channels=["chat"]
        )
        error_msg = create_process_page.get_error_message(
            create_process_page.ERROR_PROCESS_NAME_TEXT_LOCATOR
        )

        assert error_msg == create_process_page.ERROR_PROCESS_NAME_TEXT

        logger.info("Logging out...")
        logout.logout()
        logger.info("Logout complete. Test finished.")
        # Add assertions here for validation error

    def test_no_channel_selected(self, driver_function):
        """No channel selected"""

        login = LoginPage(driver_function)
        loader = Loader(driver_function)
        logout = Logout(driver_function)
        side_menu = SideMenuPage(driver_function)
        open_filter = FilterSearch(driver_function)
        open_process = OpenProcess(driver_function)
        create_process_page = CreateProcess(driver_function)

        process_filter_page = ProcessFilter(driver_function)

        logger.info("Starting test_filter_process_by_name")

        logger.info("Opening login page...")
        login.open()
        logger.info("Login page opened.")

        logger.info("Attempting login...")
        login.login()
        logger.info("Login complete.")

        logger.info("Waiting for page to load after login...")
        loader.load()
        logger.info("Page loaded.")

        logger.info("Navigating to Process section via Side Menu...")
        side_menu.process()  # Assuming this navigates to the process list page
        logger.info("Navigated to Process section.")
        create_process_page.create_process(
            process_code="NO_CHANNEL_CODE",
            process_name="No Channel Process",
            review_rating=False,
            channels=[]
        )
        assert create_process_page.last_toast == create_process_page.PROCESS_SUCCESS_TEXT
        logger.info("Logging out...")
        logout.logout()
        logger.info("Logout complete. Test finished.")
        # Add assertions here for validation error

    def test_special_characters_in_process_code(self, driver_function):
        """Special characters in Process Code"""

        login = LoginPage(driver_function)
        loader = Loader(driver_function)
        logout = Logout(driver_function)
        side_menu = SideMenuPage(driver_function)
        open_filter = FilterSearch(driver_function)
        open_process = OpenProcess(driver_function)
        create_process_page = CreateProcess(driver_function)

        process_filter_page = ProcessFilter(driver_function)

        logger.info("Starting test_filter_process_by_name")

        logger.info("Opening login page...")
        login.open()
        logger.info("Login page opened.")

        logger.info("Attempting login...")
        login.login()
        logger.info("Login complete.")

        logger.info("Waiting for page to load after login...")
        loader.load()
        logger.info("Page loaded.")

        logger.info("Navigating to Process section via Side Menu...")
        side_menu.process()  # Assuming this navigates to the process list page
        logger.info("Navigated to Process section.")
        create_process_page.create_process(
            process_code="ABC!@#",
            process_name="",
            review_rating=False,
            channels=["chat"]
        )
        error_msg = create_process_page.get_error_message(
            create_process_page.ERROR_PROCESS_CODE_TEXT_LOCATOR
        )

        assert error_msg == create_process_page.ERROR_PROCESS_CODE_FORMAT_TEXT

        logger.info("Logging out...")
        logout.logout()
        logger.info("Logout complete. Test finished.")
