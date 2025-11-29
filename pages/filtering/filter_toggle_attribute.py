from selenium.webdriver.common.by import By

from utils.logger import get_logger

from utils.screenshot import Screenshot



logger = get_logger(__name__)
from utils.data_reader import load_test_data

data = load_test_data("filter/DataAttributeFilter.json")
filter_data = data["active"]  # Only active filters


class FilterToggleAttribute:

    # Only the toggles we support
    filter_toggle = ["Rating", "Transcript", "Sentiment", "IsBye"]

    def __init__(self, driver):
        self.driver = driver

    def set_toggle_by_name(self, attribute_name):
        try:
            # Click the LABEL, not the hidden input
            label_xpath = f"//label[@for='flexSwitch_{attribute_name}']"

            toggle_label = self.driver.find_element(By.XPATH, label_xpath)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", toggle_label)
            toggle_label.click()

            # Verify actual checkbox state
            checkbox = self.driver.find_element(By.ID, f"flexSwitch_{attribute_name}")
            state = checkbox.is_selected()

            logger.info(f"✔ Toggle applied → {attribute_name}: {state}")
            print(f"✔ Toggle applied → {attribute_name}: {state}")

        except Exception as e:
            logger.error(f"❌ Failed to toggle {attribute_name}: {e}")
            print(f"❌ Failed to toggle {attribute_name}: {e}")

    def apply_active_toggles(self):
        """Enable only the toggles listed in JSON under 'active'"""

        for key, value in filter_data.items():

            # Check only toggle filters
            if key in self.filter_toggle:

                # If value is True → toggle ON
                if value is True:
                    print(f"→ Setting toggle ON for: {key}")
                    logger.info(f"→ Setting toggle ON for: {key}")
                    self.set_toggle_by_name(key)

                else:
                    print(f"→ Skipping (false/off): {key}")
                    logger.info(f"→ Skipping (false/off): {key}")

    def apply_toggle(self, name, should_enable):
        checkbox = self.driver.find_element(By.ID, f"flexSwitch_{name}")
        current = checkbox.is_selected()

        # If state already correct → do nothing
        if current == should_enable:
            logger.info(f"⏭ Toggle already in correct state → {name}: {should_enable}")
            return

        # Click label to change state
        self.set_toggle_by_name(name)
