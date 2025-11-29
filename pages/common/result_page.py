from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By


class ResultPage:
    ROWS = (By.XPATH, "//table[contains(@class,'rad_grid_table')]//tbody/tr")
    NO_DATA_CELL = (By.XPATH, "//*[@id='pills-allrec']//td[contains(text(),'No records found')]")

    def __init__(self, driver):
        self.driver = driver

    def get_first_row(self):
        # Example table xpath. Adjust to your UI.
        return self.driver.find_element(By.XPATH, "//table/tbody/tr[1]")

    def is_value_present(self, row, column_name, expected_value):
        # column_name to column index mapping (dynamic or fixed)
        col_index = self.get_column_index(column_name)

        cell = row.find_element(By.XPATH, f"td[{col_index}]")
        return expected_value.lower() in cell.text.lower()

    def get_column_index(self, column_name):
        headers = self.driver.find_elements(By.XPATH, "//table/thead/tr/th")
        for i, header in enumerate(headers, start=1):
            if column_name.lower() in header.text.lower():
                return i
        raise Exception(f"Column '{column_name}' not found!")


    def get_row_count(self):
        rows = self.driver.find_elements(*self.ROWS)
        return len(rows)

    def is_no_data(self):
        try:
            return self.driver.find_element(*self.NO_DATA_CELL).is_displayed()
        except NoSuchElementException:
            return False