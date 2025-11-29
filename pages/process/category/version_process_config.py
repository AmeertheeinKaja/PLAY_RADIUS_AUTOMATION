from selenium.common import TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

import time
from pages.base_page import BasePage

from utils.count_manager import get_next_process_number
from utils.logger import get_logger
from utils.data_reader import load_test_data

from utils.screenshot import Screenshot

data = load_test_data("questionDataNew.json")
versiondata=load_test_data("versionData.json")


from pages.loader import Loader
from pages.OpenProcess import OpenProcess

# from testdata.createProcessData import process_code,process_Name,review_rating,channel


logger = get_logger()


class VersionProcessConfig(BasePage):

    CATEGORY_BASIC = (By.XPATH, "//button[@title='Close']")
    ADD_CATEGORY_VERSION_BTN = (By.XPATH, "//button[@title='Add Category/Edit Version']")
    EDIT_CATEGORY_VERSION_BTN=(By.XPATH, "//*[@id='root']/div[2]/div/div[3]/div/div/div[2]/div/div[2]/div/div[1]/div/div/div[2]/div[2]/div[1]/button")
    PUBLISH_CATEGORY_VERSION_BTN = (By.XPATH, "//button[@title='Publish Version']")
    DELETE_CATEGORY_VERSION_BTN = (By.XPATH, "//button[@title='Delete Version']")
    EDIT_VERSION_NAME = (By.XPATH, "//input[@name='versionName']")
    CATEGORY_NAME_INPUT = (By.XPATH, "//input[@name='categoryName']")
    CATEGORY_WEIGHTAGE_INPUT = (By.XPATH, "//div[@class='plver_box_header']//input[@name='weightage']")
    ADD_CATEGORY_BTN = (By.XPATH, "//span[@title='Add Category']")
    QUESTION_CODE_INPUT= (By.XPATH, "//input[@name='questionCode']")
    QUESTION_TEXT_INPUT = (By.XPATH, "//input[@name='questionText']")
    RATING_TYPE_SELECT = (By.XPATH, "//Select[@name='answerType']")
    QUESTION_WEIGHTAGE_INPUT = (By.XPATH, "//div[@class='plver_box_body']//input[@name='weightage']")
    ADD_QUESTION_BTN = (By.XPATH, "//button[@title='Add Question']")
    EDIT_QUESTION = (By.XPATH, "//button[@title='Edit']")
    DELETE_QUESTION = (By.XPATH, "//button[@title='Delete']")
    BACK_BTN = (By.XPATH, "//button[@title='Back']")
    VERSION_NAME_EDIT_BTN=(By.XPATH,"//button[@title='Edit Version/Category/Question']")
    VERSION_NAME_CLOSE_BTN = (By.XPATH, "//div[@class='items']//button[@title='Close']")
    VERSION_NAME_SAVE_BTN = (By.XPATH, "//button[@title='Save']")
    MODAL_SAVE_BTN = (By.XPATH, "//button[text()='Save Anyway']")
    MODAL_CANCEL_BTN=(By.XPATH, "//button[@title='Cancel']")
    MODAL_PUBLISH_BTN=(By.XPATH,"//button[text()='Publish']")






    def __init__(self, driver):
        super().__init__(driver)
        self.data = load_test_data("questionDataNew.json")
        self.categories = self.data.get("categories", [])
        self.version_name = versiondata.get("versionName")

    def click_edit_version_name_btn(self):
        self.click(self.VERSION_NAME_EDIT_BTN)

    def enter_version_name(self, new_name):
        self.clear_and_type(self.EDIT_VERSION_NAME, new_name)

    def click_save_version(self):
        self.click(self.VERSION_NAME_SAVE_BTN)

    def click_cancel_version(self):
        self.click(self.VERSION_NAME_CLOSE_BTN)

    def edit_version_name(self, new_name):
        try:
            self.click_edit_version_name_btn()
            self.enter_version_name(new_name)
            self.click_save_version()
            logger.info("Version name Updated")
            Screenshot.take(self.driver,f"Version name updated")
            return True
        except Exception as e:
            logger.error(f"Error editing version name: {e}", exc_info=True)
            return False





    def add_all_categories(self):
        """Loops through all categories in the JSON and adds them sequentially."""

        add_category_btn = self.wait_until_clickable(self.ADD_CATEGORY_VERSION_BTN)
        add_category_btn.click()
        logger.info("Clicked Add Category/Edit Version button")
        try:
            for category in self.categories:
                logger.info(f"🟢 Adding category: {category['categoryName']}")
                self.addCategory(category)
                time.sleep(1)  # Small delay between categories
            logger.info("✅ All categories added successfully.")
            return True
        except Exception as e:
            logger.error(f"Error adding categories: {e}", exc_info=True)
            return False

    def addCategory(self, category):
        """Adds a single category and its questions."""
        try:
            # 1️⃣ Click "Add Category/Edit Version"


            # 2️⃣ Enter Category Name
            category_name_input = self.wait_until_present(self.CATEGORY_NAME_INPUT)
            category_name_input.clear()
            category_name_input.send_keys(category["categoryName"])
            logger.info(f"Entered Category Name: {category['categoryName']}")

            # 3️⃣ Enter Category Weightage
            category_weight_input = self.wait_until_present(self.CATEGORY_WEIGHTAGE_INPUT)
            category_weight_input.clear()
            category_weight_input.send_keys(category["categoryWeight"])
            logger.info(f"Entered Category Weightage: {category['categoryWeight']}")

            # 4️⃣ Add all questions for this category
            for q in category["questions"]:
                self.addQuestion(
                    code=q["questionCode"],
                    text=q["question"],
                    rating_type=q["questionType"],
                    weightage=q["questionWeight"]
                )
                logger.info(f"Added question: {q['questionCode']} - {q['question']}")

            # 5️⃣ Click Add Category button (to finalize this category)
            add_category_final = self.wait_until_clickable(self.ADD_CATEGORY_BTN)
            add_category_final.click()
            logger.info(f"✅ Category '{category['categoryName']}' saved successfully.")

            # 6️⃣ Handle modal (Save Anyway)
            try:
                modal_locator = (By.XPATH,
                                 "//div[@role='dialog' and contains(@class,'modal') and contains(@class,'show')]")
                self.wait_until_clickable(modal_locator)

                modal_save_btn = self.wait_until_clickable(self.MODAL_SAVE_BTN)
                modal_save_btn.click()
                self.wait_invisible(modal_locator)
                logger.info("Modal Save Anyway clicked.")

            except TimeoutException:
                logger.warning("⚠️ Modal not found — continuing.")

            # ✅ Wait before adding the next category
            time.sleep(1)
            return True

        except Exception as e:
            logger.error(f"Error adding category '{category.get('categoryName', 'Unknown')}': {e}", exc_info=True)
            return False

    # --- 1. Fix the original addQuestion method (NO LOOP HERE) ---
    def addQuestion(self, code, text, rating_type, weightage):
        """Adds a single question to the latest category."""
        try:
            # 1. Enter Question Code
            question_code = self.wait_until_present(self.QUESTION_CODE_INPUT)
            question_code.clear()
            question_code.send_keys(code)  # Use the passed 'code' parameter

            # 2. Enter Question Text
            question_text = self.wait_until_present(self.QUESTION_TEXT_INPUT)
            question_text.clear()
            question_text.send_keys(text)  # Use the passed 'text' parameter

            # 3. Select Rating Type (FIX: Use select_by_visible_text)
            question_type_dropdown = Select(self.wait_until_clickable(self.RATING_TYPE_SELECT))
            question_type_dropdown.select_by_visible_text(rating_type)
            logger.info(f"Selected question type: {rating_type}")

            # 4. Enter Question Weightage
            question_weight = self.wait_until_present(self.QUESTION_WEIGHTAGE_INPUT)
            question_weight.clear()
            question_weight.send_keys(weightage)

            # 5. Click Add Question button
            self.wait_until_clickable(self.ADD_QUESTION_BTN).click()
            logger.info(f"Clicked Add Question button for code: {code}.")
            time.sleep(1)

            return True
        except Exception as e:
            logger.error(f"Error adding question '{code}': {e}", exc_info=True)
            return False




    def publish_version(self):

        back_button=self.wait_until_clickable(self.BACK_BTN)
        back_button.click()

        publish_button=self.wait_until_clickable(self.PUBLISH_CATEGORY_VERSION_BTN)
        publish_button.click()

        try:
            # Wait for modal to appear
            modal_locator = (By.XPATH,
                             "//div[@role='dialog' and contains(@class,'modal') and contains(@class,'show')]")
            self.wait_until_clickable(modal_locator)

            modal_save_btn = self.wait_until_clickable(self.MODAL_PUBLISH_BTN)
            modal_save_btn.click()

            logger.info(f"Version {self.version_name} published successfully.")
            Screenshot.take( f"click_error_{self.version_name}")

            time.sleep(2)

            self.wait_invisible(modal_locator)

            # Wait for modal to disappear

            return True

        except TimeoutException:
            logger.warning("⚠️ Import Version modal not found or took too long to load.")
            return False



