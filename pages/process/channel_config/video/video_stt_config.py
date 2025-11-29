
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select




from pages.base_page import BasePage
from pages.common.loader import Loader
from utils.logger import get_logger
from utils.data_reader import load_test_data
from utils.screenshot import Screenshot

full_config = load_test_data("processData.json")




logger = get_logger()


class VideoSTTConfig(BasePage):


    VIDEO_CONFIG_SCOPE = "//div[@id='media-configuration-video']"
    STT_SAMPLE_HERTZ_SELECT = (By.NAME, "sampleHertz")
    STT_ENGINE_SELECT = (By.NAME, "engineNameSTT")

    STT_BUCKET_NAME = (By.NAME, "bucketName")
    STT_BUCKET_PATH = (By.NAME, "bucketDirectory")
    STT_KEY_FILE_INPUT = (By.NAME, "keyFile")
    STT_AUDIO_FILE_INPUT = (By.NAME, "audioFile")
    STT_SUBMIT_BTN = (By.XPATH, "//button[text()='Submit']")
    STT_RADIO_CONVERSION_MODE_MANUAL = (By.XPATH, f"{VIDEO_CONFIG_SCOPE}//*[@value='manualMode']")
    STT_RADIO_CONVERSION_MODE_AUTO = (By.XPATH, f"{VIDEO_CONFIG_SCOPE}//*[@value='autoMode']")
    STT_TEST_BTN = (By.XPATH, f"{VIDEO_CONFIG_SCOPE}//button[text()='Test']")
    STT_RESET_BTN = (By.XPATH, f"{VIDEO_CONFIG_SCOPE}//button[@title='Reset']")
    STT_EDIT_BTN = (By.XPATH, f"{VIDEO_CONFIG_SCOPE}//button[@title='Edit']")
    STT_SAVE_BTN = (By.XPATH, f"{VIDEO_CONFIG_SCOPE}//*[@id='stt-tab-video-pane']//button[@title='Save']")
    STT_TEST_AGAIN_BTN = (By.XPATH, f"{VIDEO_CONFIG_SCOPE}//button[text()='Test Again']")

    CONVERSION_MODE_STT = (By.CSS_SELECTOR, "input[name='conversionMode'][value='manualMode']")
    TAB_STT = (By.XPATH, "//*[@id='stt-tab-video']")

    def __init__(self, driver):
        super().__init__(driver)

        video_config = full_config.get("channel_config", {}).get("video", {})


        stt_config = video_config.get("stt", {})
        self.speech_to_text = stt_config.get("speech_to_text")
        if self.speech_to_text is None:
            self.speech_to_text = None
        else:
            # Safely converts 'true', 'false', "True", "False" to Python True/False
            self.speech_to_text = str(self.speech_to_text).lower() == 'true'

        self.bucket_name = stt_config.get("bucket_name")
        self.buck_dir = stt_config.get("bucket_dir")
        self.stt_keyFile = stt_config.get("keyFile")
        self.sampleRate = stt_config.get("sample_rate", "")
        self.audioFile = stt_config.get("audioFile", "")
        self.keyFile = stt_config.get("keyFile", "")
        self.mode = stt_config.get("conversion_mode", "")
        self.engine=stt_config.get("engine_name")


        self.loader = Loader(driver)

    def config_stt(self):
        try:
            self.tab_stt()

            self.click_edit()
            logger.info("Edit clicked")
            self.wait_for_filter_ui_ready()

            # ENABLE_LABEL = (By.XPATH, "//*[@id='stt-tab-call-pane']/div/form/div/div/div/div/div[1]/div/label[2]/span")
            # label = self.driver.find_element(*ENABLE_LABEL)
            # label.click()
            # print("Clicked on STT label instead of input.")

            try:
                toggle_stt = self.driver.find_element(By.XPATH,
                                                      "//*[@id='stt-tab-video-pane']/div/form/div/div/div/div/div[1]/div/label[2]/span")
                current_state = toggle_stt.is_selected()
                if self.speech_to_text != current_state:
                    toggle_stt.click()
                    print("Action: Toggled stt")
                else:
                    print("Already stt active")
            except Exception as e:
                logger.info("Error when setting speech to text ", e)

            try:
                element = self.wait_until_visible(self.STT_SAMPLE_HERTZ_SELECT)
                select = Select(element)
                select.select_by_value(str(self.sampleRate))
                print(f"Selected Sample Hertz: {self.sampleRate}")
                logger.info(f"Selected Sample Hertz: {self.sampleRate}")

            except Exception as e:
                print("Error selecting sample hertz:", e)
                logger.error("Error selecting sample hertz", exc_info=True)

            sample_dropdown = Select(self.driver.find_element(*self.STT_ENGINE_SELECT))
            sample_dropdown.select_by_value(self.engine)

            print(f"Selected Sample Hertz: {self.engine}")
            logger.info(f"Selected Sample Hertz: {self.engine}")

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

            bucket_name_field = self.driver.find_element(*self.STT_BUCKET_NAME)
            bucket_name_field.clear()
            bucket_name_field.send_keys(self.bucket_name)
            print(f"Entered bucket name: {self.bucket_name}")
            logger.info(f"Entered bucket name: {self.bucket_name}")

            bucket_path_field = self.driver.find_element(*self.STT_BUCKET_PATH)
            bucket_path_field.clear()
            bucket_path_field.send_keys(self.buck_dir)
            print(f"Entered bucket path: {self.buck_dir}")
            logger.info(f"Entered bucket path: {self.buck_dir}")

            # In pages/create_process.py, inside the config_stt method:

            # ... (Previous STT configuration code) ...

            # Fix the file path string by removing the trailing single quote and using a raw string for safety

            key_file_input = self.driver.find_element(*self.STT_KEY_FILE_INPUT)
            key_file_input.send_keys(self.keyFile)  # Use the corrected and safe path
            print(f"✅ File uploaded: {self.keyFile}")
            logger.info(f"File uploaded successfully: {self.keyFile}")

            self.click_save()
            print("Speech To Text configured successfully.")
            logger.info(f"Speech To Text configured successfully: ")
            self.wait_for_filter_ui_ready()

            self.click_test()
            logger.info("Test button has been selected.")

            # Example: click a button inside the modal
            MODAL_DIALOG_LOCATOR = (By.CSS_SELECTOR, 'div[role="dialog"][aria-modal="true"]')

            modal_element = self.wait_until_visible(MODAL_DIALOG_LOCATOR)
            print("Modal element ", modal_element.text)

            # Wait for the modal to be visible

            logger.info("Modal is visible. Proceeding to interact with elements inside.")

            audio_file_input = self.driver.find_element(*self.STT_AUDIO_FILE_INPUT)
            audio_file_input.send_keys(self.audioFile)  # Use the corrected and safe path

            self.click_submit()

            logger.info("audio file uploaded successfully.")
            Screenshot.take(self.driver, f"audio file uploaded")

            self.loader.load()
            self.wait_for_filter_ui_ready()

            self.click_submit()
            logger.info("submitted  successfully.")
            self.loader.load()
            Screenshot.take(self.driver,"stt succesfully configured")

            test_again_btn = self.wait_until_clickable(self.STT_TEST_AGAIN_BTN)




        except Exception as e:
            logger.error(f"Error when configuring STT tab: {e}", exc_info=True)

    def click_save(self):
        self.wait_until_clickable(self.STT_SAVE_BTN).click()

    def click_reset(self):
        self.wait_until_clickable(self.STT_RESET_BTN).click()

    def click_edit(self):
        self.wait_until_clickable(self.STT_EDIT_BTN).click()

    def click_test(self):
        self.wait_until_clickable(self.STT_TEST_BTN).click()

    def click_test_again(self):
        self.wait_until_clickable(self.STT_TEST_AGAIN_BTN).click()

    def click_submit(self):
        submit_button = self.wait_until_clickable(self.STT_SUBMIT_BTN, timeout=10)
        submit_button.click()

    def tab_stt(self):
        tab_stt = self.wait_until_clickable(self.TAB_STT)
        tab_stt.click()
        self.loader.load()
