from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.common.submit_search_filter import SubmitFilterSearch
from utils.logger import get_logger
from pages.common.loader import Loader
from utils.screenshot import Screenshot
from selenium.webdriver.common.action_chains import ActionChains

logger = get_logger(__name__)


class RecordPageTabs(BasePage):

    class RecordPageTabHandler:
        # -------------------- TAB LOCATORS --------------------
        EMAIL_TAB = (By.ID, "email_detail_tab")
        CHAT_TAB = (By.ID, "chat_detail_tab")
        VIDEO_TAB = (By.ID, "video_detail_tab")

        AI_INSIGHTS_TAB = (By.ID, "summary-tab")
        RATINGS_TAB = (By.ID, "ratings-tab")
        COMMENTS_TAB = (By.ID, "comments-tab")

        # Transcript tab (call channel)
        TRANSCRIPT_TAB = (By.ID, "call_detail_tab")

        # Media tab (video channel)
        MEDIA_TAB = (By.XPATH, "//button[@id='video_media_tab' or @aria-controls='agentdet-pane']")

        # -------------------- CHANNEL & TAB RULES --------------------
        CHANNEL_TABS = {
            "call": ["transcript", "ai_insights", "ratings", "comments"],
            "chat": ["chat", "ai_insights", "ratings", "comments"],
            "email": ["email", "ai_insights", "ratings", "comments"],
            "video": ["video", "media", "ai_insights", "ratings", "comments"],
        }

        # -------------------- TAB → LOCATOR MAP --------------------
        TAB_MAP = {
            "email": EMAIL_TAB,
            "chat": CHAT_TAB,
            "video": VIDEO_TAB,

            "transcript": TRANSCRIPT_TAB,
            "media": MEDIA_TAB,

            "ai_insights": AI_INSIGHTS_TAB,
            "ratings": RATINGS_TAB,
            "comments": COMMENTS_TAB
        }
        HOME_TAB_MAP = {
            "call": "transcript",
            "email": "email",
            "chat": "chat",
            "video": "video"
        }

    # ----------------------------------------------------------
    #                    INIT
    # ----------------------------------------------------------
    def __init__(self, driver):
        super().__init__(driver)
        self.action = SubmitFilterSearch(driver)
        self.loader = Loader(driver)
        self.driver = driver

        self.channel = None

    # ----------------------------------------------------------
    #            IDENTIFY CHANNEL (call/chat/email/video)
    # ----------------------------------------------------------
    def find_channel(self):
        try:
            self.channel = self.action.get_record_type().lower()
            logger.info(f"[RecordPageTabs] Channel identified: {self.channel}")
        except Exception as e:
            logger.error(f"Failed to detect channel: {e}")
            Screenshot.take(self.driver,f"channel_detect_failed")
        return self.channel

    # ----------------------------------------------------------
    #            INTERNAL CLICK WITH FALLBACKS
    # ----------------------------------------------------------
    def click_element(self, element, name):
        try:
            # Scroll into view
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

            # Try normal click
            element.click()
            logger.info(f"[RecordPageTabs] Clicked: {name}")

        except Exception:
            logger.warning(f"[RecordPageTabs] Normal click failed. Trying JS click → {name}")
            try:
                self.driver.execute_script("arguments[0].click();", element)
            except Exception:
                logger.error(f"[RecordPageTabs] JS click also failed on {name}")
                Screenshot.take(self.driver,f"click_failed_{name}")
                raise

    # ----------------------------------------------------------
    #                   SWITCH TABS CLEANLY
    # ----------------------------------------------------------
    from selenium.common.exceptions import TimeoutException, NoSuchElementException

    def is_element_present(self, locator):
        try:
            self.wait_until_visible(locator, timeout=3)
            return True
        except TimeoutException:
            return False

    def switch_tabs(self, tab_name: str):
        tab_name = tab_name.lower()
        logger.info(f"[RecordPageTabs] Request → Switch tab: {tab_name}")

        # Detect channel if not already detected
        if not self.channel:
            self.find_channel()

        allowed_tabs = self.RecordPageTabHandler.CHANNEL_TABS.get(self.channel, [])

        # ---------- Channel validation ----------
        if tab_name not in allowed_tabs:
            logger.warning(
                f"[RecordPageTabs] '{tab_name}' is NOT allowed for channel '{self.channel}'. Skipping."
            )
            Screenshot.take(self.driver,f"skipped_invalid_tab_{tab_name}")
            return False  # <-- no failure, just skip

        # ---------- Locator fetch ----------
        locator = self.RecordPageTabHandler.TAB_MAP.get(tab_name)

        if not locator:
            logger.warning(
                f"[RecordPageTabs] No locator found for tab '{tab_name}'. Skipping."
            )
            Screenshot.take(self.driver,f"missing_locator_{tab_name}")
            return False

        # ---------- EARLY EXIT IF ELEMENT NOT PRESENT ----------
        if not self.is_element_present(locator):
            logger.warning(
                f"[RecordPageTabs] Tab '{tab_name}' is NOT present on this UI. Skipping."
            )
            Screenshot.take(self.driver,f"tab_not_present_{tab_name}")
            return False

        # ---------- Try clicking ----------
        try:
            element = self.wait_until_clickable(locator)
            self.click_element(element, tab_name)

            self.loader.load()  # Wait for content to load
            logger.info(f"[RecordPageTabs] ✔ Switched to tab: {tab_name}")
            return True

        except Exception as e:
            logger.error(f"[RecordPageTabs] ❌ Failed switching to tab '{tab_name}': {e}")
            Screenshot.take(self.driver,f"switch_failed_{tab_name}")
            return False  # <-- again: no crash

    def open_home_tab(self):
        """
        Automatically opens the base/default tab for the detected channel.
        Example:
          - call → transcript
          - email → email
          - chat → chat
          - video → video
        """
        if not self.channel:
            self.find_channel()

        home_tab = self.RecordPageTabHandler.HOME_TAB_MAP.get(self.channel)

        if not home_tab:
            msg = f"[RecordPageTabs] No HOME tab configured for channel: {self.channel}"
            logger.error(msg)
            Screenshot.take(self.driver,f"missing_home_tab_{self.channel}")
            raise Exception(msg)

        logger.info(f"[RecordPageTabs] Opening HOME tab: {home_tab}")
        return self.switch_tabs(home_tab)