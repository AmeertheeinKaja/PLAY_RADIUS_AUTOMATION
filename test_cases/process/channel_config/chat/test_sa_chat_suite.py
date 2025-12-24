import pytest
from selenium.webdriver.support.select import Select

from pages.login.login import LoginPage
from pages.common.loader import Loader
from pages.common.sidemenupage import SideMenuPage
from pages.process.process_manager.create_process import CreateProcess
from pages.process.process_manager.process_filter import ProcessFilter
from pages.common.open_filter_search import FilterSearch
from pages.process.process_manager.search_process import OpenProcess
from pages.process.channel_config.chat.chat_sa_config import ChatSAConfig
from pages.login.logout import Logout
from utils.data_reader import load_test_data
from utils.logger import get_logger
from utils.process_factory import create_process_from_json

logger = get_logger(__name__)


@pytest.mark.usefixtures("driver_function")
class TestChatSASuite:

    def _common_navigation(self, driver, process_name=None):

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
        loader.load()

        if process_name:
            filter_search.filter()
            process_filter.apply_filter_by_name(process_name)
            open_process.view_process()
        else:
            create_process = CreateProcess(driver)
            create_process = create_process_from_json(driver)
            create_process.create_process()

        loader.load()

    def _open_sa(self, driver):
        cfg = load_test_data("process/create_process.json")
        stt_cfg = cfg["channel_config"]["chat"]["sa"]
        return ChatSAConfig(
            driver,
            sentiment_analysis=stt_cfg.get("sentiment_analysis"),
            engine_name=stt_cfg.get("engine_name"),
            keyFile=stt_cfg.get("keyFile"),
            sentiment_text=stt_cfg.get("sentiment_text"),
            conversion_mode=stt_cfg.get("conversion_mode"),
        )


    # TEST CASE 1: Full config happy path
    def test_sa_full_config(self, driver_function):
        driver = driver_function
        self._common_navigation(driver)
        sa = self._open_sa(driver)
        sa.config_sa()

    # TEST CASE 2: Reconfigure existing
    def test_sa_reconfig(self, driver_function):
        driver = driver_function
        self._common_navigation(driver)
        sa = self._open_sa(driver)
        sa.reconfig_sa()

    # TEST CASE 3: Toggle ON -> Save -> OFF -> Save
    def test_sa_reset(self, driver_function):
        driver = driver_function
        self._common_navigation(driver)
        sa = self._open_sa(driver)

        sa.tab_sa()
        sa.click_edit()
        sa.click_reset()

        assert sa.wait_until_visible(sa.EDIT_LOC_MAIN, timeout=5), \
            "Edit button not shown after reset"


    # TEST CASE 4: Toggle disabled before edit validation
    def test_sa_toggle_locked_before_edit(self, driver_function):
        driver = driver_function
        self._common_navigation(driver)
        sa = self._open_sa(driver)

        sa.tab_sa()
        selected, disabled = sa.get_edit_toggle_state()

        assert disabled is True

    # TEST CASE 5: Missing engine validation
    def test_sa_engine_missing_validation(self, driver_function):
        driver = driver_function
        self._common_navigation(driver)

        sa = ChatSAConfig(driver, engine_name="")
        sa.tab_sa()
        sa.click_edit()
        sa.toggle_sa(True)
        sa.click_save()

        error = sa.get_sa_error("engine")
        assert error != ""

    # TEST CASE 6: Missing key file validation
    def test_sa_keyfile_missing_validation(self, driver_function):
        driver = driver_function
        self._common_navigation(driver)

        sa = ChatSAConfig(
            driver,
            sentiment_analysis=True,
            engine_name="google",
            conversion_mode="manualMode",
            keyFile=""
        )

        sa.tab_sa()
        sa.click_edit()

        # Toggle ON using JSON-driven constructor value
        sa.toggle_sa()

        # Engine + mode auto handled via constructor logic
        sa.select_engine()
        sa.choose_conversion_mode()

        sa.click_save()

        error = sa.get_sa_error("key_file")
        assert error.strip() == "This field is required"

    # TEST CASE 7: Missing modal sentiment text error
    def test_sa_modal_text_missing(self, driver_function):
        driver = driver_function
        self._common_navigation(driver)
        sa = self._open_sa(driver)

        sa.tab_sa()
        sa.click_edit()
        sa.toggle_sa(True)
        sa.select_engine()
        sa.choose_conversion_mode()
        sa.key_file_input()

        sa.click_save()
        sa.click_test()
        sa.click_submit()

        error = sa.get_sa_error("sentiment_text")
        assert error != ""


    # TEST CASE 8: Reset functionality
    def test_sa_chat_reset(self, driver_function):
        driver = driver_function

        # Step 1 → reach SA screen
        self._common_navigation(driver)
        sa = self._open_sa(driver)

        # capture UI saved state BEFORE reset
        sa.tab_sa()
        saved_toggle = driver.find_element(*sa.SA_TOGGLE_INPUT).is_selected()
        saved_engine = None

        if sa.is_element_present(sa.SA_SELECT_ENGINE):
            saved_engine = Select(
                driver.find_element(*sa.SA_SELECT_ENGINE)
            ).first_selected_option.get_attribute("value")

        # Step 2 → enter edit mode
        sa.click_edit()
        sa.loader.load()

        # MODIFY UI before resetting
        sa.toggle_sa(not saved_toggle)  # make a change
        if saved_engine:
            Select(driver.find_element(*sa.SA_SELECT_ENGINE)) \
                .select_by_index(0)  # random change

        # Step 3 → RESET FORM
        sa.click_reset()
        sa.loader.load()

        # Step 4 → ASSERTIONS

        # 4.1 edit button must return visible
        assert sa.is_element_present(sa.EDIT_LOC_MAIN), \
            "Edit button not visible after reset"

        # 4.2 toggle should return to previously saved state
        reset_toggle = driver.find_element(*sa.SA_TOGGLE_INPUT).is_selected()
        assert reset_toggle == saved_toggle, \
            f"Toggle mismatch after reset. Expected {saved_toggle} Got {reset_toggle}"

        # 4.3 engine drop-down should return to ORIGINAL value
        if saved_engine:
            reset_engine = Select(
                driver.find_element(*sa.SA_SELECT_ENGINE)
            ).first_selected_option.get_attribute("value")

            assert reset_engine == saved_engine, \
                f"Engine mismatch after reset. Expected {saved_engine} Got {reset_engine}"

        # 4.4 Save button must NOT be visible
        assert not sa.is_element_present(sa.SA_SAVE_BTN), \
            "Save button still present -> form stuck in edit state"

        # 4.5 No validation errors allowed
        assert "error" not in driver.page_source.lower(), \
            "Error visible after reset -> UI failed"



    # TEST CASE 10: Toast validation
    def test_sa_toast_save_message(self, driver_function):
        driver = driver_function
        self._common_navigation(driver)

        sa = self._open_sa(driver)
        sa.tab_sa()
        sa.click_edit()
        sa.toggle_sa(False)
        sa.click_save()

        assert sa.last_toast is not None
        assert "success" in sa.last_toast.lower()
