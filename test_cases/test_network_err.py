import pytest
from pages.login.login import LoginPage
from utils.read_properties import ReadConfig
from utils.logger import get_logger
logger = get_logger(__name__)

@pytest.mark.usefixtures("driver_function")
class TestNetworkError:

    def test_login_network_error(self, driver_function):
        login_page = LoginPage(driver_function)
        login_page.open()

        # Intentionally invalid input
        login_page.login()

        # Force click the login button even if disabled


        # Read network error
        network_msg = login_page.get_network_error()
        logger.info(network_msg)


        assert network_msg == "Network Error", \
            f"Expected 'Network Error', but got '{network_msg}'"


