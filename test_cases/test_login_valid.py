import pytest
from pages.login.login import LoginPage
from utils.read_properties import ReadConfig


@pytest.mark.usefixtures("driver_function")
class TestLoginPage:

    def test_valid_login(self, driver_function):
        """Verify that a user can log in with valid credentials."""
        login_page = LoginPage(driver_function)
        login_page.open()

        login_page.login()  # Uses default credentials from ReadConfig

        # You can assert the expected post-login UI or URL
        assert "/recording-list/all-records" in driver_function.current_url or \
               driver_function.find_elements(*LoginPage.DASHBOARD_UI), \
               "Login failed or Dashboard not loaded after valid credentials."

    @pytest.mark.parametrize("username,password", [
        ("wronguser", "wrongpass"),
        ("", "somepass"),
        ("valid_user", "")
    ])
    def test_invalid_login(self, driver_function, username, password):
        """Verify invalid login scenarios."""
        login_page = LoginPage(driver_function)
        login_page.open()
        login_page.login(username=username, password=password)

        login_btn = driver_function.find_element(*LoginPage.LOGIN_BTN)
        assert not login_btn.is_enabled(), "Login button should be disabled for empty credentials."
        print("✅ Login button is disabled as expected for empty inputs.")

    def test_empty_credentials(self, driver_function):
        """Verify that login button is disabled when username/password are empty."""
        login_page = LoginPage(driver_function)
        login_page.open()

        login_page.login(username="", password="")

        login_btn = driver_function.find_element(*LoginPage.LOGIN_BTN)
        assert not login_btn.is_enabled(), "Login button should be disabled for empty credentials."
        print("✅ Login button is disabled as expected for empty inputs.")



