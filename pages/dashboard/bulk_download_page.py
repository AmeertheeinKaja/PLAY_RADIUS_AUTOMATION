from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from pages.base_page import BasePage
from utils.logger import get_logger
from utils.screenshot import Screenshot
from utils.data_reader import load_test_data


data = load_test_data("bulkDownloadData.json")

logger = get_logger(__name__)

class BulkDownloadPage(BasePage):


    SELECT_PROCESS=(By.XPATH,"//select[@name='campaign']")
    SELECT_CHANNEL=(By.XPATH,"//select[@name='channel']")
    TEXT_USERID=(By.XPATH,"//input[@id='agentid']")
    TEXT_CONTACT_ADDRESS=(By.XPATH,"//input[@id='contactaddress']")
    START_FROM=(By.XPATH,"//input[@id='from']")
    START_TO=(By.XPATH,"//input[@id='to']")
    SEARCH_BUTTON=(By.XPATH,"//button[@title='Search']")
    DOWNLOAD_BUTTON=(By.XPATH,"//button[@title='Download Zip']")
    RESET_BUTTON=(By.XPATH,"//button[@title='Reset']")

    def __init__(self, driver):
        super().__init__(driver)
        self.process_code = data.get('processCode', '')
        self.channel = data.get('channel', '')
        self.userId = data.get('userId', '')
        self.contactAddress = data.get('contactAddress', '')
        self.start_from = data.get('start_From', '')
        self.start_to = data.get('start_To', '')

    def search_bulk_records(self):
        try:
            # Select process
            if self.process_code:
                process_dropdown = Select(self.wait_until_clickable(self.SELECT_PROCESS))
                process_dropdown.select_by_visible_text(self.process_code)

            # Select channel
            if self.channel:
                channel_dropdown = Select(self.wait_until_clickable(self.SELECT_CHANNEL))
                channel_dropdown.select_by_visible_text( self.channel)

            # Fill text fields
            if self.userId:
                self.send_keys(self.TEXT_USERID, self.userId)

            if self.contactAddress:
                self.send_keys(self.TEXT_CONTACT_ADDRESS, self.contactAddress)

            if self.start_from:
                self.set_date_via_js(self.START_FROM, self.start_from)

            if self.start_to:
                self.set_date_via_js(self.START_TO, self.start_to)

            # Click Search
            self.click(self.SEARCH_BUTTON)
            Screenshot.take(self.driver, "bulk_download_search")
            logger.info("✅ Search executed successfully on Bulk Download page.")

        except Exception as e:
            logger.error(f"❌ Failed to search bulk records: {e}")
            Screenshot.take(self.driver, "bulk_download_search_error")
            raise

    def set_date_via_js(self, locator, date_value):
        """
        Safely sets date input values using JavaScript.
        This avoids issues with date pickers that block send_keys().
        """
        try:
            element = self.wait_until_visible(locator)
            self.driver.execute_script(
                "arguments[0].value = arguments[1];", element, date_value
            )
            self.driver.execute_script("""
                arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
                arguments[0].dispatchEvent(new Event('blur', { bubbles: true }));
            """, element)
            element.send_keys("\t")  # Optional: ensure blur triggers
            Screenshot.take(self.driver, f"Date_Set_{locator[1].split('[')[-1].split(']')[0]}")
            get_logger(__name__).info(f"✅ Set date for {locator[1]} to {date_value}")

        except Exception as e:
            get_logger(__name__).error(f"❌ Failed to set date for {locator[1]}: {e}")
            Screenshot.take(self.driver, f"Date_SetError_{locator[1]}")
            raise
