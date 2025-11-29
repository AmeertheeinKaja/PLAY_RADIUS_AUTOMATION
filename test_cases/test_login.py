import pytest

from pages.login.login import LoginPage
from utils.logger import get_logger

logger = get_logger(__name__)

@pytest.mark.usefixtures("driver_session")
class TestLogin:
    def test_login_successful(self,driver_session):
        """Verify that login is successful and redirected to expected URL."""
        try:
            login_page = LoginPage(driver_session)
            login_page.open()
            login_page.login()


            expected_substring = "/recording-list/all-records"
            current_url = driver_session.current_url


            assert expected_substring in current_url, (
                f"Login failed: Expected '{expected_substring}' in URL, got '{current_url}'"
            )

            logger.info(f" Login successful: {current_url}")


        except AssertionError as ae:
            logger.error(f" Assertion failed: {ae}")
            pytest.fail(str(ae))

        except Exception as e:
            logger.error(f" Unexpected error during login: {e}")
            pytest.fail(f"Unexpected error during login: {e}")