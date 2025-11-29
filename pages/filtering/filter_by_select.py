from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from pages.base_page import BasePage
from pages.common.loader import Loader
from utils.logger import get_logger
from utils.data_reader import load_test_data
from utils.screenshot import Screenshot

# data = load_test_data("filterData.json")

data = load_test_data("filter/filterData.json")

logger = get_logger(__name__)

class FilterBySelect(BasePage):
    CHANNEL_FIELD = (By.XPATH, "//select[@id='attributeValue_channel']")
    INTERACTION_FIELD = (By.XPATH, "//select[@id='attributeValue_xsesstype']")

    def __init__(self, driver):
        super().__init__(driver)
        self.loader = Loader(driver)
        self.channel = data.get("Channel", "")
        self.interaction = data.get("Interaction Type", "")

    def select_dropdown(self, locator, value, label):

        if not value:
            logger.warning(f"No value provided for {label}. Skipping.")
            return

        try:
            self.loader.load()
            dropdown = self.wait_until_visible(locator)

            logger.info(f"{label} dropdown visible")
            logger.info(f"Selecting {label}: {value}")

            Select(dropdown).select_by_value(value)

            logger.info(f"Successfully selected {label}: {value}")

        except NoSuchElementException:
            logger.error(f"{label} '{value}' NOT found in dropdown!", exc_info=True)
            Screenshot.take(self.driver,f"{label}_dropdown_error")


        except Exception as e:
            logger.error(f"Unexpected error selecting {label}: {value}", exc_info=True)
            Screenshot.take(self.driver, f"{label}_unexpected_error")

    def channelSearch(self, channel_value=None):
        value = channel_value or self.channel
        self.select_dropdown(self.CHANNEL_FIELD, value, "Channel")

    def interactionSearch(self, interaction_value=None):
        value = interaction_value or self.interaction
        self.select_dropdown(self.INTERACTION_FIELD, value, "Interaction Type")

    def get_selected_value(self, filter_name):
        # Works for Channel / Interaction Type
        dropdown = self.wait_until_visible(
            (By.XPATH, f"//label[text()='{filter_name}']/following::select[1]")
        )
        return Select(dropdown).first_selected_option.text.strip()