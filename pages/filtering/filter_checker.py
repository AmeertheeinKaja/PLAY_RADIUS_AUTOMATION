from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import get_logger
from selenium.common.exceptions import StaleElementReferenceException
from utils.data_reader import load_test_data
from utils.screenshot import Screenshot

data = load_test_data("filter/DataAttributeFilter.json")


class FilterChecker(BasePage):
    FILTER_LOCATORS = {
        "Rating": (By.XPATH, "//span[normalize-space(text())='Rating']"),
        "Transcript": (By.XPATH, "//span[normalize-space(text())='Transcript']"),
        "Sentiment": (By.XPATH, "//span[normalize-space(text())='Sentiment']"),
        "IsBye": (By.XPATH, "//span[normalize-space(text())='IsBye']"),
        "Record ID": (By.ID, "attributeValue_recordId"),
        "Process Code": (By.ID, "attributeValue_campaign"),
        "Process Name": (By.ID, "attributeValue_processName"),
        "Interaction ID": (By.ID, "attributeValue_xsessid"),
        "Channel": (By.ID, "attributeValue_channel"),
        "Interaction Type": (By.ID, "attributeValue_xsesstype"),
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
        "Session Time": (By.XPATH, "//label[text()='Session Time']"),
        "Ring Time": (By.XPATH, "//label[text()='Ring Time']"),
        "Talk Time": (By.XPATH, "//label[text()='Talk Time']"),
        "Wrapup Time": (By.XPATH, "//label[text()='Wrapup Time']"),
    }

    def __init__(self, driver):
        super().__init__(driver)
        self.logger = get_logger(__name__)


    def get_available_filters(self):
        available_filters = []
        TIMEOUT = 1

        self.logger.info("--- Checking Filter Availability ---")

        for name, locator in self.FILTER_LOCATORS.items():
            try:
                if self.check_element_presence(locator, timeout=TIMEOUT):
                    available_filters.append(name)
                    self.logger.info(f"✅ FOUND: {name}")
                else:
                    self.logger.warning(f"❌ MISSING: {name}")
            except StaleElementReferenceException:
                self.logger.warning(f"⚠️ Retrying due to stale element: {name}")
                if self.check_element_presence(locator, timeout=TIMEOUT):
                    available_filters.append(name)

        self.logger.info("------------------------------------")
        self.logger.info(f"Available filters: {available_filters}")
        return available_filters

    def is_filter_available(self, filter_name):
        locator = self.FILTER_LOCATORS.get(filter_name)
        if locator is None:
            raise ValueError(f"Filter name '{filter_name}' is not defined in the locator dictionary.")
        return self.check_element_presence(locator, timeout=2)

    def get_missing_active_filters(self):
        """
        Checks which filters defined as 'active' in DataAttributeFilter.json
        are missing or not visible in the UI.
        Returns the list of missing active filters.
        """
        try:
            active_filters = data.get("active", {})
            active_keys = list(active_filters.keys())

            self.logger.info(f"🔍 Expected active filters from JSON: {active_keys}")

            missing_filters = []

            for filter_name in active_keys:
                if not self.is_filter_available(filter_name):
                    missing_filters.append(filter_name)
                    self.logger.warning(f"❌ Missing active filter in UI: {filter_name}")
                else:
                    self.logger.info(f"✅ Active filter visible in UI: {filter_name}")

            self.logger.info(f"🚫 Missing active filters: {missing_filters}")
            return missing_filters

        except Exception as e:
            self.logger.error(f"Error while checking missing active filters: {str(e)}")
            return []


