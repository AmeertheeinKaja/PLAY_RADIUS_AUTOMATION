# pages/version/version_modal.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from pages.base_page import BasePage
from utils.logger import get_logger
from utils.counter_manager import get_next_process_number

logger = get_logger()


class VersionModal(BasePage):

    # Modal root
    MODAL = (By.XPATH, "//div[@role='dialog' and contains(@class,'modal') and contains(@class,'show')]")

    # Common modal fields
    PROCESS_DROPDOWN = (By.XPATH, "//select[@name='selProcess']")
    VERSION_DROPDOWN = (By.XPATH, "//select[@name='selVersion']")
    COPY_VERSION_DROPDOWN = (By.XPATH, "//select[@name='cpyVersion']")
    INTERACTION_DROPDOWN = (By.XPATH, "//select[@name='interaction']")
    VERSION_NAME_INPUT = (By.XPATH, "//input[@name='name']")
    COPY_VERSION_NAME_INPUT = (By.XPATH, "//input[@name='cpyVrsnname']")
    SUBMIT_BUTTON = (By.XPATH, "//button[normalize-space()='Submit']")
    CANCEL_BUTTON = (By.XPATH, "//button[@id='addVersionClose']")
    ERROR_TOAST_TEXT="Version name already exist in this process for channel call"
    SUCCESS_TOAST_IMPORT_TEXT="Version imported successfully"
    SUCCESS_TOAST_COPY_TEXT = "Version copied successfully"
    SUCCESS_TOAST_ADD_TEXT = "Version saved successfully"

    def __init__(self, driver):
        super().__init__(driver)
        self.last_toast=None

    # ---------------------------
    # MODAL HANDLERS
    # ---------------------------

    def wait_for_modal(self):
        """Wait until modal appears"""
        self.wait_until_visible(self.MODAL)
        logger.info("Modal opened.")

    def wait_for_modal_close(self):
        """Wait until modal disappears"""
        self.wait_invisible(self.MODAL)
        logger.info("Modal closed.")

    # ---------------------------
    # FIELD ACTIONS
    # ---------------------------

    def select_process(self, process_name):
        dropdown = Select(self.wait_until_clickable(self.PROCESS_DROPDOWN))
        dropdown.select_by_visible_text(process_name)
        logger.info(f"Selected process: {process_name}")

    def select_version(self, version_name):
        dropdown = Select(self.wait_until_clickable(self.VERSION_DROPDOWN))
        dropdown.select_by_visible_text(version_name)
        logger.info(f"Selected version: {version_name}")

    def select_copy_version(self, version_name):
        dropdown = Select(self.wait_until_clickable(self.COPY_VERSION_DROPDOWN))
        dropdown.select_by_visible_text(version_name)
        logger.info(f"Selected copy version: {version_name}")

    def select_interaction(self, interaction_code):
        dropdown = Select(self.wait_until_clickable(self.INTERACTION_DROPDOWN))
        dropdown.select_by_value(interaction_code)
        logger.info(f"Selected interaction: {interaction_code}")

    def enter_version_name(self, name):
        inp = self.wait_until_visible(self.VERSION_NAME_INPUT)
        inp.clear()
        inp.send_keys(name)
        logger.info(f"Entered version name: {name}")

    def enter_copy_version_name(self, name):
        inp = self.wait_until_visible(self.COPY_VERSION_NAME_INPUT)
        inp.clear()
        inp.send_keys(name)
        logger.info(f"Entered copy version name: {name}")

    # ---------------------------
    # BUTTON ACTIONS
    # ---------------------------
    def toast_text(self):
        toast_text = self.capture_toast()
        self.last_toast = toast_text  # Store the value
        logger.info(f"Captured Toast: {toast_text}")
        return toast_text

    def submit(self):
        self.wait_until_clickable(self.SUBMIT_BUTTON).click()
        logger.info("Submit clicked.")
        return self.toast_text()

    def cancel(self):
        self.wait_until_clickable(self.CANCEL_BUTTON).click()
        logger.info("Cancel clicked.")


    def fill(self, data: dict):
        """
        Fills modal fields based on dictionary keys.
        Supports optional fields & different modal types.
        """
        if "process_name" in data:
            self.select_process(data["process_name"])

        if "version" in data:
            # Could be import version OR copy version
            try:
                self.select_version(data["version"])
            except:
                try:
                    self.select_copy_version(data["version"])
                except:
                    pass

        if "interaction" in data:
            self.select_interaction(data["interaction"])

        if "name" in data:
            # Could be version creation or copy name
            try:
                self.enter_version_name(data["name"]+ str(get_next_process_number()))
            except:
                try:
                    self.enter_copy_version_name(data["name"]+ str(get_next_process_number()))
                except:
                    pass

        logger.info(f"Modal filled with data: {data}")
