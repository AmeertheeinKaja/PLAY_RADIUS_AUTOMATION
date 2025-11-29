import time

from selenium.common import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select




from pages.base_page import BasePage
from pages.common.loader import Loader
from utils.logger import get_logger
from utils.data_reader import load_test_data
from utils.screenshot import Screenshot

full_config = load_test_data("processData.json")




logger = get_logger()



class ChatSAConfig(BasePage):
    CALL_CONFIG_SCOPE = "//div[@id='media-configuration-chat']"


    TAB_SENTIMENT_ANALYSIS = (By.XPATH, f"{CALL_CONFIG_SCOPE}//button[@id='sa-tab-chat']")

    TOGGLE_SA = (By.XPATH,
                 f"{CALL_CONFIG_SCOPE}//*[@id='sa-tab-chat-pane']/div/form/div/div/div[2]/div/div[1]/div/label[2]/span")
    SA_SAVE_BTN = (By.XPATH, f"{CALL_CONFIG_SCOPE}//*[@id='sa-tab-chat-pane']//button[@title='Save']")
    SA_RESET_BTN = (By.XPATH, f"{CALL_CONFIG_SCOPE}//button[@title='Reset']")
    SA_EDIT_BTN = (By.XPATH,
                   f"{CALL_CONFIG_SCOPE}//*[@id='sa-tab-chat-pane']/div/form/div/div/div[2]/div/div[2]/div/div/button")
    SA_SELECT_ENGINE = (By.XPATH, f"{CALL_CONFIG_SCOPE}//select[@name='engineNameSA']")
    SA_RADIO_CONVERSION_MODE = (By.XPATH, f"{CALL_CONFIG_SCOPE}//*[@id='manualModeSa_chat']")
    SA_KEY_FILE_INPUT = (By.NAME, "keyFile")
    SA_TEST_BTN = (By.XPATH, f"{CALL_CONFIG_SCOPE}//button[text()='Test']")
    SA_TEXT_AREA = (By.XPATH, "//*[@id='sentiment_text']")
    SA_SUBMIT = (By.XPATH, "//button[text()='Submit']")
    SA_CANCEL = (By.XPATH, "//button[text()='Cancel']")
    SA_RADIO_CONVERSION_MODE_MANUAL = (By.XPATH, f"{CALL_CONFIG_SCOPE}//*[@id='manualModeSa_chat']")
    SA_RADIO_CONVERSION_MODE_AUTO = (By.XPATH, f"{CALL_CONFIG_SCOPE}//*[@id='autoModeSa_chat']")
    MODAL_TITLE = (By.XPATH, "//div[@class='modal-title h4']//span")
    SA_MODAL_SUBMIT = (By.XPATH, "//button[text()='Submit']")
    SA_TEST_AGAIN_BTN = (By.XPATH, f"{CALL_CONFIG_SCOPE}//button[text()='Test Again']")



    def __init__(self, driver):
        super().__init__(driver)
        self.loader = Loader(self.driver)

        call_config = full_config.get("channel_config", {}).get("call", {})
        sa_config = call_config.get("sa", {})
        self.sentimentAnalysis = sa_config.get("sentimentAnalysis")
        if self.sentimentAnalysis is None:
            self.sentimentAnalysis = None
        else:
            # Safely converts 'true', 'false', "True", "False" to Python True/False
            self.sentimentAnalysis = str(self.sentimentAnalysis).lower() == 'true'
        self.engine = sa_config.get("engine_name", "")

        self.keyFile = sa_config.get("keyFile", "")
        self.sentiment_text = sa_config.get("sentiment_text", "")
        self.mode = sa_config.get("conversion_mode", "")

    def config_sentiment_analysis(self):
        try:
            self.tab_stt()
            logger.info("sentiment tab clicked")

            self.click_edit()
            print("Edit clicked")
            self.wait_for_filter_ui_ready()

            try:
                toggle_sa = self.driver.find_element(By.XPATH,
                                                     "//*[@id='sa-tab-chat-pane']/div/form/div/div/div[2]/div/div[1]/div/label[2]/span")
                current_state = toggle_sa.is_selected()
                if self.sentimentAnalysis != current_state:
                    toggle_sa.click()
                    logger.info("Action: Toggled sentiment analysis")
                else:
                    logger.info("Already sa active")
            except Exception as e:
                print("Error when setting sentiment analysis ", e)

            sample_dropdown = Select(self.driver.find_element(*self.SA_SELECT_ENGINE))
            sample_dropdown.select_by_value(self.engine)

            print(f"Selected Engine: {self.engine}")
            logger.info(f"Selected Engine: {self.engine}")

            if self.mode and self.mode.lower() == 'manualmode':
                mode_locator = self.SA_RADIO_CONVERSION_MODE_MANUAL
                mode_name = "Manual Mode"
            elif self.mode and self.mode.lower() == 'automode':
                mode_locator = self.SA_RADIO_CONVERSION_MODE_AUTO
                mode_name = "Auto Mode"
            else:
                logger.warning(f"Conversion mode '{self.mode}' not recognized or missing. Defaulting to Manual Mode.")
                mode_locator = self.SA_RADIO_CONVERSION_MODE_MANUAL
                mode_name = "Manual Mode (Defaulted)"

            self.driver.find_element(*mode_locator).click()
            print(f"Selected Conversion Mode: {mode_name}")

            key_file_input = self.driver.find_element(*self.SA_KEY_FILE_INPUT)
            key_file_input.send_keys(self.keyFile)  # Use the corrected and safe path

            logger.info(f"File uploaded successfully: {self.keyFile}")
            self.wait_for_filter_ui_ready()
            logger.info("GOing to save")

            self.click_save()
            Screenshot.take(self.driver,"Config details saved successfully")
            logger.info(f"Sentiment Analysis configured successfully: {self.sentimentAnalysis}")

            self.click_test()
            logger.info("Test button has been selected.")
            #
            # # Wait for modal to appear and print the title
            try:
                logger.info("Attempting to open modal...")

                modal_locator = (By.XPATH,
                                 "//div[@role='dialog' and contains(@class,'modal') and contains(@class,'show')]")
                self.wait_until_clickable(modal_locator)

                logger.info(" modal is visible.")

                # Wait for textarea inside modal
                text_area = self.wait_until_visible(self.SA_TEXT_AREA, timeout=10)
                logger.info("Text area found, entering sentiment text...")

                text_area.clear()
                text_area.send_keys(self.sentiment_text)
                logger.debug(f"Sentiment text entered: {self.sentiment_text}")



                # First submit inside modal
                self.click_submit()
                logger.info("First modal submit clicked.")
                self.loader.load()

                # Final modal confirmation (if applicable)
                self.click_submit()
                logger.info("Final modal submit clicked.")
                self.loader.load()
                Screenshot.take(self.driver,"Sentiment Analysis saved successfully")

                logger.info(" Modal form submitted successfully.")


            except Exception as e:
                logger.exception(" Unexpected error while handling modal: %s", e)
                raise

        except Exception as e:
            logger.error("Error when configuring sentiment analysis mode", exc_info=True)

    def click_save(self):
        self.wait_until_clickable(self.SA_SAVE_BTN).click()

    def click_reset(self):
        self.wait_until_clickable(self.SA_RESET_BTN).click()

    def click_edit(self):
        self.wait_until_clickable(self.SA_EDIT_BTN).click()

    def click_test(self):
        self.wait_until_clickable(self.SA_TEST_BTN).click()

    def click_test_again(self):
        self.wait_until_clickable(self.SA_TEST_AGAIN_BTN).click()

    def click_submit(self):
        submit_button = self.wait_until_clickable(self.SA_SUBMIT, timeout=10)
        submit_button.click()

    def tab_stt(self):
        tab_stt = self.wait_until_clickable(self.TAB_SENTIMENT_ANALYSIS)
        tab_stt.click()
        self.loader.load()
        