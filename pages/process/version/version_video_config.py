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

class VersionVideoConfig(BasePage):

    VIDEO_VERSION_ACCORD = (By.XPATH, "//button[@id='video_version_accord']")
    IMPORT_VIDEO_VERSION = (By.XPATH, "//ul[@id='menuv_video']//button[@title='Import Version']")
    COPY_VIDEO_VERSION = (By.XPATH, "//ul[@id='menuv_video']//button[@title='Copy Version']")
    ADD_VIDEO_VERSION = (By.XPATH, "//ul[@id='menuv_video']//button[@title='Add Version']")
    VERSION_NAME = (By.XPATH, "//input[@name='name']")
    VERSION_INTERACTION = (By.XPATH, "//select[@name='interaction']")
    SUBMIT_BUTTON = (By.XPATH, "//button[normalize-space()='Submit']")
    CANCEL_BUTTON = (By.XPATH, "//button[@id='addVersionClose']")
    VERSION_PROCESS_NAME = (By.XPATH, "//select[@name='selProcess']")
    VERSION_VERSION = (By.XPATH, "//select[@name='selVersion']")
    VERSION_CPY_VERSION = (By.XPATH, "//select[@name='cpyVersion']")

    VERSION_CPY_VERSION_NAME = (By.XPATH, "//input[@name='cpyVrsnname']")
    ERROR_TEXT="Version name already exist in this process for channel video"


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

    def get_version_tab(self):
        return (By.XPATH, f"//ul//li//span[@title='{self.version_name}']")

    def video_version_accord(self):
        try:
            video_version_accord=self.wait_until_clickable(self.VIDEO_VERSION_ACCORD)
            video_version_accord.click()
            self.wait_until_clickable(self.VIDEO_VERSION_ACCORD)

            print("Video Version Accord Clicked")
            logger.info("Video Version Accord Clicked")

        except Exception as e:
            print("Error during clicking Video Version Accord",e)
            logger.error("Error during clicking Video Version Accord",e)

    def open_version(self):
        try:
            # self.video_version_accord()
            version_tab = self.wait_until_clickable(self.get_version_tab())
            version_tab.click()
            logger.info(f"Opened version tab for {self.version_name}")
            Screenshot.take( f"Opened_Version_Tab_{self.version_name}")
        except Exception as e:
            logger.error("Error opening version tab: %s", e)


    def import_video_version(self):
        try:
            import_video_version=self.wait_until_clickable(self.IMPORT_VIDEO_VERSION)
            import_video_version.click()
            self.wait_until_clickable(self.IMPORT_VIDEO_VERSION)

            print("Import email Version Clicked")
            logger.info("Import email Version Clicked")

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
            print("Error during clicking Import Video Version",e)
            logger.error("Error during clicking Import Video Version",e)

    def copy_video_version(self):
        try:
            copy_video_version=self.wait_until_clickable(self.COPY_VIDEO_VERSION)
            copy_video_version.click()
            self.wait_until_clickable(self.COPY_VIDEO_VERSION)

            print("Copy Video Version Clicked")
            logger.info("Copy Video Version Clicked")
            Screenshot.take(f"Copy_Video_Version_Clicked")

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
                Screenshot.take(f"Copy_Video_Version_Modal_Closed_Successfully")

                return True

            except TimeoutException:
                logger.warning("⚠️ Copy Version modal not found or took too long to load.")
                return False

            except Exception as e:
                logger.error("❌ Error while copying version", exc_info=True)
                return False


        except Exception as e:
            print("Error during clicking Copy Video Version",e)
            logger.error("Error during clicking Copy Video Version",e)
            Screenshot.take(f"Copy_Video_Version_Clicked")

    def add_video_version(self):
        try:
            add_video_version=self.wait_until_clickable(self.ADD_VIDEO_VERSION)
            add_video_version.click()
            self.wait_until_clickable(self.ADD_VIDEO_VERSION)

            print("Add Video Version Clicked")
            logger.info("Add Video Version Clicked")
            Screenshot.take(f"Add_video_Version_Clicked")

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
                self.submit()

                # driver.execute_script("arguments[0].click();", submit_button)
                logger.info("Clicked Submit button on version modal.")

                status=self.capture_toast()
                if status in self.ERROR_TEXT:
                    self.cancel()



                self.wait_invisible(modal_locator)

                # Wait for modal to disappear

                logger.info("Add Version modal closed successfully.")
                Screenshot.take(f"Add_Video_Version_Modal_Closed_Successfully")

                return True

            except TimeoutException:
                logger.warning("⚠️ Add Version modal not found or took too long to load.")
                return False

            except Exception as e:
                logger.error("❌ Error while adding version", exc_info=True)
                return False

        except Exception as e:
            print("Error during clicking Add Video Version",e)
            logger.error("Error during clicking Add Video Version",e)
            Screenshot.take(f"Add_Video_Version_Clicked")

    def submit(self):
        submit_button = self.wait_until_clickable(self.SUBMIT_BUTTON)
        submit_button.click()

        # driver.execute_script("arguments[0].click();", submit_button)
        logger.info("Clicked Submit button on version modal.")
    def cancel(self):
        cancel_btn = self.wait_until_clickable(self.CANCEL_BUTTON)
        cancel_btn.click()
        logger.info("Clicked Cancel button on version modal.")

