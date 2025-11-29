import pytest

from flow.filter_flow import FilterFlow
from flow.list_attribute_flow import ListAttributeFlow
from pages.login.login import LoginPage
from pages.common.loader import Loader
from pages.common.sidemenupage import SideMenuPage
from pages.login.logout import Logout

from pages.login.logout import Logout
from utils.screenshot import Screenshot
from utils.logger import get_logger

logger = get_logger(__name__)


@pytest.mark.usefixtures("driver_function")
class TestListAttributeConfiguration:
    def test_list_attributes(self, driver_function):
        driver = driver_function

        login = LoginPage(driver)
        menu = SideMenuPage(driver)
        flow = ListAttributeFlow(driver)
        logout = Logout(driver)

        login.open()
        login.login()

        menu.config()
        flow.enable_missing_attributes()

        # 🔥 Assertion here
        flow.assert_attributes_enabled()

        menu.record()
        logout.logout()





