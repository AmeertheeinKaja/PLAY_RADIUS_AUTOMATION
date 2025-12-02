import pytest

from pages.login.login import LoginPage
from pages.login.logout import Logout
from utils.logger import get_logger

logger = get_logger(__name__)

@pytest.mark.usefixtures("driver_function")
class TestLogout:
    def test_logout_successful(self,driver_function):
        """Verify that login is successful and redirected to expected URL."""
        try:
            login_page = LoginPage(driver_function)
            logout_page = Logout(driver_function)
            login_page.open()
            login_page.login()
            logout_page.logout()






            assert "Login" in logout_page.title


            logger.info(f" Logout successful")


        except AssertionError as ae:
            logger.error(f" Assertion failed: {ae}")
            pytest.fail(str(ae))

        except Exception as e:
            logger.error(f" Unexpected error during logout: {e}")
            pytest.fail(f"Unexpected error during logout: {e}")