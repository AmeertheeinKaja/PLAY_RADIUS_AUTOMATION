from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import get_logger
from utils.screenshot import Screenshot

logger = get_logger(__name__)


class DashboardPage(BasePage):
    TAB_ALLRECORDS = (By.XPATH, "//button[@id='pills-allrec-tab']")
    TAB_CLOSED_RECORDS = (By.XPATH, "//button[@id='pills-closedrec-tab']")
    TAB_BULK_RECORDS = (By.XPATH, "//button[@id='pills-bulkdwnld-tab']")

    TAB_MAP = {
        "allrecords": TAB_ALLRECORDS,
        "closedrecords": TAB_CLOSED_RECORDS,
        "bulkdownload": TAB_BULK_RECORDS
    }

    def __init__(self, driver):
        super().__init__(driver)

    def open_tab(self, tab_name: str):
        """Generic method to open any dashboard tab by name."""
        tab_name = tab_name.lower().strip()

        if tab_name not in self.TAB_MAP:
            raise ValueError(f"Invalid tab name: {tab_name}. Choose from {list(self.TAB_MAP.keys())}")

        try:
            tab_locator = self.TAB_MAP[tab_name]
            tab_element = self.wait_until_clickable(tab_locator)
            tab_element.click()
            logger.info(f"Entered '{tab_name}' tab successfully.")

            # Take screenshot
            Screenshot.take(self.driver, f"{tab_name}_page")
            self.wait_for_page_load()

        except Exception as e:
            logger.error(f" Failed to open '{tab_name}' tab: {e}")
            raise

    # Optional: convenience wrappers if you still want explicit methods
    def open_all_records(self):
        self.open_tab("allrecords")

    def open_closed_records(self):
        self.open_tab("closedrecords")

    def open_bulk_download(self):
        self.open_tab("bulkdownload")
