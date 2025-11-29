from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.common.loader import Loader
from utils.data_reader import load_test_data
from utils.screenshot import Screenshot

data = load_test_data("sorting\\sortData.json")


class SortingColumn(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.loader = Loader(driver)


    def sort_column(self, column_name, order="asc"):

        if order == "asc":
            icon = "icon-up-arrow"
        else:
            icon = "icon-down-arrow"

        locator = (
            By.XPATH,
            f"//span[@class='th_cell_name' and normalize-space(text())='{column_name}']"
            "/following-sibling::div"
            f"//span[contains(@class,'{icon}')]"
        )

        element = self.wait_until_clickable(locator)
        element.click()
        self.loader.load()
        Screenshot.take(self.driver, f"sorted_{column_name}_{order}")

