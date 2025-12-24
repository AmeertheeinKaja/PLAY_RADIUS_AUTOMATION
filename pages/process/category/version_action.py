import time
from selenium.common import TimeoutException

from pages.process.category.version_page import VersionPage
from pages.process.category.locators import VersionPageLocators as L
from utils.data_reader import load_test_data
from utils.logger import get_logger
from utils.screenshot import Screenshot

logger = get_logger()
# data=load_test_data()

class VersionActions(VersionPage):

    def __init__(self, driver,categories):
        super().__init__(driver)
        self.categories = categories
        # self.data = load_test_data("questionDataNew.json")
        # self.categories = self.data.get("categories", [])
        self.version_name = load_test_data("versionData.json").get("versionName")

    def add_question(self, q):
        self.enter_question_code(q["questionCode"])
        self.enter_question_text(q["question"])
        self.select_rating_type(q["questionType"])
        self.enter_question_weight(q["questionWeight"])
        self.click_add_question()

    def add_category(self, category):
        self.enter_category_name(category["categoryName"])
        self.enter_category_weight(category["categoryWeight"])

        for q in category["questions"]:
            self.add_question(q)

        self.click_add_category()
        time.sleep(1)

    def add_all_categories(self):
        self.click_add_category_button()

        for c in self.categories:
            logger.info(f"Adding category: {c['categoryName']}")
            self.add_category(c)

        logger.info("All categories added.")

    def publish_version(self):
        self.click_back_button()
        self.click_publish_button()

        try:
            modal = self.wait_until_present(L.MODAL_PUBLISH_BTN)
            modal.click()
            logger.info("Version published")
            Screenshot.take(self.driver, "Published_version")
            return True
        except TimeoutException:
            return False
