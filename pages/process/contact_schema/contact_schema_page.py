import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from pages.base_page import BasePage
from utils.logger import get_logger
from pages.common.loader import Loader

from utils.data_reader import load_test_data
from utils.screenshot import Screenshot

data = load_test_data("contact_schema.json")

logger = get_logger(__name__)
class ContactSchema(BasePage):

    TAB_CONTACT_SCHEMA=(By.XPATH,"//*[@id='accordionExample']/ul/ul[4]/li/button/span[2]")
    AUTO_MODE_RADIO = (By.XPATH, "//input[@value='auto']")
    MANUAL_MODE_RADIO = (By.XPATH, "//input[@value='manual']")
    SAVE_BTN=(By.XPATH,"//button[@title='Save']")
    CANCEL_BTN=(By.XPATH,"//button[@title='Cancel']")
    CLOSE_BTN=(By.XPATH,"//button[@title='Close']")
    REMOVE_ATTRIBUTE=(By.XPATH,"//button[@title='Remove']")
    ADD_ATTRIBUTE = (By.XPATH, "//button[@title='Add']")
    EDIT_BTN = (By.XPATH, "//button[@title='Edit']")
    NAME_INPUT=(By.XPATH,"//input[@name='name_1']")
    SELECT_INPUT=(By.XPATH,"//select[@name='dataType_1']")
    ATTRIBUTE_ROWS = (By.XPATH, "//tr[contains(@class,'custom-attribute-row')]")

    def __init__(self, driver):
        super().__init__(driver)
        self.loader = Loader(driver)
        self.mode=data['mode']
        self.field_list = data.get("fields", [])

    def tab_contact_schema(self):
        tab_contact_schema=self.wait_until_clickable(self.TAB_CONTACT_SCHEMA)
        tab_contact_schema.click()
        self.loader.load()
        logger.info("contact schema tab selected")
        Screenshot.take(self.driver,f"Contact schema tab")

    def choose_mode(self):
        if self.mode and self.mode.lower() == 'manualmode':
            mode_locator = self.MANUAL_MODE_RADIO
            mode_name = "Manual Mode"
        elif self.mode and self.mode.lower() == 'automode':
            mode_locator = self.AUTO_MODE_RADIO
            mode_name = "Auto Mode"
        else:
            logger.warning(f"Conversion mode '{self.mode}' not recognized or missing. Defaulting to Manual Mode.")
            mode_locator = self.MANUAL_MODE_RADIO
            mode_name = "Manual Mode (Defaulted)"
        self.driver.find_element(*mode_locator).click()
        logger.info(f"Selected Conversion Mode: {mode_name}")
        Screenshot.take(self.driver,f"Selected Conversion Mode: {mode_name}")
        self.loader.load()



    def save_contact(self):
        """Clicks the Save button."""
        save_btn = self.wait_until_clickable(self.SAVE_BTN)
        save_btn.click()
        logger.info("Save button clicked.")
        Screenshot.take(self.driver,f"Contact schema save")

    def edit_contact(self):
        """Clicks the Save button."""
        edit_btn = self.wait_until_clickable(self.EDIT_BTN)
        edit_btn.click()
        logger.info("Edit button clicked.")
        Screenshot.take(self.driver,f"Contact schema save")
    def cancel_contact(self):
        """Clicks the Cancel button."""
        cancel_btn = self.wait_until_clickable(self.CANCEL_BTN)
        cancel_btn.click()
        logger.info("Cancel button clicked.")

    def close_contact(self):
        """Clicks the Close button."""
        close_btn = self.wait_until_clickable(self.CLOSE_BTN)
        close_btn.click()
        logger.info("Close button clicked.")

    def add_attribute_field(self):
        logger.info("Adding a new attribute row...")
        add_btn = self.driver.find_element(By.XPATH, "//button[@title='Add']")
        add_btn.click()

    def delete_attribute_field(self):
        remove_btn = self.wait_until_clickable(self.REMOVE_ATTRIBUTE)
        remove_btn.click()

    def get_name_input(self, index):
        return (By.XPATH, f"//input[@name='name_{index}']")

    def get_type_select(self, index):
        return (By.XPATH, f"//select[@name='dataType_{index}']")

    def add_name(self,name):
        name_input = self.wait_until_clickable(self.NAME_INPUT)
        name_input.clear()
        name_input.send_keys(name)
        logger.info(f"Name input: {name_input}")

    def add_data_type(self,datatype):
        data_type_dropdown = Select(self.wait_until_clickable(self.SELECT_INPUT))
        data_type_dropdown.select_by_visible_text(datatype)
        logger.info(f"Selected question type: {datatype}")

    def add_attribute(self):
        total_fields = len(self.field_list)

        for index, field in enumerate(self.field_list, start=1):

            # dynamic locators
            name_locator = (By.XPATH, f"//input[@name='name_{index}']")
            type_locator = (By.XPATH, f"//select[@name='dataType_{index}']")

            # name
            name_input = self.wait_until_clickable(name_locator)
            name_input.clear()
            name_input.send_keys(field["fieldName"])
            logger.info(f"Entered field name: {field['fieldName']}")

            # datatype
            data_type_dropdown = Select(self.wait_until_clickable(type_locator))
            data_type_dropdown.select_by_visible_text(field["dataType"])
            logger.info(f"Selected data type: {field['dataType']}")

            # 🔥 Only click Add if NOT the last field
            if index < total_fields:
                add_btn = self.wait_until_clickable(self.ADD_ATTRIBUTE)
                add_btn.click()
                logger.info("Added new empty row")

        # finally save
        self.save_contact()

    def get_existing_row_count(self):
        rows = self.driver.find_elements(
            By.XPATH, "//div[contains(@class,'row') and contains(@class,'gx-2')][.//input[contains(@name,'name_')]]"
        )

        count = 0
        for row in rows:
            name_input = row.find_element(By.XPATH, ".//input[contains(@name,'name_')]")
            if name_input.get_attribute("value").strip():
                count += 1

        logger.info(f"[EXISTING ROW COUNT] {count}")
        return count

    def get_total_rows(self):
        rows = self.driver.find_elements(
            By.XPATH, "//div[contains(@class,'row') and contains(@class,'gx-2')][.//input[contains(@name,'name_')]]"
        )
        logger.info(f"[ROW COUNT] Found {len(rows)} rows")
        return len(rows)

    def delete_attribute(self):
        self.delete_attribute_field()

    def delete_last_attribute_field(self):
        remove_buttons = self.driver.find_elements(By.XPATH, "//button[@title='Remove']")
        if remove_buttons:
            remove_buttons[-1].click()  # delete LAST one

    def delete_last_empty_row(self):
        rows = self.driver.find_elements(
            By.XPATH, "//div[contains(@class,'row') and contains(@class,'gx-2')][.//input[contains(@name,'name_')]]"
        )

        for row in rows[::-1]:
            name_input = row.find_element(By.XPATH, ".//input[contains(@name,'name_')]")
            if not name_input.get_attribute("value").strip():
                remove_button = row.find_element(By.XPATH, ".//button[@title='Remove']")
                remove_button.click()
                logger.info("Removed last empty row.")
                break

    def remove_empty_rows(self):
        rows = self.driver.find_elements(By.XPATH, "//tr[contains(@class,'custom-attribute-row')]")

        for row in rows:
            name_input = row.find_element(By.XPATH, ".//input[contains(@name,'name_')]")
            if not name_input.get_attribute("value").strip():
                row.find_element(By.XPATH, ".//button[@title='Remove']").click()
                logger.info("[REMOVE EMPTY ROW] Deleted an empty row.")

    def edit_attribute(self):
        self.edit_contact()
        self.loader.load()

        required_rows = len(self.field_list)
        logger.info(f"[START EDIT] Required JSON rows: {required_rows}")

        # 1. Count rows currently visible on UI
        existing_rows_ui = self.get_total_rows()
        logger.info(f"[UI ROWS] Existing rows on UI: {existing_rows_ui}")

        # 2. How many NEW rows to add?
        rows_to_add = required_rows
        logger.info(f"[ADD REQUIRED] Need to add {rows_to_add} new rows")

        # 3. Add rows (stable loop)
        for i in range(rows_to_add):
            logger.info(f"[ADD] Adding row {i + 1}/{rows_to_add}")
            self.add_attribute_field()
            time.sleep(0.3)

        # 4. Now fill ONLY the newly-added rows
        start_index = existing_rows_ui + 1
        end_index = existing_rows_ui + required_rows

        logger.info(f"[UPDATE RANGE] Updating rows {start_index} to {end_index}")

        json_index = 0
        for row_index in range(start_index, end_index + 1):
            field = self.field_list[json_index]
            json_index += 1

            logger.info(f"[UPDATE] Row {row_index} → {field}")

            name_locator = self.get_name_input(row_index)
            type_locator = self.get_type_select(row_index)

            # update name
            name_input = self.wait_until_clickable(name_locator)
            name_input.clear()
            name_input.send_keys(field["fieldName"])

            # update datatype
            dropdown = Select(self.wait_until_clickable(type_locator))
            dropdown.select_by_visible_text(field["dataType"])

        # 5. Save
        logger.info("[SAVE]")
        self.save_contact()
        Screenshot.take(self.driver,f"Attribut Saved")

    def delete_attribute_by_name(self, attribute_name):

        self.edit_contact()
        self.loader.load()
        """
        Locates and clicks the Remove button for a specific attribute row 
        based on the field name.
        """
        # Compound XPath to find the remove button inside the row that contains the input with the given value.
        DELETE_BUTTON_LOCATOR = (
            By.XPATH,
            f"//input[@value='{attribute_name}']/ancestor::div[contains(@class, 'row gx-2')]//button[@title='Remove']"
        )

        logger.info(f"Attempting to delete attribute: {attribute_name}")

        try:
            remove_btn = self.wait_until_clickable(DELETE_BUTTON_LOCATOR)
            remove_btn.click()
            logger.info(f"Successfully deleted attribute: {attribute_name}")
            Screenshot.take(self.driver, f"Deleted attribute {attribute_name}")
        except Exception as e:
            logger.error(f"Failed to find or click the remove button for attribute '{attribute_name}': {e}")
            raise

        logger.info("[SAVE]")
        self.save_contact()
        Screenshot.take(self.driver, f"Attribut Saved")
        self.capture_toast()
        Screenshot.take(self.driver, f"Attribut Saved")
