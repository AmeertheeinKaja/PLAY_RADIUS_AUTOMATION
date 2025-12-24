from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import get_logger
from utils.screenshot import Screenshot
from pages.common.loader import Loader

logger = get_logger(__name__)


class RecentRecordsMenu(BasePage):
    RECENT_RECORD_BTNS = (
        By.XPATH,
        "//div[@id='v-pills-tab']//div[@class='tm_opts']/a/button"
    )
    def __init__(self, driver):
        super().__init__(driver)
        self.loader = Loader(driver)

    def click_record_by_name(self, name_part: str):
        """
        Clicks a recent record by partial title tooltip.
        Example: name_part='RADIUS_OIS'
        """
        logger.info(f"🔍 Searching recent record containing: {name_part}")

        buttons = self.driver.find_elements(*self.RECENT_RECORD_BTNS)

        for btn in buttons:
            title = btn.get_attribute("title") or ""
            if name_part.lower() in title.lower():
                logger.info(f"📌 Clicking recent record: {title}")
                self.driver.execute_script("arguments[0].click();", btn)
                Screenshot.take(self.driver, f"Clicked_Recent_{title}")
                return

        logger.error(f"❌ Recent record '{name_part}' not found in top menu")
        Screenshot.take(self.driver, f"Recent_Record_Not_Found_{name_part}")
        raise Exception(f"Recent record '${name_part}' not found")

    def click_record_by_href_id(self, record_id: str):
        """
        Example href: /play/recording-list/SS1753539105906BBH
        record_id = 'SS1753539105906BBH'
        """
        locator = (
            By.XPATH,
            f"//div[@id='v-pills-tab']//a[contains(@href,'{record_id}')]/button"
        )

        logger.info(f"🔍 Trying to click record with ID: {record_id}")

        btn = self.wait_until_clickable(locator)
        self.driver.execute_script("arguments[0].click();", btn)
        self.loader.load()

        Screenshot.take(self.driver, f"Clicked_Record_ID_{record_id}")
        logger.info(f"✅ Record {record_id} clicked successfully!")
