from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
import time

from selenium.webdriver.support.select import Select

from pages.base_page import BasePage

from utils.counter_manager import get_next_process_number
from utils.logger import get_logger

from utils.screenshot import Screenshot
from utils.data_reader import load_test_data
from utils.screenshot import Screenshot

data = load_test_data("versionData.json")
logger = get_logger()

class VersionChatConfig(BasePage):

    CHAT_VERSION_ACCORD = (By.XPATH, "//button[@id='chat_version_accord']")
    IMPORT_CALL_VERSION = (By.XPATH, "//ul[@id='menuv_chat']//button[@title='Import Version']")
    COPY_CALL_VERSION = (By.XPATH, "//ul[@id='menuv_chat']//button[@title='Copy Version']")
    ADD_CALL_VERSION = (By.XPATH, "//ul[@id='menuv_chat']//button[@title='Add Version']")
    VERSION_NAME = (By.XPATH, "//input[@name='name']")
    VERSION_INTERACTION = (By.XPATH, "//select[@name='interaction']")
    SUBMIT_BUTTON = (By.XPATH, "//button[normalize-space()='Submit']")
    CANCEL_BUTTON = (By.XPATH, "//button[@id='addVersionClose']")
    VERSION_PROCESS_NAME = (By.XPATH, "//select[@name='selProcess']")
    VERSION_VERSION = (By.XPATH, "//select[@name='selVersion']")
    VERSION_CPY_VERSION = (By.XPATH, "//select[@name='cpyVersion']")

    VERSION_CPY_VERSION_NAME = (By.XPATH, "//input[@name='cpyVrsnname']")

    def __init__(self, driver):
        super().__init__(driver)
        self.version_name = data.get("new", {}).get("name")
        self.interaction = data.get("new", {}).get("interaction")
        self.import_version_process = data.get("import", {}).get("process_name")
        self.import_version_version = data.get("import", {}).get("version")
        self.import_version_interaction = data.get("import", {}).get("interaction")
        self.import_version_name= data.get("import", {}).get("name")
        self.copy_version_version = data.get("copy", {}).get("version")
        self.copy_version_interaction = data.get("copy", {}).get("interaction")
        self.copy_version_name = data.get("copy", {}).get("name")


    def chat_version_accord(self):
        try:
            call_version_accord=self.wait_until_clickable(self.CHAT_VERSION_ACCORD)
            call_version_accord.click()
            self.wait_until_clickable(self.CHAT_VERSION_ACCORD)

            print("Call Version Accord Clicked")
            logger.info("Call Version Accord Clicked")

        except Exception as e:
            print("Error during clicking Call Version Accord",e)
            logger.error("Error during clicking Call Version Accord",e)

    def import_chat_version(self):
        try:
            import_call_version=self.wait_until_clickable(self.IMPORT_CALL_VERSION)
            import_call_version.click()
            self.wait_until_clickable(self.IMPORT_CALL_VERSION)

            print("Import Call Version Clicked")
            logger.info("Import Call Version Clicked")

            try:
                # Wait for modal to appear
                modal_locator = (By.XPATH,
                                 "//div[@role='dialog' and contains(@class,'modal') and contains(@class,'show')]")
                self.wait_until_clickable(modal_locator)

                logger.info("Import Version modal is visible.")
                # Select process (Inbound/Outbound)
                process_dropdown = Select(self.wait_until_clickable(self.VERSION_PROCESS_NAME))

                process_dropdown.select_by_visible_text(self.import_version_process)
                logger.info(f"Selected process: {self.import_version_process}")
                # Select interaction (Inbound/Outbound)
                version_dropdown = Select(self.wait_until_clickable(self.VERSION_VERSION))

                version_dropdown.select_by_visible_text(self.import_version_version)
                logger.info(f"Selected version: {self.import_version_version}")

                # Select interaction (Inbound/Outbound)
                interaction_dropdown = Select(self.wait_until_clickable(self.VERSION_INTERACTION))

                interaction_dropdown.select_by_value(self.import_version_interaction)  # use 'ob' or 'ib'
                logger.info(f"Selected interaction: {self.import_version_interaction}")

                # Fill version name
                version_name_input=self.wait_until_present(self.VERSION_NAME)

                version_name_input.clear()
                version_name_input.send_keys(self.import_version_name)
                logger.info(f"Entered version name: {self.import_version_name}")



                # Click Submit
                submit_button=self.wait_until_clickable(self.SUBMIT_BUTTON)
                submit_button.click()

                # driver.execute_script("arguments[0].click();", submit_button)
                logger.info("Clicked Submit button on version modal.")

                time.sleep(2)

                self.wait_invisible(modal_locator)

                # Wait for modal to disappear

                logger.info("Import Version modal closed successfully.")
                Screenshot.take(f"Import_Version_Modal_Closed_Successfully")

                return True

            except TimeoutException:
                logger.warning("⚠️ Import Version modal not found or took too long to load.")
                return False

            except Exception as e:
                logger.error("❌ Error while importing version", exc_info=True)
                return False


        except Exception as e:
            print("Error during clicking Import Call Version",e)
            logger.error("Error during clicking Import Call Version",e)

    def copy_chat_version(self):
        try:
            copy_call_version=self.wait_until_clickable(self.COPY_CALL_VERSION)
            copy_call_version.click()
            self.wait_until_clickable(self.COPY_CALL_VERSION)

            print("Copy Call Version Clicked")
            logger.info("Copy Call Version Clicked")
            Screenshot.take(f"Copy_Call_Version_Clicked")

            try:
                # Wait for modal to appear
                modal_locator = (By.XPATH,
                                 "//div[@role='dialog' and contains(@class,'modal') and contains(@class,'show')]")
                self.wait_until_clickable(modal_locator)

                logger.info("Copy Version modal is visible.")
                # Select interaction (Inbound/Outbound)
                version_dropdown = Select(self.wait_until_clickable(self.VERSION_CPY_VERSION))

                version_dropdown.select_by_visible_text(self.copy_version_version)
                logger.info(f"Selected version: {self.copy_version_version}")

                # Select interaction (Inbound/Outbound)
                interaction_dropdown = Select(self.wait_until_clickable(self.VERSION_INTERACTION))

                interaction_dropdown.select_by_value(self.copy_version_interaction)  # use 'ob' or 'ib'
                logger.info(f"Selected interaction: {self.copy_version_interaction}")

                # Fill version name
                version_name_input=self.wait_until_present(self.VERSION_CPY_VERSION_NAME)

                version_name_input.clear()
                version_name_input.send_keys(self.copy_version_name)
                logger.info(f"Entered version name: {self.copy_version_name}")



                # Click Submit
                submit_button=self.wait_until_clickable(self.SUBMIT_BUTTON)
                submit_button.click()

                # driver.execute_script("arguments[0].click();", submit_button)
                logger.info("Clicked Submit button on version modal.")

                time.sleep(2)

                self.wait_invisible(modal_locator)

                # Wait for modal to disappear

                logger.info("Add Version modal closed successfully.")
                Screenshot.take(f"Copy_Call_Version_Modal_Closed_Successfully")

                return True

            except TimeoutException:
                logger.warning("⚠️ Copy Version modal not found or took too long to load.")
                return False

            except Exception as e:
                logger.error("❌ Error while copying version", exc_info=True)
                return False


        except Exception as e:
            print("Error during clicking Copy Call Version",e)
            logger.error("Error during clicking Copy Call Version",e)
            Screenshot.take(f"Copy_Call_Version_Clicked")

    def add_chat_version(self):
        try:
            add_call_version=self.wait_until_clickable(self.ADD_CALL_VERSION)
            add_call_version.click()
            self.wait_until_clickable(self.ADD_CALL_VERSION)

            print("Add Call Version Clicked")
            logger.info("Add Call Version Clicked")
            Screenshot.take(f"Add_Call_Version_Clicked")

            try:
                # Wait for modal to appear
                modal_locator = (By.XPATH,
                                 "//div[@role='dialog' and contains(@class,'modal') and contains(@class,'show')]")
                self.wait_until_clickable(modal_locator)

                logger.info("Add Version modal is visible.")

                # Fill version name
                version_name_input=self.wait_until_present(self.VERSION_NAME)

                version_name_input.clear()
                version_name_input.send_keys(self.version_name)
                logger.info(f"Entered version name: {self.version_name}")

                # Select interaction (Inbound/Outbound)
                interaction_dropdown=Select(self.wait_until_clickable(self.VERSION_INTERACTION))

                interaction_dropdown.select_by_value(self.interaction)  # use 'ob' or 'ib'
                logger.info(f"Selected interaction: {self.interaction}")

                # Click Submit
                submit_button=self.wait_until_clickable(self.SUBMIT_BUTTON)
                submit_button.click()

                # driver.execute_script("arguments[0].click();", submit_button)
                logger.info("Clicked Submit button on version modal.")

                time.sleep(2)

                self.wait_invisible(modal_locator)

                # Wait for modal to disappear

                logger.info("Add Version modal closed successfully.")
                Screenshot.take(f"Add_Call_Version_Modal_Closed_Successfully")

                return True

            except TimeoutException:
                logger.warning("⚠️ Add Version modal not found or took too long to load.")
                return False

            except Exception as e:
                logger.error("❌ Error while adding version", exc_info=True)
                return False

        except Exception as e:
            print("Error during clicking Add Call Version",e)
            logger.error("Error during clicking Add Call Version",e)
            Screenshot.take(f"Add_Call_Version_Clicked")


