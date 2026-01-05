from pages.common.loader import Loader
from pages.common.open_filter_search import FilterSearch
from pages.common.sidemenupage import SideMenuPage
from pages.common.submit_search_filter import SubmitFilterSearch
from pages.filtering.filter_record_by_attribute import FilterByAttribute
from pages.login.login import LoginPage
from pages.login.logout import Logout
from pages.record.record_manager import RecordManager
from pages.record.record_page import RecordPage


class RecordEndToEndFlow:

    def __init__(self, driver,full_cfg):

        self.login_page = LoginPage(driver)
        logout_page = Logout(driver)
        loader = Loader(driver)
        record_manager = RecordManager(driver)
        record_page = RecordPage(driver, full_cfg)
        filter_record = FilterByAttribute(driver)
        open_filter = FilterSearch(driver)
        filter_action = SubmitFilterSearch(driver)
        side_menu_page = SideMenuPage(driver)
