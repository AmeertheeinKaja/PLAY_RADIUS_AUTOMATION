import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from pages.process.process_manager.search_process import OpenProcess
from pages.process.process_manager.process_filter import ProcessFilter
from pages.common.open_filter_search import FilterSearch
from pages.process.channel_config.call.call_stt_config import CallSTTConfig
from pages.common.loader import Loader
from utils.logger import get_logger
from utils.screenshot import Screenshot
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



    def __init__(self, driver,config_data):
        super().__init__(driver)
        self.loader = Loader(driver)
        self.open_process = OpenProcess(driver)
        self.open_filter = FilterSearch(driver)
        self.process_filter = ProcessFilter(driver)
        self.call_stt_config = CallSTTConfig(driver)
        self.router = ChannelConfigRouter(driver, config_data)
        self.process_name=None
        self.channel=None

        self.config_data = config_data

    def record_info(self,error_message=None):
        self.error_message=error_message
        # Capture toast only once
        # if not self.error_message:
        #     self.find_message()

        self.find_channel()
        self.find_process_name()
        if self.check_media_not_found():
            return  # handled, nothing more to do
        self.handle_record_flow()


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

