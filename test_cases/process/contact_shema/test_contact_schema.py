import pytest
from selenium.webdriver.common.by import By

from pages.login.login import LoginPage
from pages.common.loader import Loader
from pages.process.process_manager.create_process import CreateProcess
from pages.process.process_manager.process_filter import ProcessFilter
from pages.common.sidemenupage import SideMenuPage
from pages.common.open_filter_search import FilterSearch
from pages.process.process_manager.search_process import OpenProcess
from pages.process.contact_schema.contact_schema_page import ContactSchema

from pages.process.process_manager.create_process import CreateProcess


from pages.login.logout import Logout
from utils.process_factory import create_process_from_json
from utils.screenshot import Screenshot
from utils.logger import get_logger
from utils.data_reader import load_test_data

logger = get_logger(__name__)


@pytest.mark.usefixtures("driver_function")
class TestContactSchema:

    def test_add_contact_schema(self, driver_function):
        """
        Full STT configuration test (happy path)


        """



        driver = driver_function
        contact_data = load_test_data("process/contact_schema/contact_schema.json")
        mode = contact_data["mode"]
        fields = contact_data["fields"]

        logout = None

        try:
            login = LoginPage(driver)
            loader = Loader(driver)
            side_menu = SideMenuPage(driver)
            create_process = CreateProcess(driver)
            filter_search = FilterSearch(driver)
            process_filter = ProcessFilter(driver)
            open_Process = OpenProcess(driver)
            contact_schema = ContactSchema(driver)


            logout = Logout(driver)

            login.open()
            login.login()
            loader.load()

            side_menu.process()
            create_process = create_process_from_json(driver_function)
            create_process.create_process()

            contact_schema.tab_contact_schema()
            contact_schema.configure_contact_schema(mode, fields)
            # contact_schema.edit_attribute()
            loader.load()

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

    def test_edit_contact_schema(self, driver_function):
        """
        Full STT configuration test (happy path)


        """

        driver = driver_function
        contact_data = load_test_data("process/contact_schema/contact_schema.json")
        mode = contact_data["mode"]
        fields = contact_data["fields"]

        logout = None

        try:
            login = LoginPage(driver)
            loader = Loader(driver)
            side_menu = SideMenuPage(driver)
            create_process = CreateProcess(driver)
            filter_search = FilterSearch(driver)
            process_filter = ProcessFilter(driver)
            open_Process = OpenProcess(driver)
            contact_schema = ContactSchema(driver)

            logout = Logout(driver)

            login.open()
            login.login()
            loader.load()

            side_menu.process()
            # create_process.create_process()
            filter_search.filter()
            process_filter.apply_filter_by_name("SMK_PLAY_24OCT_A")
            open_Process.view_process()
            contact_schema.tab_contact_schema()

            contact_schema.edit_attribute(fields)
            loader.load()

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

    def test_add_contact_schema_auto(self, driver_function):
        """
        Full STT configuration test (happy path)


        """

        driver = driver_function
        contact_data = load_test_data("process/contact_schema/contact_schema.json")
        mode = contact_data["mode"]
        fields = contact_data["fields"]

        logout = None

        try:
            login = LoginPage(driver)
            loader = Loader(driver)
            side_menu = SideMenuPage(driver)
            create_process = CreateProcess(driver)

            contact_schema = ContactSchema(driver)

            logout = Logout(driver)

            login.open()
            login.login()
            loader.load()

            side_menu.process()
            create_process.create_process()

            contact_schema.tab_contact_schema()
            contact_schema.configure_contact_schema(mode,fields)

            loader.load()

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

    def test_create_process_with_auto_mode(self, driver_function):

        driver = driver_function

        login = LoginPage(driver)
        loader = Loader(driver)
        side_menu = SideMenuPage(driver)
        create_process = CreateProcess(driver)
        contact_schema = ContactSchema(driver)
        logout = Logout(driver)

        login.open()
        login.login()
        loader.load()

        side_menu.process()

        create_process.create_process()
        contact_schema.tab_contact_schema()

        contact_schema.configure_contact_schema(mode="automode")

        loader.load()
        toast = contact_schema.last_toast
        assert contact_schema.ADD_SUCCESS_TEXT in toast

        logout.logout()

    def test_create_process_with_manual_mode(self, driver_function):

        driver = driver_function
        data = load_test_data("process/contact_schema/contact_schema.json")

        login = LoginPage(driver)
        loader = Loader(driver)
        side_menu = SideMenuPage(driver)
        create_process = CreateProcess(driver)
        contact_schema = ContactSchema(driver)
        logout = Logout(driver)

        login.open()
        login.login()
        loader.load()

        side_menu.process()

        # PROCESS CREATION FLOW
        create_process.create_process()
        contact_schema.tab_contact_schema()

        # MANUAL MODE OPERATION
        field_data = data["fields"]
        # Example:
        # [
        #   {"fieldName":"contact_id","dataType":"String"},
        #   {"fieldName":"is_active","dataType":"Boolean"}
        # ]

        contact_schema.configure_contact_schema(
            mode="manualmode",
            field_list=field_data
        )

        loader.load()

        toast = contact_schema.last_toast

        # MANUAL SAVE SUCCESS SHOULD MATCH
        assert contact_schema.ADD_SUCCESS_TEXT in toast, \
            f"Expected '{contact_schema.ADD_SUCCESS_TEXT}', got '{toast}'"

        logout.logout()

    def test_edit_contact_schema_with_param(self, driver_function):

        driver = driver_function

        login = LoginPage(driver)
        loader = Loader(driver)
        side_menu = SideMenuPage(driver)
        filter_search = FilterSearch(driver)
        process_filter = ProcessFilter(driver)
        open_process = OpenProcess(driver)
        contact_schema = ContactSchema(driver)
        logout = Logout(driver)

        login.open()
        login.login()
        loader.load()

        side_menu.process()

        # FILTER + OPEN SPECIFIC PROCESS
        filter_search.filter()
        process_filter.apply_filter_by_name("SMK_PLAY_24OCT_A")
        open_process.view_process()

        # OPEN CONTACT SCHEMA
        contact_schema.tab_contact_schema()

        # NEW FIELD DATA FOR EDIT
        update_fields = [
            {"fieldName": "customer_id", "dataType": "String"},
            {"fieldName": "created_date", "dataType": "Date"},
            {"fieldName": "modified_time", "dataType": "Time"}
        ]

        contact_schema.edit_attribute(update_fields)

        loader.load()

        toast = contact_schema.last_toast
        assert contact_schema.UPDATE_SUCCESS in toast, \
            f"Expected '{contact_schema.UPDATE_SUCCESS}' in toast, got '{toast}'"

        logout.logout()

    def test_delete_specific_contact_schema_field(self, driver_function):

        driver = driver_function

        login = LoginPage(driver)
        loader = Loader(driver)
        side_menu = SideMenuPage(driver)
        filter_search = FilterSearch(driver)
        process_filter = ProcessFilter(driver)
        open_process = OpenProcess(driver)
        contact_schema = ContactSchema(driver)
        logout = Logout(driver)

        login.open()
        login.login()
        loader.load()

        side_menu.process()

        # FILTER EXISTING PROCESS
        filter_search.filter()
        process_filter.apply_filter_by_name("SMK_PLAY_24OCT_A")
        open_process.view_process()

        # OPEN CONTACT SCHEMA
        contact_schema.tab_contact_schema()

        # IDENTIFY ATTRIBUTE TO DELETE
        attribute_to_delete = "customer_id"
        # valid name created in previous edit test

        # COUNT RECORDS BEFORE DELETE
        before_count = contact_schema.get_existing_row_count()

        # DELETE
        contact_schema.delete_attribute_by_name(attribute_to_delete)

        loader.load()

        # COUNT AFTER DELETE
        after_count = contact_schema.get_existing_row_count()

        # EXPECT ONE LESS
        assert after_count == before_count - 1, \
            f"Expected {before_count - 1} rows, got {after_count}"

        # VALIDATE TOAST
        toast = contact_schema.last_toast
        assert contact_schema.UPDATE_SUCCESS in toast, \
            f"Toast mismatch. Actual: {toast}"

        logout.logout()

    def test_duplicate_field_name_validation(self, driver_function):

        driver = driver_function

        login = LoginPage(driver)
        loader = Loader(driver)
        side_menu = SideMenuPage(driver)
        create_process = CreateProcess(driver)
        contact_schema = ContactSchema(driver)
        logout = Logout(driver)

        login.open()
        login.login()
        loader.load()

        side_menu.process()

        create_process.create_process()
        contact_schema.tab_contact_schema()

        contact_schema.choose_mode("manualmode")

        # add first attribute
        field1 = [{"fieldName": "duplicate_test", "dataType": "String"}]
        contact_schema.add_attribute(field1)

        # insert duplicate using page class helper function
        contact_schema.insert_duplicate_field(
            field_name="duplicate_test",
            datatype="Integer"
        )

        toast = contact_schema.last_toast

        assert contact_schema.ERROR_TEXT in toast, \
            f"Expected duplicate validation error toast, got '{toast}'"

        logout.logout()
