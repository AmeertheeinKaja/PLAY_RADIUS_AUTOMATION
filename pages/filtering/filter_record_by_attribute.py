import time
from selenium.webdriver.common.by import By
from selenium.common import NoSuchElementException
from selenium.webdriver.support.select import Select

from pages.filtering.filter_by_select import FilterBySelect
from pages.filtering.filter_toggle_attribute import FilterToggleAttribute
from pages.base_page import BasePage
from pages.filtering.filter_checker import FilterChecker
from pages.record_attributes.edit_filter_attribute import EditFilterAttribute
from pages.record_attributes.enable_filter_attribute import EnableFilterAttribute
from pages.common.sidemenupage import SideMenuPage

from pages.common.open_filter_search import FilterSearch
from utils.logger import get_logger
from utils.data_reader import load_test_data
from pages.filtering.time_range_filter import TimeRangeFilter
from utils.screenshot import Screenshot

data = load_test_data("filter/DataAttributeFilter.json")
filter_data=data["active"]

logger = get_logger(__name__)

FILTER_LOCATORS = {
    "Record ID": (By.ID, "attributeValue_recordId"),
    "Process Code": (By.ID, "attributeValue_campaign"),
    "Process Name": (By.ID, "attributeValue_processName"),
    "Interaction ID": (By.ID, "attributeValue_xsessid"),
    "Contact Address": (By.ID, "attributeValue_contactaddress"),
    "Caller ID": (By.ID, "attributeValue_callerid"),
    "Dialed ID": (By.ID, "attributeValue_dialedid"),
    "Start At From": (By.ID, "attributeValue_startat_from"),
    "Start At To": (By.ID, "attributeValue_startat_to"),
    "End At From": (By.ID, "attributeValue_endat_from"),
    "End At To": (By.ID, "attributeValue_endat_to"),
    "Interaction Status": (By.ID, "attributeValue_xsessstatus"),
    "Connection ID": (By.ID, "attributeValue_xconnid"),
    "Connection Type": (By.ID, "attributeValue_xconntype"),
    "User Address": (By.ID, "attributeValue_address"),
    "User ID": (By.ID, "attributeValue_agentid"),
    "User Name": (By.ID, "attributeValue_agentname"),
    "Cause": (By.ID, "attributeValue_xsesscause"),
    "Hold Duration": (By.ID, "attributeValue_holdduration"),
    "Interaction Action": (By.ID, "attributeValue_xsessaction"),
    "Disposition": (By.ID, "attributeValue_disposition"),
    "Contact ID": (By.ID, "attributeValue_contactid"),


}
PARENT_FILTER_MAPPING = {
    "Start At From": "Start At",
    "Start At To": "Start At",
    "End At From": "End At",
    "End At To": "End At",
}
BOOLEAN_FILTER_LOCATORS = {
    "Rating": (By.ID, "flexSwitch_Rating"),
    "Transcript": (By.ID, "flexSwitch_Transcript"),
    "Sentiment": (By.ID, "flexSwitch_Sentiment"),
    "IsBye": (By.ID, "flexSwitch_IsBye")
}
SELECT_FILTER_LOCATORS = {
    "Channel":"Channel",
    "Interaction Type":"Interaction Type"
}
TIME_SLIDER_LOCATORS={
    "Session Time":"Session Time",
    "Wrapup Time":"Wrapup Time",
    "Talk Time":"Talk Time",
    "Ring Time":"Ring Time"
}

