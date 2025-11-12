import pytest
from utils.browser_setup import setup_browser
from utils.screenshot import Screenshot

@pytest.fixture(scope="session")
def driver():
    driver = setup_browser()
    yield driver
    driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            name = item.name
            path = Screenshot.take(driver, f"failed_{name}")
            if path and hasattr(report, "extra"):
                plugin = item.config.pluginmanager.getplugin("html")
                if plugin:
                    html = (
                        f'<div><a href="{path}" target="_blank">'
                        f'<img src="{path}" alt="screenshot" '
                        f'style="width:300px;height:200px;border:1px solid #ccc"/></a></div>'
                    )
                    report.extra.append(plugin.extras.html(html))
