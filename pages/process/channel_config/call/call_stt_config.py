import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from pages.base_page import BasePage
from pages.common.loader import Loader
from utils.logger import get_logger

from utils.screenshot import Screenshot

logger = get_logger()



class CallSTTConfig(BasePage):

    # -------------------------
    #       LOCATORS
    # -------------------------
    CALL_SCOPE = "//div[@id='media-configuration-call']"
    STT_TOGGLE = (By.XPATH, "//*[@id='stt-tab-call-pane']/div/form/div/div/div/div/div[1]/div/label[2]/span")
    STT_TOGGLE_INPUT = (By.XPATH, "//input[@name='isEnableSTT']")

    # Inputs
    STT_SAMPLE_HERTZ = (By.NAME, "sampleHertz")
    STT_ENGINE = (By.NAME, "engineNameSTT")
    STT_BUCKET = (By.NAME, "bucketName")
    STT_BUCKET_PATH = (By.NAME, "bucketDirectory")
    STT_KEY_FILE = (By.NAME, "keyFile")
    STT_AUDIO_FILE = (By.NAME, "audioFile")
    STT_PANE_ANCHOR = f"{CALL_SCOPE}//div[@id='stt-tab-call-pane']"

    # Buttons
    TAB_STT = (By.XPATH, "//*[@id='stt-tab-call']")
    BTN_EDIT_MAIN = (By.XPATH,
                     "//div[@id='stt-tab-call-pane']//button[@class='section_form_acts_btn' and @title='Edit']")
    BTN_SAVE = (By.XPATH, f"{CALL_SCOPE}//*[@id='stt-tab-call-pane']//button[@title='Save']")
    BTN_TEST = (By.XPATH, f"{CALL_SCOPE}//button[text()='Test']")
    BTN_SUBMIT = (By.XPATH, "//button[text()='Submit']")
    BTN_EDIT_KEY_FILE = (
        By.XPATH,
        f"{STT_PANE_ANCHOR}//input[@name='prevKeyFile']/following-sibling::button[@title='Edit']"
    )
    # Conversion Mode
    RADIO_MANUAL = (By.XPATH, f"{CALL_SCOPE}//*[@value='manualMode']")
    RADIO_AUTO = (By.XPATH, f"{CALL_SCOPE}//*[@value='autoMode']")

    # Modal — Always select latest active modal
    MODAL_ACTIVE = '(//div[@role="dialog" and contains(@class,"show")])[last()]'
    MODAL_BTN_SUBMIT = (By.XPATH, f"{MODAL_ACTIVE}//button[text()='Submit']")
    MODAL_BTN_CLOSE = (By.XPATH, f"{MODAL_ACTIVE}//button[text()='Close']")
    MODAL_BTN_TEST_AGAIN = (By.XPATH, f"{MODAL_ACTIVE}//button[text()='Test Again']")
    STT_RADIO_CONVERSION_MODE_MANUAL = (By.XPATH, f"{CALL_SCOPE}//*[@value='manualMode']")
    STT_RADIO_CONVERSION_MODE_AUTO = (By.XPATH, f"{CALL_SCOPE}//*[@value='autoMode']")

    # Toast messages
    MSG_TEST_SUCCESS = "Speech-to-text tested successfully"
    MSG_CONVERT_SUCCESS = "Speech-to-text converted successfully"
    MSG_UPDATE_SUCCESS = "Speech-to-text updated successfully"

    ERROR_MESSAGE="This field is required"
    ERROR_LOCATOR=(By.XPATH,"//div[contains(@class, 'invalid-tooltip')]")
    STT_ERROR_LOCATORS = {
        "sample_rate": (
            By.XPATH, "//select[@name='sampleHertz']/following-sibling::div[contains(@class,'invalid-tooltip')]"
        ),
        "engine": (
            By.XPATH, "//select[@name='engineNameSTT']/following-sibling::div[contains(@class,'invalid-tooltip')]"
        ),
        "bucket_name": (
            By.XPATH, "//input[@name='bucketName']/following-sibling::div[contains(@class,'invalid-tooltip')]"
        ),
        "bucket_dir": (
            By.XPATH, "//input[@name='bucketDirectory']/following-sibling::div[contains(@class,'invalid-tooltip')]"
        ),
        "key_file": (
            By.XPATH, "//input[@name='keyFile']/following-sibling::div[contains(@class,'invalid-tooltip')]"
        ),
        "audio_file": (
            By.XPATH,
            "//input[@name='audioFile']/following-sibling::div[contains(@class,'invalid-tooltip')]"
        )

        # "conversion_mode": None  # No error shown for radios in UI
    }

    # -------------------------
    #       CONSTRUCTOR
    # -------------------------
    def __init__(self, driver, speech_to_text=None, bucket_name=None,
                 bucket_dir=None, sample_rate=None, engine_name=None,
                 keyFile=None, audioFile=None, conversion_mode=None):

        super().__init__(driver)
        self.loader = Loader(driver)

        self.speech_to_text = speech_to_text
        self.bucket_name = bucket_name
        self.bucket_dir = bucket_dir
        self.sample_rate = sample_rate
        self.engine = engine_name
        self.key_file = keyFile
        self.audio_file = audioFile
        self.mode = conversion_mode

        self.last_toast = None

    # -------------------------
    #  GENERIC UTILITY METHODS
    # -------------------------
    def _safe_click(self, locator, load=True):
        element = self.wait_until_clickable(locator)
        element.click()
        if load:
            self.loader.load()

    def toast_text(self):
        txt = self.capture_toast()
        self.last_toast = txt
        logger.info(f"Toast: {txt}")
        return txt

    def _handle_modal(self, button_locator):
        """Generic modal button handler."""
        try:
            self.loader.load()
            self._safe_click(button_locator, load=False)
            return self.toast_text()
        except Exception:
            Screenshot.take(self.driver, "modal_handling_failed")
            raise

    # -------------------------
    #       SIMPLE ACTIONS
    # -------------------------
    def open_tab(self):
        self._safe_click(self.TAB_STT)
        logger.info("STT Tab opened")

    def click_edit(self):
        self._safe_click(self.BTN_EDIT_MAIN)
        self.loader.load()
        logger.info("STT Edit clicked")

    def click_save(self):
        self._safe_click(self.BTN_SAVE)
        logger.info("STT Save clicked")

    def click_test(self):
        self._safe_click(self.BTN_TEST)
        logger.info("STT Test clicked")

    def key_file_edit(self):
        self.loader.load()

        # STEP 1: Wait for prevKeyFile INPUT to appear in DOM
        prev_key_input = (By.XPATH, f"{self.STT_PANE_ANCHOR}//input[@name='prevKeyFile']")
        self.wait_until_present(prev_key_input)  # important!

        # STEP 2: Now wait for the Edit button which only appears after React renders it
        edit_btn_locator = self.BTN_EDIT_KEY_FILE

        for attempt in range(3):
            try:
                self.scroll_into_view(edit_btn_locator)
                element = self.wait_until_clickable(edit_btn_locator)
                element.click()
                self.loader.load()
                logger.info("STT Key file Edit clicked")
                return
            except Exception:
                logger.warning(f"Retry {attempt + 1}: Edit button not ready, waiting...")
                time.sleep(1)

        raise Exception("Failed to click Key File Edit button after waiting for DOM render.")

        raise Exception("Failed to click Key File Edit button even after retry.")

    def set_stt(self, turn_on: bool):
        if turn_on:
            self.enable_stt()
        else:
            self.disable_stt()

    def _get_stt_input_and_clickable(self):
        input_locator = (By.XPATH, f"{self.CALL_SCOPE}//input[@name='isEnableSTT']")
        span_locator = (By.XPATH, f"{self.CALL_SCOPE}//input[@name='isEnableSTT']/following-sibling::span")

        # input may be invisible (because disabled), so use presence_of_element_located
        input_el = self.wait_until_present(input_locator)

        # clickable span (this is always visible)
        try:
            span_el = self.driver.find_element(*span_locator)
        except:
            span_el = input_el  # fallback

        return input_el, span_el

    def enable_stt(self):
        input_el, clickable = self._get_stt_input_and_clickable()

        is_disabled = input_el.get_attribute("disabled") is not None
        is_checked = input_el.is_selected()

        if is_disabled:
            logger.info("STT toggle disabled—cannot enable.")
            return

        if is_checked:
            logger.info("STT already enabled, no action.")
            return

        clickable.click()
        logger.info("STT enabled.")
        time.sleep(0.3)
        self.loader.load()

    def disable_stt(self):
        input_el, clickable = self._get_stt_input_and_clickable()

        is_disabled = input_el.get_attribute("disabled") is not None
        is_checked = input_el.is_selected()

        if is_disabled:
            logger.info("STT toggle disabled—cannot disable.")
            return

        if not is_checked:
            logger.info("STT already disabled, no action.")
            return

        clickable.click()
        logger.info("STT disabled.")
        time.sleep(0.3)
        self.loader.load()

    def set_speech_to_text(self, speech_to_text=None):
        # Priority: parameter > JSON value already stored in self.speech_to_text
        if speech_to_text is None:
            speech_to_text = self.speech_to_text

        if speech_to_text is None:
            logger.info("No STT instruction provided, skipping toggle.")
            return

        try:
            input_el, _ = self._get_stt_input_and_clickable()
            current = input_el.is_selected()

            # Only change if needed
            if current == bool(speech_to_text):
                logger.info("STT already in desired state - no change.")
                return

            # delegate to explicit enable/disable so behavior is consistent
            if speech_to_text:
                self.enable_stt()
            else:
                self.disable_stt()

        except Exception:
            logger.error("Error toggling STT", exc_info=True)
            raise

    def set_sample_rate(self, sample_rate=None):
        value = sample_rate if sample_rate is not None else self.sample_rate

        dropdown = Select(self.wait_until_visible(self.STT_SAMPLE_HERTZ))
        dropdown.select_by_value(str(value))

        logger.info(f"Sample rate set to {value}")

    def set_engine(self, engine=None):
        value = engine if engine is not None else self.engine

        dropdown = Select(self.wait_until_visible(self.STT_ENGINE))
        dropdown.select_by_value(value)

        logger.info(f"Engine set to {value}")

    def set_conversion_mode(self, mode=None):
        raw = mode if mode is not None else self.mode
        value = str(raw).lower() if raw else "manualmode"

        if value == "manualmode":
            locator = self.STT_RADIO_CONVERSION_MODE_MANUAL
            name = "Manual Mode"
        elif value == "automode":
            locator = self.STT_RADIO_CONVERSION_MODE_AUTO
            name = "Auto Mode"
        else:
            logger.warning(f"Unknown mode '{value}', defaulting to manual.")
            locator = self.STT_RADIO_CONVERSION_MODE_MANUAL
            name = "Manual Mode (Defaulted)"

        self.driver.find_element(*locator).click()
        logger.info(f"Selected Conversion Mode: {name}")

    def set_bucket(self, bucket_name=None):
        value = bucket_name if bucket_name is not None else self.bucket_name

        bucket_el = self.wait_until_visible(self.STT_BUCKET)
        bucket_el.clear()
        bucket_el.send_keys(value)

        logger.info(f"Bucket name set: {value}")

    def set_bucket_path(self, bucket_dir=None):
        value = bucket_dir if bucket_dir is not None else self.bucket_dir

        dir_el = self.wait_until_visible(self.STT_BUCKET_PATH)
        dir_el.clear()
        dir_el.send_keys(value)

        logger.info(f"Bucket directory set: {value}")

    def scroll_into_view(self, locator):
        try:
            el = self.driver.find_element(*locator)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
            time.sleep(0.3)
            return el
        except Exception:
            return None

    def upload_key_file(self, key_file=None):
        file = key_file if key_file is not None else self.key_file
        self.wait_until_visible(self.STT_KEY_FILE).send_keys(file)
        logger.info(f"Key file uploaded: {file}")

    def get_error_for(self, field):
        locator = self.STT_ERROR_LOCATORS.get(field)
        if not locator:
            raise ValueError(f"No error locator mapped for field: {field}")

        element = self.wait_until_visible(locator)
        return element.text.strip()

    def upload_audio_file(self, audio_file=None):
        file = audio_file if audio_file is not None else self.audio_file

        # Always locate the audio input inside the active modal
        audio_locator = (By.XPATH, f"{self.MODAL_ACTIVE}//input[@name='audioFile']")
        audio_el = self.wait_until_visible(audio_locator)

        # Clear value (if UI reuses the same element)
        self.driver.execute_script("arguments[0].value = '';", audio_el)

        audio_el.send_keys(file)
        logger.info(f"Audio file uploaded in ACTIVE MODAL: {file}")

        return self._handle_modal(self.MODAL_BTN_SUBMIT)

    # -------------------------
    #     MAIN STT FLOW
    # -------------------------
    def configure_stt(self):
        """Full STT configuration workflow."""
        try:
            self.open_tab()
            self.click_edit()

            self.set_speech_to_text()
            # Form setup
            self.set_sample_rate()
            self.set_engine()
            self.set_conversion_mode()
            self.set_bucket()
            self.set_bucket_path()

            # File uploads
            self.upload_key_file()

            # Save settings
            self.click_save()

            # Test flow
            self.click_test()
            self.upload_audio_file()

            # Final confirmation (if any modal appears again)
            self._handle_modal(self.MODAL_BTN_SUBMIT)

            Screenshot.take(self.driver, "STT_success")

        except Exception as e:
            logger.error("STT configuration failed", exc_info=True)
            Screenshot.take(self.driver, "STT_config_error")
            raise

    def reconfigure_stt(self):
        try:
            self.open_tab()
            self.click_edit()

            self.set_speech_to_text()
            self.set_sample_rate()
            self.set_engine()
            self.set_conversion_mode()
            self.set_bucket()
            self.set_bucket_path()

            # ✔ Check if prevKeyFile exists
            prev_key_locator = (By.XPATH, f"{self.STT_PANE_ANCHOR}//input[@name='prevKeyFile']")

            if self.is_element_present(prev_key_locator):
                logger.info("Existing key file found. Clicking Edit button...")
                self.key_file_edit()
                self.upload_key_file()
            else:
                logger.info("No previous key file found. Uploading new key file directly...")
                self.upload_key_file()

            # Save + Test flow
            self.click_save()
            self.click_test()
            self.upload_audio_file()
            self._handle_modal(self.MODAL_BTN_SUBMIT)

        except Exception:
            logger.error("STT configuration failed", exc_info=True)
            Screenshot.take(self.driver, "STT_config_error")
            raise
