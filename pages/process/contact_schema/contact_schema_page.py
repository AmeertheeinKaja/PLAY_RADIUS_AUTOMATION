import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from pages.base_page import BasePage
from utils.logger import get_logger
from pages.common.loader import Loader

from utils.data_reader import load_test_data
from utils.screenshot import Screenshot



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
    ADD_SUCCESS_TEXT="Contact attributes saved successfully"
    ERROR_TEXT="Name field in these attributes is contains duplicate values"
    UPDATE_SUCCESS="Contact attributes updated successfully"



    def __init__(self, driver):
        super().__init__(driver)
        self.loader = Loader(driver)
        self.last_toast = None

    def configure_contact_schema(self, mode, field_list=None):
        """
        Configure Contact Schema based on mode.
        - Auto mode: only select mode & save
        - Manual mode: select mode, add attributes & save
        """

        self.choose_mode(mode)
        logger.info(f"configuring mode for {mode}")

        if mode and mode.lower() == "manualmode":
            if not field_list:
                raise ValueError("Field list is required for Manual Mode")

            logger.info("Manual mode selected → Adding attributes")
            self.add_attribute(field_list)

        elif mode and mode.lower() == "automode":
            logger.info("Auto mode selected → Skipping attribute creation")
            self.save_contact()

        else:
            raise ValueError(f"Unsupported contact schema mode: {mode}")

    def tab_contact_schema(self):
        tab_contact_schema=self.wait_until_clickable(self.TAB_CONTACT_SCHEMA)
        tab_contact_schema.click()
        self.loader.load()
        logger.info("contact schema tab selected")
        Screenshot.take(self.driver,f"Contact schema tab")

    def choose_mode(self, mode):
        if mode and mode.lower() == 'manualmode':
            mode_locator = self.MANUAL_MODE_RADIO
            mode_name = "Manual Mode"
        elif mode and mode.lower() == 'automode':
            mode_locator = self.AUTO_MODE_RADIO
            mode_name = "Auto Mode"
        else:
            logger.warning(f"Conversion mode '{mode}' not recognized or missing. Defaulting to Manual Mode.")
            mode_locator = self.MANUAL_MODE_RADIO
            mode_name = "Manual Mode (Defaulted)"

        self.driver.find_element(*mode_locator).click()
        logger.info(f"Selected Conversion Mode: {mode_name}")
        Screenshot.take(self.driver, f"Selected Conversion Mode: {mode_name}")
        self.loader.load()



    def save_contact(self):
        """Clicks the Save button."""
        save_btn = self.wait_until_clickable(self.SAVE_BTN)
        save_btn.click()
        self.toast_text()
        logger.info("Save button clicked.")
        Screenshot.take(self.driver,f"Contact schema save")

    def toast_text(self):
        toast_text = self.capture_toast()
        self.last_toast = toast_text  # Store the value
        logger.info(f"Captured Toast: {toast_text}")
        Screenshot.take(f"toast_{toast_text.replace(' ', '_')}")

        return toast_text

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

    def add_attribute(self,field_list):
        total_fields = len(field_list)

        for index, field in enumerate(field_list, start=1):

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

    def get_field_error(self, field_name):
        """
        field_name example: name_1, dataType_1
        """
        error_locator = (
            By.XPATH,
            f"//*[@name='{field_name}']/ancestor::div[contains(@class,'form-floating')]"
            "//div[contains(@class,'invalid-tooltip') and string-length(normalize-space())>0]"
        )
        return self.wait_until_visible(error_locator).text.strip()

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

    def edit_attribute(self, field_list):
        self.edit_contact()
        self.loader.load()

        required_rows = len(field_list)
        existing_rows = self.get_total_rows()

        logger.info(f"[EDIT] UI rows: {existing_rows}, JSON rows: {required_rows}")

        # 1️⃣ Update existing rows
        rows_to_update = min(existing_rows, required_rows)

        for index in range(1, rows_to_update + 1):
            field = field_list[index - 1]

            logger.info(f"[UPDATE] Row {index} → {field}")

            name_input = self.wait_until_clickable(self.get_name_input(index))
            name_input.clear()
            name_input.send_keys(field["fieldName"])

            dropdown = Select(self.wait_until_clickable(self.get_type_select(index)))
            dropdown.select_by_visible_text(field["dataType"])

        # 2️⃣ Add missing rows
        if required_rows > existing_rows:
            rows_to_add = required_rows - existing_rows
            logger.info(f"[ADD] Adding {rows_to_add} rows")

            for _ in range(rows_to_add):
                self.add_attribute_field()
                self.loader.load()

            for index in range(existing_rows + 1, required_rows + 1):
                field = field_list[index - 1]

                name_input = self.wait_until_clickable(self.get_name_input(index))
                name_input.clear()
                name_input.send_keys(field["fieldName"])

                dropdown = Select(self.wait_until_clickable(self.get_type_select(index)))
                dropdown.select_by_visible_text(field["dataType"])

        # 3️⃣ Delete extra rows
        if existing_rows > required_rows:
            rows_to_delete = existing_rows - required_rows
            logger.info(f"[DELETE] Removing {rows_to_delete} rows")

            for _ in range(rows_to_delete):
                self.delete_last_attribute_field()
                self.loader.load()

        # 4️⃣ Save
        self.save_contact()
        Screenshot.take(self.driver, "Attribute Edited & Saved")

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

    def set_field_value(self, index, field_name, datatype):
        name_input = self.wait_until_clickable(self.get_name_input(index))
        name_input.clear()
        name_input.send_keys(field_name)

        dropdown = Select(self.wait_until_clickable(self.get_type_select(index)))
        dropdown.select_by_visible_text(datatype)

    def add_empty_row(self):
        add_btn = self.wait_until_clickable(self.ADD_ATTRIBUTE)
        add_btn.click()
        self.loader.load()

    def insert_duplicate_field(self, field_name, datatype):
        self.edit_contact()
        self.loader.load()

        # add second row
        self.add_empty_row()

        # fill values using class level method
        self.set_field_value(index=2, field_name=field_name, datatype=datatype)

        # save to capture toast
        self.save_contact()
