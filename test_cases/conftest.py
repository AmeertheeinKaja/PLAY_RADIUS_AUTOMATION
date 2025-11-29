import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from pages.login.login import LoginPage
from utils.read_properties import ReadConfig
from utils.screenshot import Screenshot
import allure


# =========================================================
# 🔧 BROWSER SETUP
# =========================================================
def setup_browser():
    chrome_options = Options()

    # Basic settings
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")

    #  Disable Chrome Password Manager
    chrome_options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "autofill.profile_enabled": False,
        "autofill.credit_card_enabled": False,
        "password_manager.leak_detection.enabled": False,
    })

    #  Disable ALL Google services that create the popup
    chrome_options.add_argument("--disable-save-password-bubble")
    chrome_options.add_argument("--disable-features=PasswordManagerOnboarding")
    chrome_options.add_argument("--disable-features=PasswordChange")
    chrome_options.add_argument("--disable-features=PasswordLeakDetection")
    chrome_options.add_argument("--disable-features=SafetyCheck")
    chrome_options.add_argument("--disable-features=NotificationTriggers")
    chrome_options.add_argument("--disable-features=PasswordManagerRedesign")
    chrome_options.add_argument("--disable-features=PasswordReuseDetection")
    chrome_options.add_argument("--disable-features=AutofillServerCommunication")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--disable-features=IsolateOrigins,site-per-process")
    chrome_options.add_argument("--allow-cross-origin-auth-prompt")


    # Guest mode OFF (forces normal fresh session)
    chrome_options.add_argument("--guest=false")

    # Run Chrome without syncing any stored Google credentials
    chrome_options.add_argument("--disable-sync")

    # OPTIONAL: Force a new clean session
    chrome_options.add_argument("--no-first-run")
    chrome_options.add_argument("--no-default-browser-check")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    driver.implicitly_wait(5)
    return driver

# =========================================================
# 🚀 FIXTURES
# =========================================================

@pytest.fixture(scope="function")
def driver_function():
    """Creates a NEW browser instance for each test."""
    driver = setup_browser()
    yield driver
    driver.quit()


@pytest.fixture(scope="session")
def driver_session():
    """Creates ONE browser instance reused for the entire session."""
    driver = setup_browser()
    yield driver
    driver.quit()


@pytest.fixture(scope="session")
def credentials():
    """Loads credentials once per test session."""
    return {
        "username": ReadConfig.get_username(),
        "password": ReadConfig.get_password()
    }


@pytest.fixture(scope="function")
def login_driver(driver_session, credentials):
    """
    Provides a logged-in driver.
    Reuses the session-scoped browser for faster execution.
    """
    login_page = LoginPage(driver_session)

    # Login only if not already on a post-login page
    if "recording-list" not in driver_session.current_url:
        login_page.open()
        login_page.login(
            username=credentials["username"],
            password=credentials["password"]
        )

    yield driver_session

def pytest_runtest_setup(item):
    # Auto set Allure Title = Test function name
    test_name = item.name.replace("_", " ").title()
    allure.dynamic.title(test_name)

    # Auto set Allure Description = Docstring (if exists)
    if item.function.__doc__:
        allure.dynamic.description(item.function.__doc__.strip())
# =========================================================
# 📸 SCREENSHOT ON FAILURE
# =========================================================
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture screenshot when a test fails (pytest-html compatible)."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        # Try to fetch any available driver fixture
        driver = (
            item.funcargs.get("driver_function") or
            item.funcargs.get("driver_session") or
            item.funcargs.get("login_driver")
        )

        if driver:
            test_name = item.name
            screenshot_path = Screenshot.take(driver, f"failed_{test_name}")

            if screenshot_path and hasattr(report, "extra"):
                pytest_html = item.config.pluginmanager.getplugin("html")
                if pytest_html:
                    html = (
                        f'<div><a href="{screenshot_path}" target="_blank">'
                        f'<img src="{screenshot_path}" alt="screenshot" '
                        f'style="width:300px;height:200px;border:1px solid #ccc"/></a></div>'
                    )
                    report.extra.append(pytest_html.extras.html(html))
