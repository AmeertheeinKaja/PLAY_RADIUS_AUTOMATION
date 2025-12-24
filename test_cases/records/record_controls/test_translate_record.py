import pytest
from pages.login.login import LoginPage
from pages.login.logout import Logout
from pages.record.record_manager import RecordManager
from pages.filtering.filter_record_by_attribute import FilterByAttribute
from pages.common.open_filter_search import FilterSearch
from pages.common.submit_search_filter import SubmitFilterSearch
from pages.common.sidemenupage import SideMenuPage
from pages.record.record_controls.record_translate import RecordTranslate
from pages.common.loader import Loader
from utils.data_reader import load_test_data


@pytest.mark.usefixtures("driver_function")
class TestTranslateRecord:
    data = load_test_data("record/translate_data.json")["translationTests"]

    @pytest.fixture
    def setup_pages(self, driver_function):
        """Provides initialized page objects for all tests."""
        driver = driver_function
        return {
            "driver": driver,
            "login": LoginPage(driver),
            "logout": Logout(driver),
            "loader": Loader(driver),
            "record_manager": RecordManager(driver),
            "filter_record": FilterByAttribute(driver),
            "open_filter": FilterSearch(driver),
            "filter_action": SubmitFilterSearch(driver),
            "side_menu": SideMenuPage(driver),
            "translator": RecordTranslate(driver)
        }

    def open_record(self, pages, record_id):
        pages["side_menu"].record()
        pages["open_filter"].filter()

        pages["filter_record"].search("Record ID", record_id)
        pages["filter_action"].searchFilter()

        pages["record_manager"].view_record()
        pages["loader"].load()

    # ------------------------------------
    # TEST 1: Base Japanese Translation
    # ------------------------------------
    def test_translate_record(self, setup_pages):
        pages = setup_pages

        # Login
        pages["login"].open()
        pages["login"].login()
        pages["loader"].load()

        # Open record
        record_id = "QU1765383423414EC"
        self.open_record(pages, record_id)

        # Translate
        pages["translator"].open_translate()
        pages["translator"].select_language_by_text("Japanese")
        pages["loader"].load()
        pages["translator"].open_translate()

        translated = pages["translator"].get_translated_lang()
        assert translated == "Japanese", f"Expected 'Japanese' but got '{translated}'"

        # Restore original
        pages["translator"].click_original_btn()
        pages["loader"].load()

        # Logout
        pages["logout"].logout()

    # ------------------------------------
    # TEST 2: Parameterized Multi-language Test
    # ------------------------------------
    @pytest.mark.parametrize("lang", ["Japanese", "Spanish", "Arabic", "French"])
    def test_translate_record_multiple_languages(self, setup_pages, lang):
        pages = setup_pages

        # Login
        pages["login"].open()
        pages["login"].login()
        pages["loader"].load()

        record_id = "QU1765383423414EC"
        self.open_record(pages, record_id)

        # Translate
        pages["translator"].open_translate()
        pages["translator"].select_language_by_text(lang)
        pages["loader"].load()
        pages["translator"].open_translate()

        translated = pages["translator"].get_translated_lang()
        assert translated == lang, f"Expected '{lang}' but got '{translated}'"

        # Restore original
        pages["translator"].click_original_btn()
        pages["loader"].load()

        pages["logout"].logout()

    def test_translate_record_data_driven(self, setup_pages):
        pages = setup_pages

        # Login
        pages["login"].open()
        pages["login"].login()
        pages["loader"].load()

        # Iterate through each record-language pair in JSON
        for case in self.data:
            record_id = case["recordId"]
            lang = case["language"]
            expected = case["expectedTranslatedLanguage"]

            # Open record
            self.open_record(pages, record_id)

            # Translate
            pages["translator"].open_translate()
            pages["translator"].select_language_by_text(lang)
            pages["loader"].load()
            pages["translator"].open_translate()

            translated = pages["translator"].get_translated_lang()

            # Assertion
            assert translated == expected, (
                f"For record {record_id}, expected '{expected}' but got '{translated}'"
            )

            # Restore Original
            pages["translator"].click_original_btn()
            pages["loader"].load()

        # Logout after all test cases
        pages["logout"].logout()
