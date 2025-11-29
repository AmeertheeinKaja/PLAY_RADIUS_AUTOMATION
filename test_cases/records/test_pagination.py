import pytest
from selenium.webdriver.common.by import By

from pages.login.login import LoginPage
from pages.common.loader import Loader
from pages.pagination.pagination import Pagination
from utils.data_reader import load_test_data
from utils.screenshot import Screenshot

data = load_test_data("pagination/paginationData.json")["pagination"]


@pytest.mark.usefixtures("driver_function")
class TestPagination:

    def test_pagination_next(self, driver_function):
        """Verify that clicking NEXT moves to the next page."""

        login_page = LoginPage(driver_function)
        loader = Loader(driver_function)

        # Step 1: Login
        login_page.open()
        login_page.login()
        loader.load()

        # Step 2: Open All Records page (taken from JSON in future)


        pagination = Pagination(driver_function)

        # JSON expected value
        expected_increment = data["next_page"]["expected_increment"]

        # Step 3: Capture current page
        initial_page = pagination.get_current_page()

        # Step 4: Click NEXT
        pagination.go_to_next()
        new_page = pagination.get_current_page()

        try:
            assert new_page == initial_page + expected_increment, \
                f"Expected page {initial_page + expected_increment}, but got {new_page}"
        except AssertionError as e:
            Screenshot.take(driver_function, "pagination_next_failed")
            raise e

    @pytest.mark.parametrize("case", data["actions"])
    def test_pagination_all(self, driver_function, case):

        login_page = LoginPage(driver_function)
        loader = Loader(driver_function)
        pagination = Pagination(driver_function)

        # Step 1: Login
        login_page.open()
        login_page.login()
        loader.load()

        # Step 2: Open page


        # Capture initial page (if needed)
        initial_page = pagination.get_current_page()

        action = case["action"]

        if action == "next":
            pagination.go_to_next()
            assert pagination.get_current_page() == initial_page + case["expectedChange"]

        elif action == "previous":
            pagination.go_to_previous()
            assert pagination.get_current_page() == initial_page + case["expectedChange"]

        elif action == "first":
            pagination.go_to_page(case["pageNumber"])
            assert pagination.get_current_page() == case["expectedPage"]

        elif action == "last":
            total=pagination.get_total_pages()
            pagination.go_to_page(total)
            assert pagination.get_current_page() >= 1  # At least page 1

        elif action == "goto":
            pagination.go_to_page(case["pageNumber"])
            assert pagination.get_current_page() == case["expectedPage"]



        else:
            raise ValueError(f"Unknown action: {action}")