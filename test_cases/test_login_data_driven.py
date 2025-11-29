import time

import pytest
from pages.login.login import LoginPage
from utils.data_reader import load_test_data

# Load test data
data = load_test_data("test_invalidLogin.json")


@pytest.mark.usefixtures("driver_function")
class TestLoginPage:

    @pytest.mark.parametrize("case", data["invalid_cases"])
    def test_invalid_login(self, driver_function, case):
        """Test invalid login scenarios."""
        login_page = LoginPage(driver_function)
        login_page.open()
        login_page.login(case["username"], case["password"])

        if case["expected"] == "disabled":
            # Login button should be disabled
            is_enabled = driver_function.find_element(*LoginPage.LOGIN_BTN).is_enabled()
            assert not is_enabled, "Login button should be disabled for empty credentials."
        else:
            # Check for error message
            error_text = login_page.get_error_message()
            assert case["expected"] in error_text, \
                f"Expected '{case['expected']}', but got '{error_text}'"

    @pytest.mark.parametrize("case", data["valid_cases"])
    def test_valid_login(self, driver_function, case):
        """Test valid login scenarios."""
        login_page = LoginPage(driver_function)
        login_page.open()
        print(f"🔹 Running case: {case['case']} with user '{case['username']}'")

        login_page.login(case["username"], case["password"])
        login_page.wait_until_visible(login_page.DASHBOARD_UI)

        expected_string = case["expected"]
        current_url = driver_function.current_url
        assert expected_string in current_url, f"Expected '{expected_string}', but got '{current_url}'"
        print(f" Passed case: {case['case']}")

