from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import get_logger
from pages.common.loader import Loader
from utils.screenshot import Screenshot
from selenium.webdriver.common.action_chains import ActionChains
from pages.common.submit_search_filter import SubmitFilterSearch
from utils.screenshot import Screenshot

logger = get_logger(__name__)


class AIInsightsPage(BasePage):
    GENERATE_SUMMARY_BTN = (By.XPATH, "//button[@title='Click to generate Summary']")
    GENERATE_SUMMARY_TEXT = (By.XPATH, "//span[text()='Generate Summary']")
    SENTIMENT_SCORE_BTN=(By.XPATH, "//button[@title='Click to generate sentiment']")
    TOAST_ERROR_TEXT="No Sentiment is Generated. Generate it."
    TOAST_PROPERTY_ERROR_TEXT="Cannot read properties of undefined (reading 'split')"
    TOAST_NO_VERSION="No Active Version found."


    CHANNEL_TAB_IDS = {
        "chat": "chat-pane",
        "call": "summary-tab-pane",  # under Call tab, summary is the active content with chatbox
        "video": "chat-pane",  # under Video tab, chat content
        "email": "email-pane",  # email content tab
    }
    SCROLL_CONTAINERS = {
        "summary": "#summary-tab-pane .overflow-y-auto",
        "translate": "#translate-tab-pane .chat_box_messages",
        "ratings": None,
        "comments": None
    }

    def __init__(self, driver):
        super().__init__(driver)
        self.action = SubmitFilterSearch(driver)
        self.last_message = None
        self.channel=None
        self.count=0




    def click_generate_summary(self):

        try:
            logger.info(f" Attempting  to click 'Generate Summary' button...")

            generate_summary_button = self.wait_until_clickable(self.GENERATE_SUMMARY_BTN)
            actions = ActionChains(self.driver)
            actions.move_to_element(generate_summary_button).click().perform()

            self.count += 1  # ✅ increment here

            logger.info(f"✅ 'Generate Summary' button clicked {self.count} time(s).")
            Screenshot.take(self.driver, "Generate_Summary_Clicked")


        except Exception as e:
            Screenshot.take(self.driver, "Error_Generate_Summary_Click")
            logger.error(f"❌ Error clicking 'Generate Summary' button: {e}", exc_info=True)
            print(f"Error during clicking 'Generate Summary' button: {e}")

    def is_generate_summary_displayed(self):
        logger.info("🔍 Checking if 'Generate Summary' is displayed...")

        try:
            elements = self.driver.find_elements(*self.GENERATE_SUMMARY_TEXT)

            if len(elements) == 0:
                logger.info("ℹ️ 'Generate Summary' not found on page.")
                return False

            is_displayed = elements[0].is_displayed()
            logger.info(f"Is displayed? {is_displayed}")
            return is_displayed

        except Exception as e:
            logger.error(f"❌ Error checking 'Generate Summary': {e}")
            return False

    def get_last_message(self):
        # Just return stored message, do NOT capture again here
        return self.last_message

    def generate_sentiment_score(self):
        try:
            logger.info("🔄 Attempting to click 'Generate Sentiment Score' button...")

            sentiment_score_button = self.wait_until_clickable(self.SENTIMENT_SCORE_BTN)
            actions = ActionChains(self.driver)
            actions.move_to_element(sentiment_score_button).click().perform()

            logger.info("✅ 'Generate Sentiment Score' button clicked.")
            Screenshot.take(self.driver, "Generate_Sentiment_Score_Clicked")


        except Exception as e:
            Screenshot.take(self.driver, "Error_Generate_Sentiment_Score_Click")
            logger.error(f"❌ Error clicking 'Generate Sentiment Score' button: {e}", exc_info=True)
            print(f"Error during clicking 'Generate Sentiment Score' button: {e}")

    def ai_insights_info(self):
        try:
            logger.info("🧭 Checking AI Insights panel state...")
            self.channel = self.action.get_record_type().lower()

            # 1. Summary visible?
            if self.is_generate_summary_displayed():
                logger.info("✨ 'Generate Summary' is available. Proceeding to click...")

                self.click_generate_summary()

                # Capture toast ONCE
                self.last_message = self.capture_toast()
                logger.info(f"📨 Toast message captured: {self.last_message}")

                # ✅ HANDLE SENTIMENT MISSING CASE
                if self.last_message == self.TOAST_ERROR_TEXT:
                    logger.warning("⚠ Sentiment missing. Triggering sentiment generation...")

                    self.generate_sentiment_score()

                    # capture toast again (optional but recommended)
                    self.last_message = self.capture_toast()
                    logger.info(f"📨 Sentiment Toast captured: {self.last_message}")

                    logger.info("🔁 Retrying Generate Summary after sentiment generation...")
                    self.click_generate_summary()
                    self.last_message = self.capture_toast()
                    logger.info(f"📨 Final Summary Toast: {self.last_message}")

                return self.last_message

            # 2. If not found → maybe below fold → scroll
            scroll_locator = self.get_scroll_container("summary")

            if scroll_locator:
                scroll_el = self.wait_until_visible(scroll_locator)

                content_h = self.driver.execute_script(
                    "return arguments[0].scrollHeight;", scroll_el
                )
                visible_h = self.driver.execute_script(
                    "return arguments[0].clientHeight;", scroll_el
                )

                if content_h > visible_h:
                    logger.info("🌀 Scrolling Summary container...")
                    self.scroll_element_slow(scroll_el)
                else:
                    logger.info("Summary container does not require scrolling.")
            else:
                logger.info("No scrollable container for Summary tab.")

            return None

        except Exception as e:
            Screenshot.take(self.driver, "Error_AI_Insights_Info")
            logger.error(f"❌ Error in ai_insights_info: {e}", exc_info=True)
            return None



    def get_scroll_container(self, channel):
        css = self.SCROLL_CONTAINERS.get(channel)

        if css is None:
            logger.info(f"No scrollable content for channel: {channel}")
            return None

        return (By.CSS_SELECTOR, css)