class FilterByAttribute(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.filter_checker = FilterChecker(driver)
        self.edit_filter = EditFilterAttribute(driver)
        self.enable_filter = EnableFilterAttribute(driver)
        self.sidemenu = SideMenuPage(driver)
        self.filter_search = FilterSearch(driver)
        self.toggle = FilterToggleAttribute(driver)
        self.select_attr=FilterBySelect(driver)
        self.time_slider=TimeRangeFilter(driver)


    def filter(self):
        for name, value in filter_data.items():
            self.search(name, value)

    def ensure_filter_enabled(self, filter_name):
        """Enable a specific filter if it is not visible."""
        try:
            locator = (
                By.XPATH,
                f"//div[contains(@class,'filter-parent')]//span[text()='{filter_name}']"
            )
            self.wait_until_visible(locator, timeout=2)
            return True  # Already enabled
        except:
            # Not enabled, enable it
            logger.info(f"Filter '{filter_name}' is not enabled. Enabling now...")

            # Enable only the required filter
            self.sidemenu.config()
            self.edit_filter.edit()
            self.enable_filter.enable([filter_name])

            # Return back to records page
            self.sidemenu.record()
            return True

    def enable_missing(self):
        """Find and enable missing filters, then refresh UI."""
        try:
            # STEP 1: Identify missing filters
            self.missing_filters = self.filter_checker.get_missing_active_filters()
            logger.info(f"DEBUG STEP 1: Filters returned from checker: {self.missing_filters}")

            if not self.missing_filters:
                logger.info("No missing active filters found.")
                self.filter()  # <-- ADD THIS
                return True

            # STEP 2: Map child filters to parent filters
            mapped = {PARENT_FILTER_MAPPING.get(f, f) for f in self.missing_filters}
            self.missing_filters = list(mapped)
            logger.info(f"⚙️ Final filters to enable (Mapped): {self.missing_filters}")

            # STEP 3: Open configuration UI
            self.sidemenu.config()

            # STEP 4: Edit configuration UI
            self.edit_filter.edit()

            # STEP 5: Enable filters
            self.enable_filter.enable( self.missing_filters)

            # STEP 6: Refresh UI after enabling
            self.sidemenu.record()
            self.filter_search.filter()



            # for name, value in filter_data.items():
            #     self.search(name, value)
            #     logger.info(f"DEBUG STEP 2: Filters returned from checker: {name,value}")


            logger.info("✅ Missing filters enabled and UI refreshed successfully.")
            return True

        except Exception as e:
            logger.error(f"❌ Error in enabling missing filters: {str(e)}", exc_info=True)
            raise

    def search(self, filter_name, filter_value):
        try:
            logger.info(f"🔍 Checking filter availability for: {filter_name}")
            logger.info(f"DEBUG STEP 3: Checking filter availability for: {filter_name}")

            # 1️⃣ HANDLE BOOLEAN FILTERS FIRST
            if filter_name in BOOLEAN_FILTER_LOCATORS:
                logger.info(f"🟦 Applying toggle filter → {filter_name}: {filter_value}")
                self.toggle.apply_toggle(filter_name, filter_value)
                logger.info(f"🟦 Toggle applied successfully for {filter_name}")
                return

            # 2️⃣ MAP PARENT FILTERS
            parent_filter_name = PARENT_FILTER_MAPPING.get(filter_name, filter_name)

            if filter_name in SELECT_FILTER_LOCATORS:
                if filter_name == "Interaction Type":
                    self.select_attr.interactionSearch(filter_value)
                    return

                elif filter_name == "Channel":
                    self.select_attr.channelSearch(filter_value)
                    return

            if filter_name in TIME_SLIDER_LOCATORS:
                self.time_slider.set_slider_range(filter_name, "lower", filter_value)
                return  # ← IMPORTANT
            # if filter_name in TIME_SLIDER_LOCATORS:
            #     if filter_name=="Session Time":
            #         self.time_slider.set_slider_range("Session Time","lower",filter_value)
            #     elif filter_name=="Talk Time":
            #         self.time_slider.set_slider_range("Talk Time","lower",filter_value)
            #     elif filter_name=="Wrapup Time":
            #         self.time_slider.set_slider_range("Wrapup Time","lower",filter_value)
            #     elif filter_name=="Ring Time":
            #         self.time_slider.set_slider_range("Ring Time","lower",filter_value)

            # 3️⃣ VALIDATE LOCATOR EXISTS
            if filter_name not in FILTER_LOCATORS:
                raise KeyError(f"No locator found for filter '{filter_name}'")

            # 4️⃣ HANDLE NORMAL FILTERS
            filter_locator = FILTER_LOCATORS[filter_name]
            filter_input = self.wait_until_visible(filter_locator)
            filter_input.clear()

            DATE_FILTERS = ["Start At From", "Start At To", "End At From", "End At To"]

            if filter_name in DATE_FILTERS:
                self.driver.execute_script(
                    "arguments[0].value = arguments[1];", filter_input, filter_value
                )
                self.driver.execute_script("""
                    arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                    arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
                    arguments[0].dispatchEvent(new Event('blur', { bubbles: true }));
                """, filter_input)

                logger.info(f"📅 Date set for filter {filter_name}: {filter_value}")
                return

            # 5️⃣ DEFAULT VALUE FOR NORMAL INPUTS
            filter_input.send_keys(filter_value)
            logger.info(f"✏️ Entered '{filter_value}' in {filter_name}")

        except Exception as e:
            logger.error(f"Error handling filter '{filter_name}' with value '{filter_value}': {e}", exc_info=True)



