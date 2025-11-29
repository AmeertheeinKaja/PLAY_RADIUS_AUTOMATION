import pytest
from selenium.webdriver.common.by import By

from pages.login.login import LoginPage
from pages.dashboard.dashboard_page import DashboardPage
from pages.common.loader import Loader

@pytest.mark.usefixtures("driver_function")
class TestDashboard:

    def test_bulk_download_tab(self, driver_function):
        login_page = LoginPage(driver_function)
        dashboard = DashboardPage(driver_function)
        loader = Loader(driver_function)

        # Step 1: Open login page and login
        login_page.open()
        login_page.login()

        # Step 2: Wait for loader if any
        loader.load()

        # Step 3: Open Bulk Download tab
        dashboard.open_bulk_download()

        # Step 4: Verify tab loaded
        assert "Bulk" in driver_function.page_source, "Bulk Download tab content not loaded properly."

    def test_open_all_records_tab(self, driver_function):
        login_page = LoginPage(driver_function)
        dashboard = DashboardPage(driver_function)
        loader = Loader(driver_function)

        login_page.open()
        login_page.login()
        loader.load()
        dashboard.open_all_records()

        assert "All Records" in driver_function.page_source or "Recording List" in driver_function.title, \
            "All Records tab content not loaded properly."

    def test_open_closed_records_tab(self, driver_function):
        login_page = LoginPage(driver_function)
        dashboard = DashboardPage(driver_function)
        loader = Loader(driver_function)

        login_page.open()
        login_page.login()
        loader.load()
        dashboard.open_closed_records()

        assert "Closed" in driver_function.page_source, "Closed Records tab content not loaded properly."

    def test_tab_switching(self, driver_function):
        login_page = LoginPage(driver_function)
        dashboard = DashboardPage(driver_function)
        loader = Loader(driver_function)

        login_page.open()
        login_page.login()
        loader.load()

        dashboard.open_all_records()
        dashboard.open_closed_records()
        dashboard.open_bulk_download()

        assert "Bulk" in driver_function.page_source, "Failed to switch tabs properly."

    def test_active_tab_highlight(self, driver_function):
        """Verify that the selected dashboard tab is highlighted with 'active' class."""
        login_page = LoginPage(driver_function)
        dashboard = DashboardPage(driver_function)
        loader = Loader(driver_function)

        # Step 1: Login
        login_page.open()
        login_page.login()
        loader.load()

        # Step 2: Open the 'Closed Records' tab
        dashboard.open_closed_records()

        # Step 3: Verify 'active' class applied to correct button
        active_tab = driver_function.find_element(By.CSS_SELECTOR, "button.ctp3_item_btn.active")
        active_tab_id = active_tab.get_attribute("id")

        assert "closedrec" in active_tab_id, (
            f"Active tab highlight not applied correctly. Found active tab id: {active_tab_id}"
        )
        print(f" Active tab highlight verified: {active_tab_id}")

    def test_loader_behavior_on_tab_change(self, driver_function):
        login_page = LoginPage(driver_function)
        dashboard = DashboardPage(driver_function)
        loader = Loader(driver_function)

        login_page.open()
        login_page.login()
        loader.load()

        dashboard.open_bulk_download()
        loader.load()  # Confirm loader disappears

    def test_invalid_tab_name_raises_error(self, driver_function):
        dashboard = DashboardPage(driver_function)
        with pytest.raises(ValueError, match="Invalid tab name"):
            dashboard.open_tab("random_tab")

    def test_dashboard_widgets_present(self, driver_function):
        login_page = LoginPage(driver_function)
        dashboard = DashboardPage(driver_function)
        login_page.open()
        login_page.login()

        assert driver_function.find_element(By.ID, "pills-allrec-tab"), "Dashboard tabs not visible after login."