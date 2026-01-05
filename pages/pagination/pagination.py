from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.common.loader import Loader
from utils.logger import get_logger

logger = get_logger()

class Pagination(BasePage):

    CURRENT_PAGE = (By.CSS_SELECTOR, "ul.pagination li.active a")
    NEXT_BTN = (By.CSS_SELECTOR, "ul.pagination span.icon-pagination-right")
    PREV_BTN = (By.CSS_SELECTOR, "ul.pagination span.icon-pagination-left")
    PAGE_NUMBERS = (By.CSS_SELECTOR, "ul.pagination li.rgp_btn a")

    def __init__(self, driver):
        super().__init__(driver)
        self.loader = Loader(driver)

    def get_current_page(self):
        return int(self.wait_until_present(self.CURRENT_PAGE).text.strip())

    def go_to_next(self):
        next_btn = self.wait_until_clickable(self.NEXT_BTN)
        next_btn.click()
        self.loader.load()

    def go_to_previous(self):
        prev_btn = self.wait_until_clickable(self.PREV_BTN)
        prev_btn.click()
        self.loader.load()

    def go_to_page(self, page_number):
        pages = self.find_elements(self.PAGE_NUMBERS)

        for page in pages:
            if page.text.strip() == str(page_number):

                page.click()
                self.loader.load()
                return

        raise Exception(f"Page {page_number} not found on pagination bar")

        raise Exception(f"Page {page_number} not found on pagination bar")

    def loop_all_pages(driver):
        pagination = Pagination(driver)

        total_pages = 598  # You can extract programmatically also

        for page in range(1, total_pages + 1):
            pagination.go_to_page(page)
            print(f"Now on page {pagination.get_current_page()}")

    def get_total_pages(self):
        # ".rec_count span" returns text like "1/598"
        footer_el = self.wait_until_visible((By.CSS_SELECTOR, ".rec_count span"))
        footer_text = footer_el.text.strip()

        current, total = footer_text.split("/")
        total = int(total.strip())

        per_page = 20
        return (total + per_page - 1) // per_page  # ceil division

    def is_next_page_disabled(self):
        try:
            btn = self.wait_until_present(self.NEXT_BTN)

            if not btn.is_enabled():
                return True

            classes = btn.get_attribute("class").lower()
            if "disabled" in classes:
                return True

            return False

        except Exception:
            return True
