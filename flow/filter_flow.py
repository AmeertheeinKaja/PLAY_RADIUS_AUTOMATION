from pages.common.open_filter_search import FilterSearch
from pages.common.result_page import ResultPage
from pages.common.submit_search_filter import SubmitFilterSearch
from pages.filtering.filter_record_by_attribute import FilterByAttribute


class FilterFlow:
    def __init__(self, driver):
        self.filter_search = FilterSearch(driver)
        self.filter_attribute = FilterByAttribute(driver)
        self.action_filter = SubmitFilterSearch(driver)
        self.result_page = ResultPage(driver)
        self.filter_data = {}

    def apply_filters(self):
        self.filter_search.filter()                 # open filter panel
        self.filter_attribute.enable_missing()      # enable missing
        self.filter_attribute.filter()              # apply values
        self.action_filter.searchFilter()
        self.filter_attribute.filter()
        self.action_filter.clearFilter()

    def validate_after_search(self):
        # reopen filter again and submit again if needed
        self.filter_search.filter()
        self.action_filter.searchFilter()
        return True

    def is_result_matching(self):
        row = self.result_page.get_first_row()

        for key, value in self.filter_data.items():
            if not self.result_page.is_value_present(row, key, value):
                return False

        return True

    def apply_multiple_filters(self, filters: dict):
        for field, value in filters.items():
            self.filter_attribute.search(field, value)
        self.action_filter.searchFilter()