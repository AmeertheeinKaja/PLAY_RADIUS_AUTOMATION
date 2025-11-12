from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def setup_browser():
    chrome_options = Options()

    # Suppress automation banners
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_argument("--disable-infobars")

    # Disable Chrome warnings, notifications, and password popups
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_entry_breach_check_enabled": False,
        "profile.password_bubble_leak_detection_enabled": False,
        "profile.enhanced_protection_enabled": False,
        "profile.safe_browsing_enabled": False,
        "safebrowsing.enabled": False,
        "safebrowsing.disable_download_protection": True,
        "profile.default_content_setting_values.notifications": 2,
        "profile.default_content_setting_values.automatic_downloads": 1,
    }
    chrome_options.add_experimental_option("prefs", prefs)

    # Disable warnings and startup prompts
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--ignore-ssl-errors")
    chrome_options.add_argument("--allow-insecure-localhost")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--no-default-browser-check")
    chrome_options.add_argument("--no-first-run")
    chrome_options.add_argument(
        "--disable-features=PasswordLeakDetection,PasswordCheck,"
        "PasswordManagerOnboarding,AutofillServerCommunication,"
        "SafeBrowsingEnhancedProtection"
    )

    # Optional for CI / headless mode
    # chrome_options.add_argument("--headless=new")

    # Suppress Chrome logs
    chrome_options.add_argument("--log-level=3")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options,
    )
    driver.maximize_window()
    driver.implicitly_wait(3)
    return driver
