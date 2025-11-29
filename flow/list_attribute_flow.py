from pages.record_attributes.list_attributes.edit_list_attribute import EditListAttribute
from pages.record_attributes.list_attributes.enable_list_attribute import EnableListAttribute
from pages.record_attributes.list_attributes.validate_list_attribute import ValidateListAttribute

from utils.data_reader import load_test_data
from utils.logger import get_logger

logger = get_logger(__name__)

data = load_test_data("filter/list_attribute.json")


class ListAttributeFlow:

    def __init__(self, driver):
        self.editor = EditListAttribute(driver)
        self.enabler = EnableListAttribute(driver)
        self.validator = ValidateListAttribute(driver)
        self.expected_list = data["enable_attributes"]

    def enable_missing_attributes(self):
        logger.info("Preparing to enable missing list attributes...")

        self.editor.open_edit()
        self.enabler.enable()

        logger.info("Missing attributes enabled successfully.")

    def assert_attributes_enabled(self):
        errors = []

        for attr in self.expected_list:
            if not self.validator.is_attribute_enabled(attr):
                errors.append(attr)

        if errors:
            raise AssertionError(
                f"The following attributes are NOT enabled as expected: {errors}"
            )