import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from pages.common.sidemenupage import SideMenuPage
from pages.process.process_manager.create_process import CreateProcess
from pages.process.process_manager.search_process import OpenProcess
from pages.process.process_manager.process_filter import ProcessFilter
from pages.common.open_filter_search import FilterSearch
from pages.process.channel_config.call.call_stt_config import CallSTTConfig
from pages.common.loader import Loader
from pages.record.ai_insights_page import AIInsightsPage
from pages.record.email.email_record_page import EmailPage
from pages.record.rating_page import RatingPage
from pages.record.record_controls.record_navigator import RecordNavigator
from pages.record.record_controls.record_page_tabs import RecordPageTabs
from pages.record.record_controls.record_recent_record import RecentRecordsMenu
from utils.logger import get_logger
from utils.screenshot import Screenshot
from pages.record.chat.chat_record_page import ChatPage
from pages.process.channel_config.channel_config_router import ChannelConfigRouter
logger = get_logger(__name__)


class RecordPage(BasePage):


    CALL_LOGO=(By.XPATH,"//div[@class='pbi_content']//span[@title='Channel - Call']")
    CHAT_LOGO = (By.XPATH, "//div[@class='pbi_content']//span[@title='Channel - Chat']")
    EMAIL_LOGO = (By.XPATH, "//div[@class='pbi_content']//span[@title='Channel - Email']")
    VIDEO_LOGO = (By.XPATH, "//div[@class='pbi_content']//span[@title='Channel - Video']")

    TOAST_LOCATOR = (By.XPATH, "//div[@role='status']")
    MEDIA_NOT_FOUND_BTN = (By.XPATH, "//button[@title='Media Not Found']")
    GENERATE_TRANSCRIPT_BTN = (By.XPATH, "//button[@title='Click to generate transcript']")
    SENTIMENT_SCORE_BTN = (By.XPATH, "//button[@title='Click to generate sentiment']")
    PROCESS_NAME = (
        By.XPATH,
        "//div[@class='col-6']/span[contains(@title,'Process Name')]"
    )
    AUDIO_PLAYER_SCOPE = "//div[@class='play_audio_bar']"

    PLAY_BTN = (By.XPATH, f"{AUDIO_PLAYER_SCOPE}//button[@id='play_btn']")
    REWIND_BTN = (By.XPATH, f"{AUDIO_PLAYER_SCOPE}//button[@title='Backward']")
    FORWARD_BTN = (By.XPATH, f"{AUDIO_PLAYER_SCOPE}//button[@title='Forward']")
    SPEED_BTN = (By.XPATH, f"{AUDIO_PLAYER_SCOPE}//button[@title='Speed']")
    MUTE_BTN = (By.XPATH, f"{AUDIO_PLAYER_SCOPE}//button[@title='Mute']")
    VOLUME_SLIDER = (By.XPATH, f"{AUDIO_PLAYER_SCOPE}//input[@title='Volume']")
    DOWNLOAD_AUDIO_BTN = (By.XPATH, f"{AUDIO_PLAYER_SCOPE}//a[@title='Download Audio']")
    error_text="Key file is missing."
    ERROR_MEDIA_NOT_FOUND="Media Not Found"
    RECORD_ID = (By.XPATH, "//span[starts-with(@title, 'RecordId')]")
    CHAT_MESSAGES = (By.CSS_SELECTOR, ".chat_messages .message_row")
    EMAIL_ITEMS = (By.CSS_SELECTOR, ".pw_mail_list_item")
    INTERACTION_TYPE = (
        By.XPATH,
        "//span[contains(@class,'icon-inbound') or contains(@class,'icon-outbound')]"
        "/following-sibling::span"
    )



    def __init__(self, driver,config_data):
        super().__init__(driver)
        self.loader = Loader(driver)
        self.open_process = OpenProcess(driver)
        self.open_filter = FilterSearch(driver)
        self.process_filter = ProcessFilter(driver)
        self.call_stt_config = CallSTTConfig(driver)
        self.navigator = RecordNavigator(self.driver)
        self.recent_records_menu = RecentRecordsMenu(driver)
        self.router = ChannelConfigRouter(driver, config_data)
        self.process_manager=CreateProcess(driver)
        self.side_menu_page = SideMenuPage(driver)
        self.record_tabs = RecordPageTabs(driver)
        self.ai_insights_page = AIInsightsPage(driver)
        self.rating_page = RatingPage(driver)
        self.process_name=None
        self.channel=None
        self.record_id=None
        self.interaction_type=None

        self.config_data = config_data

    def record_info(self,error_message=None):
        self.error_message=error_message
        # Capture toast only once
        if not self.error_message:
            self.find_message()
        self.find_record_id()
        self.find_channel()
        self.find_process_name()
        self.get_interaction_type()

        if not self.has_record_data():
            logger.info(f"ℹ No {self.channel} data found for record {self.record_id}. Skipping.")
            return "NO_DATA"
        #
        # if self.check_media_not_found():
        #     return  # handled, nothing more to do
        # if self.channel == "chat":
        #     return self._handle_chat_channel()
        # self.handle_record_flow()


    def get_record_type(self):
        if self.is_element_present(self.CALL_LOGO):
            return "Call"
        if self.is_element_present(self.CHAT_LOGO):
            return "Chat"
        if self.is_element_present(self.EMAIL_LOGO):
            return "Email"
        if self.is_element_present(self.VIDEO_LOGO):
            return "Video"

        return "Unknown"

    def is_element_present(self, locator):
        try:
            self.driver.find_element(*locator)
            return True
        except:
            return False

    def find_channel(self):
        self.channel=self.get_record_type().lower()
        logger.info(f"Record Channel is: {self.channel}")

    def find_record_id(self):
        try:
            # Wait for the element
            record_element = self.wait_until_visible(self.RECORD_ID)

            # Clean the text (removes '(' and ')')
            self.record_id = record_element.text.strip("()")

            logger.info(f"Record ID successfully retrieved: {self.record_id}")

            # Ensure you are returning the value you need
            return self.record_id

        except Exception as e:
            logger.error(f"Error retrieving Record ID: {e}", exc_info=True)
            Screenshot.take(self.driver, "Record_ID_Error")
            return None


    def find_message(self):
        if self.error_message:
            return self.error_message

        toast = self.capture_toast(timeout=2)
        if toast:
            self.error_message = toast
            return toast

        # fallback scanning page for message
        try:
            body = self.driver.find_element(By.TAG_NAME, "body").text
            if "Key file is missing" in body:
                self.error_message = "Key file is missing."
                return self.error_message
        except:
            pass

        return None

    def find_process_name(self):
        try:
            process_element = self.wait_until_visible(self.PROCESS_NAME)
            self.process_name = process_element.get_attribute("title").replace("Process Name - ", "")
            logger.info(f"Process Name is: {self.process_name}")
            return self.process_name
        except Exception as e:
            logger.error("Error retrieving Process Name", exc_info=True)
            Screenshot.take(self.driver, "Process_Name_Error")
            return None
    def generate_transcript(self):
        self.click_generate_btn()


    def click_generate_btn(self):
        try:
            generate_btn = self.wait_until_clickable(self.GENERATE_TRANSCRIPT_BTN, timeout=5)
            generate_btn.click()
            logger.info("Clicked 'Generate Transcript' button.")
            self.loader.load()
            Screenshot.take(self.driver, "Generate_Transcript_Clicked")
            return True
        except Exception as e:
            logger.error("Could not click 'Generate Transcript' button.", exc_info=True)
            Screenshot.take(self.driver, "Generate_Transcript_Click_Error")
            return False

    def check_media_not_found(self):
        """Detects Media Not Found block, clicks it, captures toast, and routes fix."""
        try:
            # 1. Check presence
            if not self.is_element_present(self.MEDIA_NOT_FOUND_BTN):
                logger.info("No Media-Not-Found widget found on page.")
                return False

            logger.info("⚠ Media-Not-Found widget detected on record page.")

            # 2. Click widget button
            btn = self.wait_until_clickable(self.MEDIA_NOT_FOUND_BTN, timeout=5)
            btn.click()
            logger.info("Clicked Media-Not-Found widget button.")
            self.loader.load()

            # 3. Capture toast
            toast = self.capture_toast(timeout=3)
            logger.info(f"Media-Not-Found toast: {toast}")
            self.open_process_page()
            self.handle_media_not_found_widget()

            # if toast == self.ERROR_MEDIA_NOT_FOUND:
            #     logger.info("🔧 Triggering call storage reconfigure due to Media Not Found.")
            #     self.open_process_page()
            #     self.handle_media_not_found_widget()
            #
            # logger.warning("Media Not Found widget clicked, but toast did not match.")
            # return False

        except Exception as e:
            logger.error("Error handling Media-Not-Found widget.", exc_info=True)
            Screenshot.take(self.driver, "Media_Not_Found_Widget_Error")
            return False
    def handle_media_not_found_widget(self):
        logger.info("🔧 Triggering reconfiguration due to Media Not Found.")
        if self.channel == "call":
            self.router.route_call_storage_missing_key()
        return True

    def capture_toast(self, timeout=3):
        locator = (By.XPATH, "//div[@role='status']")

        end = time.time() + timeout
        last_message = None

        while time.time() < end:
            elements = self.driver.find_elements(*locator)

            for el in elements:
                txt = el.text.strip()
                if txt and txt != "Loading...":
                    last_message = txt

            if last_message:
                logger.info(f"TOAST captured: {last_message}")
                return last_message

            time.sleep(0.1)

        # If nothing good found, return whatever was last seen
        if last_message:
            logger.info(f"TOAST returned after fallback: {last_message}")
            return last_message

        logger.info("No toast detected.")
        return None

    def open_process_page(self):
        self.open_process.process()
        self.open_filter.filter()
        self.process_filter.apply_filter_by_name(self.process_name)
        self.open_process.view_process()
        self.process_manager.ensure_channel_enabled(self.channel)
        # self.recent_records_menu.click_record_by_href_id(self.record_id)

    def return_to_record(self):
        """
        Navigates back to the previously opened record
        """
        logger.info(f"↩ Returning to record: {self.record_id}")
        self.recent_records_menu.click_record_by_href_id(self.record_id)

    def media_not_found(self):
        if self.error_message == self.ERROR_MEDIA_NOT_FOUND:
            logger.info("⚠ Media Not Found error detected. Opening process page...")
            self.open_process_page()
            self.handle_missing_key()
        else:
            logger.info("ℹ No Media Not Found error. Skipping process page opening.")

    def click_media_not_found_btn(self):
        try:
            media_not_found_btn = self.wait_until_clickable(self.MEDIA_NOT_FOUND_BTN, timeout=5)
            media_not_found_btn.click()
            logger.info("Clicked 'Media Not Found' button.")
            self.loader.load()
            Screenshot.take(self.driver, "Media_Not_Found_Clicked")
            return True
        except Exception as e:
            logger.error("Could not click 'Media Not Found' button.", exc_info=True)
            Screenshot.take(self.driver, "Media_Not_Found_Click_Error")
            return False

    def handle_data_not_found(self):
        """
        Called when record opens but channel data is missing
        """
        logger.warning(
            f"⚠ {self.channel.upper()} data not found for record {self.record_id}"
        )

        self.open_process_page()

        if self.channel == "call":
            logger.info("Routing call storage missing key...")
            self.router.route_call_storage_missing_key()

        elif self.channel == "chat":
            logger.info("Routing chat storage missing key...")
            self.router.route_chat_storage_missing_key()

        elif self.channel == "email":
            logger.info("Routing email storage missing key...")
            self.router.route_email_storage_missing_key()

        elif self.channel == "video":
            logger.info("Video storage handling not implemented yet")

        self.return_to_record()
        logger.info("✅ Storage reconfiguration triggered due to missing data")

    def handle_record_flow(self):


        logger.info(f"Checking if error message matches expected error text...")
        logger.info(f"Expected Error Text: {self.error_text}")
        logger.info(f"Actual Error Text: {self.error_message}")

        if self.error_message == self.error_text:
            logger.info("⚠ Error message matched. Opening process page...")
            self.open_process_page()
            self.handle_missing_key()
        else:
            logger.info("ℹ No matching error message. Skipping process page opening.")

    def has_chat_data(self):
        return len(self.driver.find_elements(*self.CHAT_MESSAGES)) > 0

    def has_email_data(self):
        return len(self.driver.find_elements(*self.EMAIL_ITEMS)) > 0

    def has_call_data(self):
        return self.is_element_present(self.PLAY_BTN)

    def has_video_data(self):
        return self.is_element_present((By.TAG_NAME, "video"))

    def has_record_data(self):
        if self.channel == "chat":
            return self.has_chat_data()
        if self.channel == "email":
            return self.has_email_data()
        if self.channel == "call":
            return self.has_call_data()
        if self.channel == "video":
            return self.has_video_data()
        return False

    def get_interaction_type(self):
        """
        Returns interaction type: Inbound / Outbound
        """
        element = self.wait_until_visible(self.INTERACTION_TYPE)
        interaction_type = element.text.strip()

        self.interaction_type = interaction_type
        logger.info(f"Interaction type detected: {interaction_type}")

        return interaction_type
    def handle_missing_key(self):

        if self.channel == "call":
            self.router.route_call_missing_key()

        elif self.channel == "chat":
            self.router.route_chat_missing_key()

        elif self.channel == "email":
            self.router.route_email_missing_key()

        elif self.channel == "video":
            self.router.route_video_missing_key()

    def open_record_from_sidebar(self, record_id):


        logger.info(f"🔎 Trying to open record from sidebar: {record_id}")

        try:
            # Dynamic locator for <a> with matching href
            locator = (By.XPATH, f"//div[@id='v-pills-tab']//a[contains(@href, '{record_id}')]")

            # Wait for visibility
            link = self.wait_until_clickable(locator, timeout=10)

            # Scroll into view (important for fixed sidebar)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", link)
            time.sleep(0.2)

            link.click()
            logger.info(f"📂 Sidebar record clicked: {record_id}")

            # Wait for any loader to finish
            self.loader.load()

            # Optional: capture toast after opening
            toast = self.capture_toast()
            logger.info(f"Toast after clicking sidebar record: {toast}")

            Screenshot.take(self.driver, f"Record_from_sidebar_{record_id}")

            return True

        except Exception as e:
            logger.error(f"❌ Could not open sidebar record: {record_id}", exc_info=True)
            Screenshot.take(self.driver, f"Sidebar_record_open_error_{record_id}")
            return False

    def _handle_chat_channel(self):
        """
        Handle CHAT channel record actions
        """
        logger.info("Handling CHAT channel")

        chat_page = ChatPage(self.driver)

        if not chat_page.has_messages():
            logger.info("Chat data not found")
            return "CHAT_DATA_NOT_FOUND"

        chat_page.add_comment_to_first_message("Automation test comment")
        chat_page.translate_chat("English", use_search=True)
        chat_page.back_to_original()

        return "CHAT_SUCCESS"

    def process_current_record(self):
        self.record_info()

        if self.error_message == self.error_text:
            logger.warning("⚠ Key file missing detected")
            logger.info(f"error_message: {self.error_message}++ expected: {self.error_text}")
            self.handle_record_flow()
            self.return_to_record()
            self.open_process_page()
            self.handle_missing_key()
            self.return_to_record()

            self.record_info()
            self._handle_record_tabs()
            return

        if self.check_media_not_found():
            self.record_info()
            self._handle_record_tabs()
            return

        if not self.has_record_data():
            self.handle_data_not_found()

            self.record_info()
            self._handle_record_tabs()
            return

        # -----------------------------
        # CHANNEL-SPECIFIC ACTIONS
        # -----------------------------
        try:
            if self.channel == "chat":
                chat_page = ChatPage(self.driver)
                if chat_page.has_messages():
                    chat_page.add_comment_to_first_message("Automation test comment")
                    chat_page.translate_chat("Japanese", use_search=True)
                    self.loader.load()
                    chat_page.back_to_original()

            elif self.channel == "email":
                email_page = EmailPage(self.driver)
                if email_page.has_emails():
                    mail = email_page.open_first_mail()
                    interaction = email_page.get_interaction_type(mail)
                    logger.info(f"📧 Email interaction type: {interaction}")
                    email_page.close_mail(mail)

        except Exception:
            logger.error("❌ Channel handling failed", exc_info=True)

        # -----------------------------
        # RECORD-LEVEL TABS (ALWAYS)
        # -----------------------------
        self._handle_record_tabs()

    def _handle_record_tabs(self):
        """
        Handles common record tabs for ALL channels
        """
        logger.info("📑 Navigating record tabs")

        try:
            self.record_tabs.switch_tabs("ai_insights")
            self.ai_insights_page.ai_insights_info()
        except Exception:
            logger.warning("AI Insights tab not available")

        try:
            self.record_tabs.switch_tabs("ratings")
        except Exception:
            logger.warning("Ratings tab not available")

        try:
            self.record_tabs.switch_tabs("comments")
        except Exception:
            logger.warning("Comments tab not available")

    def process_all_records(self):
        navigator = RecordNavigator(self.driver)

        navigator.iterate_all_records(
            callback=lambda _: self.process_current_record()
        )