# ... existing imports ...
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from pages.base_page import BasePage
from pages.common.loader import Loader
from utils.logger import get_logger
from utils.data_reader import load_test_data
from utils.screenshot import Screenshot

logger = get_logger()
full_config = load_test_data("process/create_process.json")


class CallSTTConfig(BasePage):
    # -------------------------
    #        LOCATORS
    # -------------------------
    CALL_CONFIG_SCOPE = "//div[@id='media-configuration-call']"

    STT_SAMPLE_HERTZ_SELECT = (By.NAME, "sampleHertz")
    STT_ENGINE_SELECT = (By.NAME, "engineNameSTT")
    STT_BUCKET_NAME = (By.NAME, "bucketName")
    STT_BUCKET_PATH = (By.NAME, "bucketDirectory")
    STT_KEY_FILE_INPUT = (By.NAME, "keyFile")
    STT_AUDIO_FILE_INPUT = (By.NAME, "audioFile")

    STT_SUBMIT_BTN = (By.XPATH, "//button[text()='Submit']")
    STT_EDIT = (By.XPATH, f"{CALL_CONFIG_SCOPE}//button[@title='Edit']")
    STT_SAVE_BTN = (By.XPATH, f"{CALL_CONFIG_SCOPE}//*[@id='stt-tab-call-pane']//button[@title='Save']")
    STT_TEST_BTN = (By.XPATH, f"{CALL_CONFIG_SCOPE}//button[text()='Test']")
    STT_TEST_AGAIN_BTN = (By.XPATH, f"{CALL_CONFIG_SCOPE}//button[text()='Test Again']")
    STT_RESET_BTN = (By.XPATH, f"{CALL_CONFIG_SCOPE}//button[@title='Reset']")

    # Conversion mode
    STT_RADIO_CONVERSION_MODE_MANUAL = (By.XPATH, f"{CALL_CONFIG_SCOPE}//*[@value='manualMode']")
    STT_RADIO_CONVERSION_MODE_AUTO = (By.XPATH, f"{CALL_CONFIG_SCOPE}//*[@value='autoMode']")
    STT_KEY_FILE_EDIT = (By.XPATH, f"{CALL_CONFIG_SCOPE}//button[@class='imoon icon-edit' and @title='Edit']")
    STT_EDIT_MAIN = (By.XPATH,
                     "//div[@id='stt-tab-call-pane']//button[@class='section_form_acts_btn' and @title='Edit']")

    TAB_STT = (By.XPATH, "//*[@id='stt-tab-call']")

    # Modal locators
    MODAL = (By.CSS_SELECTOR, 'div[role="dialog"][aria-modal="true"]')
    _MODAL_SUBMIT_BUTTON = (By.XPATH, "//div[@role='dialog']//button[text()='Submit']")  # Added locator
    _MODAL_CANCEL_BUTTON = (By.XPATH, "//div[@role='dialog']//button[text()='Cancel']")  # Added locator

    # -------------------------
    #     CONSTRUCTOR
    # -------------------------
    def __init__(self, driver):
        super().__init__(driver)
        self.loader = Loader(driver)

        # Load JSON config cleanly
        cfg = (
            full_config.get("channel_config", {})
            .get("call", {})
            .get("stt", {})
        )

        self.speech_to_text = str(cfg.get("speech_to_text", "")).lower() == "true"
        self.bucket_name = cfg.get("bucket_name")
        self.bucket_dir = cfg.get("bucket_dir")
        self.sample_rate = cfg.get("sample_rate")
        self.engine = cfg.get("engine_name")

        self.key_file = cfg.get("keyFile")
        self.audio_file = cfg.get("audioFile")
        self.mode = cfg.get("conversion_mode")

    # -------------------------
    #     SMALL ACTIONS
    # -------------------------

    def open_stt_tab(self):
        self.wait_until_clickable(self.TAB_STT).click()
        self.loader.load()
        logger.info("STT Tab opened")

    def click_edit(self):
        self.wait_until_clickable(self.STT_EDIT_MAIN).click()
        logger.info("STT Edit clicked")

    def click_save(self):
        self.wait_until_clickable(self.STT_SAVE_BTN).click()
        logger.info("STT Save clicked")

    def click_test(self):
        self.wait_until_clickable(self.STT_TEST_BTN).click()
        logger.info("STT Test Clicked")

    def click_submit(self):
        self.wait_until_clickable(self.STT_SUBMIT_BTN).click()
        logger.info("STT Submit clicked")

    def key_file_edit(self):
        self.wait_until_clickable(self.STT_KEY_FILE_EDIT).click()
        logger.info("STT Key file edit clicked")

    # New method to handle modal submission
    # def click_modal_submit(self):
    #     """Clicks the Submit button within the audio file upload modal and waits for it to disappear."""
    #     self.wait_until_clickable(self._MODAL_SUBMIT_BUTTON, timeout=5).click()
    #     logger.info("Modal Submit button clicked.")
    #     self.wait_invisible(self.MODAL, timeout=10)  # Wait for the modal to disappear
    #     logger.info("Modal dialog disappeared.")

    # -------------------------
    #   SHORT CONFIG HELPERS
    # -------------------------

    def set_speech_to_text(self):
        """
        Toggle STT enable/disable.
        (Click → compare mismatched state → click again only if needed)
        """
        try:
            toggle_xpath = (
                "//*[@id='stt-tab-call-pane']/div/form/div/div/div/div/div[1]/div/label[2]/span"
            )
            toggle = self.driver.find_element(By.XPATH, toggle_xpath)
            current = toggle.is_selected()

            if current != self.speech_to_text:
                toggle.click()
                logger.info("STT toggled")
        except Exception as e:
            logger.error("Error setting STT toggle", exc_info=True)

    def set_sample_rate(self):
        try:
            dropdown = Select(self.wait_until_visible(self.STT_SAMPLE_HERTZ_SELECT))
            dropdown.select_by_value(str(self.sample_rate))
            logger.info(f"Sample rate set: {self.sample_rate}")
        except Exception:
            logger.error("Failed to set sample rate", exc_info=True)

    def set_engine(self):
        dropdown = Select(self.driver.find_element(*self.STT_ENGINE_SELECT))
        dropdown.select_by_value(self.engine)
        logger.info(f"Engine selected: {self.engine}")

    def set_conversion_mode(self):
        if self.mode and self.mode.lower() == 'manualmode':
            mode_locator = self.STT_RADIO_CONVERSION_MODE_MANUAL
            mode_name = "Manual Mode"
        elif self.mode and self.mode.lower() == 'automode':
            mode_locator = self.STT_RADIO_CONVERSION_MODE_AUTO
            mode_name = "Auto Mode"
        else:
            logger.warning(f"Conversion mode '{self.mode}' not recognized or missing. Defaulting to Manual Mode.")
            mode_locator = self.STT_RADIO_CONVERSION_MODE_MANUAL
            mode_name = "Manual Mode (Defaulted)"
        self.driver.find_element(*mode_locator).click()
        print(f"Selected Conversion Mode: {mode_name}")

    def set_bucket(self):
        bucket = self.driver.find_element(*self.STT_BUCKET_NAME)
        bucket.clear()
        bucket.send_keys(self.bucket_name)

        bucket_path = self.driver.find_element(*self.STT_BUCKET_PATH)
        bucket_path.clear()
        bucket_path.send_keys(self.bucket_dir)

    def upload_key_file(self):
        file_input = self.driver.find_element(*self.STT_KEY_FILE_INPUT)
        file_input.send_keys(self.key_file)
        logger.info("Key file uploaded")


    def click_modal_submit(self):
        """Clicks the Submit button within the audio file upload modal and waits for it to disappear."""
        try:
            self.wait_until_clickable(self._MODAL_SUBMIT_BUTTON, timeout=10).click() # Increased timeout
            logger.info("Modal Submit button clicked.")
            self.wait_invisible(self.MODAL, timeout=15) # Increased timeout for modal disappearance
            logger.info("Modal dialog disappeared.")
        except Exception as e:
            logger.error(f"Failed to click modal submit button or modal did not disappear: {e}", exc_info=True)
            Screenshot.take(self.driver, "modal_submit_fail")
            raise # Re-raise to indicate a critical failure

    def upload_audio_file(self):
        """
        Uploads an audio file within the modal dialog.
        Includes explicit waits for the modal and the input field, then submits the modal.
        """
        logger.info("Attempting to upload audio file.")

        # 1. Wait for the modal to be visible
        try:
            modal = self.wait_until_visible(self.MODAL, timeout=20) # Further increased timeout for modal
            logger.info("Modal dialog is visible.")
        except Exception as e:
            logger.error(f"Modal dialog did not become visible: {e}", exc_info=True)
            Screenshot.take(self.driver, "modal_not_visible_for_audio_upload")
            raise

        # 2. Construct the locator for the audio input field *relative to the modal element*
        #    This is crucial for robustly finding elements inside a specific modal instance.
        #    The HTML shows the input has name='audioFile' and is of type='file'
        audio_input_locator_within_modal = (By.XPATH, f"{self.MODAL[1]}//input[@name='audioFile' and @type='file']")

        # 3. Wait for the audio file input field to be clickable within the modal
        try:
            input_el = self.wait_until_clickable(audio_input_locator_within_modal, timeout=15) # Further increased timeout
            logger.info(f"Audio file input field '{audio_input_locator_within_modal}' in modal is clickable.")
        except Exception as e:
            logger.error(f"Audio file input field did not become clickable: {e}", exc_info=True)
            Screenshot.take(self.driver, "audio_input_not_clickable")
            raise

        # 4. Send the file path to the input element
        try:
            # Ensure the file exists before attempting to send_keys
            import os
            if not os.path.exists(self.audio_file):
                logger.error(f"Audio file path does not exist: {self.audio_file}")
                raise FileNotFoundError(f"Audio file not found: {self.audio_file}")

            input_el.send_keys(self.audio_file)
            logger.info(f"Audio file '{self.audio_file}' sent to input field.")

            # 5. Click the Submit button on the modal to close it
            self.click_modal_submit()

        except Exception as e:
            logger.error(f"Failed to send keys to audio file input or submit modal: {e}", exc_info=True)
            Screenshot.take(self.driver, "send_keys_audio_fail")
            raise

        logger.info("Audio file upload process completed successfully.")


    # -------------------------
    #       MAIN WORKFLOW
    # -------------------------

    def configure_stt(self):
        try:
            self.open_stt_tab()
            self.click_edit()

            # The 'wait_for_filter_ui_ready' might be specific to other filters.
            # If the STT config UI is loaded via different means, you might need a different wait here.
            # self.wait_for_filter_ui_ready()


            self.set_speech_to_text()
            self.wait_until_visible(self.STT_SAMPLE_HERTZ_SELECT)  # Wait for a known STT element
            self.set_sample_rate()
            self.set_engine()
            self.set_conversion_mode()


            self.set_bucket()

            self.upload_key_file()

            self.click_save()
            self.loader.load()

            # Test flow
            self.click_test()
            # Again, wait for the modal to appear for audio upload, not filter UI
            # self.wait_for_filter_ui_ready()
            self.upload_audio_file()  # This now handles submitting the modal

            # The final click_submit here should be for the main STT config, if any
            # self.click_submit()

            Screenshot.take(self.driver, "STT success")

        except Exception as e:
            logger.error("Error configuring STT tab", exc_info=True)
