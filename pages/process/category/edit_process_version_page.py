import time
from selenium.common.exceptions import (
    TimeoutException,
    StaleElementReferenceException,
    ElementClickInterceptedException,
)
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import get_logger
from utils.data_reader import load_test_data
from utils.screenshot import Screenshot

data = load_test_data("updateCategory.json")
logger = get_logger()


class EditProcessVersionPage(BasePage):
    MODAL_OK_BTN = (By.XPATH, "//button[text()='Ok']")
    MODAL_CANCEL_BTN = (By.XPATH, "//button[text()='Cancel']")

    def __init__(self, driver, timeout=10):
        super().__init__(driver)
        self.timeout = timeout

        categories_list = data.get("categories", [])

        if categories_list:
            target = categories_list[0]
            self.categoryName = target.get("categoryName")        # new name
            self.categoryWeight = target.get("categoryWeight")    # new weight
        else:
            self.categoryName = None
            self.categoryWeight = None

        self.old_name = data.get("oldCategoryName")               # dynamic old name

    # --------------------------
    # 🟦 Dynamic Locators
    # --------------------------
    def edit_btn(self, name):
        return (
            By.XPATH,
            f"//span[@title='{name}']/ancestor::div[@class='plver_box_headerin']//button[@title='Edit']"
        )

    def delete_btn(self, name):
        return (
            By.XPATH,
            f"//span[@title='{name}']/ancestor::div[@class='plver_box_headerin']//button[@title='Delete']"
        )

    def tab_category(self, name):
        return (
            By.XPATH,
            f"//span[@title='{name}']/ancestor::div[@class='plver_box_headerin']"
        )

    def category_name_input(self, name):
        return (
            By.XPATH,
            f"//input[@value='{name}']"
        )

    def category_weight_input(self, name):
        return (
            By.XPATH,
            f"//input[@value='{name}']/ancestor::div[@class='title_editable']//input[@placeholder='Enter Weightage']"
        )

    def save_btn(self, name):
        return (
            By.XPATH,
            f"//input[@value='{name}']/ancestor::div[@class='plver_box_headerin']//button[@title='Save']"
        )

    def close_btn(self, name):
        return (
            By.XPATH,
            f"//input[@value='{name}']/ancestor::div[@class='plver_box_headerin']//button[@title='Close']"
        )

    # --------------------------
    # 🟩 Utility JS click
    # --------------------------
    def js_click(self, locator):
        element = self.wait_until_visible(locator)
        self.driver.execute_script("arguments[0].click();", element)

    # --------------------------
    # 🟧 MAIN METHOD FOR EDITING CATEGORY
    # --------------------------
    def edit_category(self):
        try:
            logger.info(f"🔍 Searching Edit button for category: {self.old_name}")

            # 1️⃣ CLICK EDIT BUTTON
            edit_button_locator = self.edit_btn(self.old_name)
            element = self.wait_until_visible(edit_button_locator)

            # scroll + JS click (stable)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)

            self.driver.execute_script("arguments[0].click();", element)

            logger.info("✔ JS click on category Edit button successful.")
            time.sleep(2)  # allow DOM to update

            # 2️⃣ CATEGORY NAME INPUT
            input_name_locator = self.category_name_input(self.old_name)
            input_name = self.wait_until_visible(input_name_locator)
            logger.info("✔ Category name input visible")

            # clear using JS (more stable)
            self.driver.execute_script("arguments[0].value='';", input_name)
            input_name.send_keys(self.categoryName)
            logger.info(f"✔ Updated category name to: {self.categoryName}")

            # 3️⃣ WEIGHT INPUT
            weight_input_locator = self.category_weight_input(self.old_name)
            weight_input = self.wait_until_visible(weight_input_locator)

            self.driver.execute_script("arguments[0].value='';", weight_input)
            weight_input.send_keys(self.categoryWeight)
            logger.info(f"✔ Updated weight to: {self.categoryWeight}")

            # 4️⃣ SAVE BUTTON
            save_btn_locator = self.save_btn(self.old_name)
            save_btn = self.wait_until_visible(save_btn_locator)

            self.driver.execute_script("arguments[0].click();", save_btn)
            logger.info("💾 Category saved successfully.")

            time.sleep(2)

        except Exception as e:
            logger.error(f"❌ Could not edit category: {e}")
            raise

    def delete_category(self):
        try:
            logger.info(f"Searching Delete button for category: {self.old_name}")

            # 1️⃣ Locate delete button dynamically
            delete_button_locator = self.delete_btn(self.old_name)
            delete_btn = self.wait_until_visible(delete_button_locator)

            # Scroll + JS click
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", delete_btn)
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", delete_btn)

            logger.info("Delete button clicked successfully")
            time.sleep(1)

            try:
                # Wait for modal to appear
                modal_locator = (By.XPATH,
                                 "//div[@role='dialog' and contains(@class,'modal') and contains(@class,'show')]")
                self.wait_until_clickable(modal_locator)

                modal_save_btn = self.wait_until_clickable(self.MODAL_OK_BTN)
                modal_save_btn.click()

                logger.info(f"Version {self.old_name} category deleted successfully.")
                Screenshot.take(self.driver,f"click_error_{self.old_name}")

                time.sleep(2)

                self.wait_invisible(modal_locator)

                # Wait for modal to disappear

                return True

            except TimeoutException:
                logger.warning("⚠️ Import Version modal not found or took too long to load.")
                return False

            # 2️⃣ Handle confirmation popup (if present)
            try:
                confirm_locator = (By.XPATH, "//button[contains(text(),'Yes') or contains(text(),'Confirm')]")
                confirm_btn = self.wait_until_visible(confirm_locator)
                self.driver.execute_script("arguments[0].click();", confirm_btn)
                logger.info("Delete confirmation clicked")
            except TimeoutException:
                logger.warning("No confirmation popup found. Continuing.")

            logger.info("Category deleted successfully")
            time.sleep(2)

        except Exception as e:
            logger.error(f"Could not delete category: {e}")

            # Capture screenshot on failure
            try:
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                screenshot_path = f"screenshots/delete_category_error_{timestamp}.png"
                self.driver.save_screenshot(screenshot_path)
                logger.error(f"Screenshot saved at: {screenshot_path}")
            except:
                logger.error("Failed to capture screenshot")

            raise
