from pages.base_page import BasePage
from pages.process.category.locators import VersionPageLocators as L

class VersionPage(BasePage):

    def click_add_category_button(self):
        self.click(L.ADD_CATEGORY_VERSION_BTN)

    def enter_category_name(self, name):
        self.clear_and_type(L.CATEGORY_NAME_INPUT, name)

    def enter_category_weight(self, weight):
        self.clear_and_type(L.CATEGORY_WEIGHTAGE_INPUT, weight)

    def click_add_category(self):
        self.click(L.ADD_CATEGORY_BTN)

    def enter_question_code(self, code):
        self.clear_and_type(L.QUESTION_CODE_INPUT, code)

    def enter_question_text(self, text):
        self.clear_and_type(L.QUESTION_TEXT_INPUT, text)

    def select_rating_type(self, rating_type):
        dropdown = self.get_select(L.RATING_TYPE_SELECT)
        dropdown.select_by_visible_text(rating_type)

    def enter_question_weight(self, weight):
        self.clear_and_type(L.QUESTION_WEIGHTAGE_INPUT, weight)

    def click_add_question(self):
        self.click(L.ADD_QUESTION_BTN)

    def click_publish_button(self):
        self.click(L.PUBLISH_CATEGORY_VERSION_BTN)

    def click_back_button(self):
        self.click(L.BACK_BTN)
