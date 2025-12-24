import time

from selenium.common import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select




from pages.base_page import BasePage
from pages.common.loader import Loader
from utils.logger import get_logger

from utils.screenshot import Screenshot






logger = get_logger()



class VideoSAConfig(BasePage):
    VIDEO_CONFIG_SCOPE = "//div[@id='media-configuration-video']"


    TAB_SENTIMENT_ANALYSIS = (By.XPATH, f"{VIDEO_CONFIG_SCOPE}//button[@id='sa-tab-video']")

    TOGGLE_SA = (By.XPATH,
                 f"{VIDEO_CONFIG_SCOPE}//*[@id='sa-tab-video-pane']/div/form/div/div/div[2]/div/div[1]/div/label[2]/span")
    SA_TOGGLE_INPUT = (By.XPATH, "//input[@name='isEnableSA']")


    SA_SAVE_BTN = (By.XPATH, f"{VIDEO_CONFIG_SCOPE}//*[@id='sa-tab-video-pane']//button[@title='Save']")
    SA_RESET_BTN = (
        By.XPATH,
        "//div[@id='sa-tab-video-pane']//button[@title='Reset']"
    )
    SA_EDIT_BTN = (By.XPATH,
                   f"{VIDEO_CONFIG_SCOPE}//*[@id='sa-tab-video-pane']/div/form/div/div/div[2]/div/div[2]/div/div/button")
    SA_TEST_EDIT_BTN = (By.XPATH, f"{VIDEO_CONFIG_SCOPE}//*[@id='sa-tab-video-pane']//button[text()='Test']/following-sibling::button[@title='Edit']")
    SA_EDIT_KEY_FILE = (By.XPATH, f"{VIDEO_CONFIG_SCOPE}//*[@id='sa-tab-video-pane']//input[@name='prevKeyFile']/following-sibling::button[@title='Edit']")
    SA_SELECT_ENGINE = (By.XPATH, f"{VIDEO_CONFIG_SCOPE}//select[@name='engineNameSA']")
    SA_RADIO_CONVERSION_MODE = (By.XPATH, f"{VIDEO_CONFIG_SCOPE}//*[@id='manualModeSa_chat']")
    SA_KEY_FILE_INPUT = (By.NAME, "keyFile")
    SA_TEST_BTN = (By.XPATH, f"{VIDEO_CONFIG_SCOPE}//button[text()='Test']")
    SA_TEXT_AREA = (By.XPATH, "//*[@id='sentiment_text']")
    SA_SUBMIT = (By.XPATH, "//button[text()='Submit']")
    SA_CANCEL = (By.XPATH, "//button[text()='Cancel']")
    SA_RADIO_CONVERSION_MODE_MANUAL = (By.XPATH, f"{VIDEO_CONFIG_SCOPE}//*[@id='manualModeSa_video']")
    SA_RADIO_CONVERSION_MODE_AUTO = (By.XPATH, f"{VIDEO_CONFIG_SCOPE}//*[@id='autoModeSa_video']")
    MODAL_TITLE = (By.XPATH, "//div[@class='modal-title h4']//span")
    SA_MODAL_SUBMIT = (By.XPATH, "//button[text()='Submit']")
    SA_TEST_AGAIN_BTN = (By.XPATH, f"{VIDEO_CONFIG_SCOPE}//button[text()='Test Again']")
    MODAL_ACTIVE = '(//div[@role="dialog" and contains(@class,"show")])[last()]'
    MODAL_BTN_SUBMIT = (By.XPATH, f"{MODAL_ACTIVE}//button[text()='Submit']")
    MODAL_BTN_CLOSE = (By.XPATH, f"{MODAL_ACTIVE}//button[text()='Close']")
    MODAL_BTN_TEST_AGAIN = (By.XPATH, f"{MODAL_ACTIVE}//button[text()='Test Again']")

    EDIT_LOC_MAIN = (By.XPATH, "//div[@id='sa-tab-video-pane']//button[@title='Edit']")
    EDIT_LOC_TEST = (By.XPATH,
                     "//div[@id='sa-tab-video-pane']//button[text()='Test']/following-sibling::button[@title='Edit']")
    EDIT_LOC_TEST_AGAIN = (By.XPATH,
                           "//div[@id='sa-tab-video-pane']//button[text()='Test Again']/following-sibling::button[@title='Edit']")

    SA_EDIT_TOGGLE_INPUT = (By.XPATH,
        f"{VIDEO_CONFIG_SCOPE}//input[@name='isEnableSA']"
    )

    EDIT_TOGGLE_SA = (By.XPATH,
        f"{VIDEO_CONFIG_SCOPE}//input[@name='isEnableSA']/following-sibling::span"
    )
    BTN_EDIT_MAIN = (By.XPATH,
                     "//div[@id='sa-tab-video-pane']//button[@class='section_form_acts_btn' and @title='Edit']")
    SUCCESS_UPDATE_MESSAGE="Sentiment analysis updated successfully"
    SUCCESS_CONVERT_MESSAGE="Sentiment analysis converted successfully"
    SUCCESS_TEST_MESSAGE="Sentiment analysis tested successfully"
    SA_ERROR_LOCATORS = {
        "engine": (
            By.XPATH,
            "//select[@name='engineNameSA']/following-sibling::div[contains(@class,'invalid-tooltip')]"
        ),
        "key_file": (
            By.XPATH,
            "//input[@name='keyFile']/following-sibling::div[contains(@class,'invalid-tooltip')]"
        ),
        "sentiment_text": (
            By.XPATH,
            "//textarea[@id='sentiment_text']/following-sibling::div[contains(@class,'invalid-tooltip')]"
        )
    }

    def __init__(self, driver,sentiment_analysis=None,engine_name=None,conversion_mode=None,keyFile=None,sentiment_text=None):
        super().__init__(driver)
        self.loader = Loader(self.driver)



        self.sentimentAnalysis = sentiment_analysis
        if self.sentimentAnalysis is None:
            self.sentimentAnalysis = None
        else:
            # Safely converts 'true', 'false', "True", "False" to Python True/False
            self.sentimentAnalysis = str(self.sentimentAnalysis).lower() == 'true'
        self.engine = engine_name

        self.keyFile = keyFile
        self.sentiment_text = sentiment_text
        self.mode =conversion_mode
        self.last_toast = None

    def open_tab(self):
        self.tab_sa()
        logger.info("SA tab opened.")

    def _get_sa_input_and_clickable(self):
        input_locator = self.SA_TOGGLE_INPUT
        span_locator = (By.XPATH, "//input[@name='isEnableSA']/following-sibling::span")

        input_el = self.wait_until_present(input_locator)

        try:
            span_el = self.driver.find_element(*span_locator)
        except:
            span_el = input_el  # fallback if span not found

        return input_el, span_el

    def enable_sa(self):
        input_el, clickable = self._get_sa_input_and_clickable()

        is_disabled = input_el.get_attribute("disabled") is not None
        is_checked = input_el.is_selected()

        if is_disabled:
            logger.info("SA toggle disabled — cannot enable.")
            return

        if is_checked:
            logger.info("SA already enabled, no action.")
            return

        clickable.click()
        logger.info("SA enabled.")
        self.loader.load()

    def disable_sa(self):
        input_el, clickable = self._get_sa_input_and_clickable()

        is_disabled = input_el.get_attribute("disabled") is not None
        is_checked = input_el.is_selected()

        if is_disabled:
            logger.info("SA toggle disabled — cannot disable.")
            return

        if not is_checked:
            logger.info("SA already disabled, no action.")
            return

        clickable.click()
        logger.info("SA disabled.")
        self.loader.load()

    def wait_for_sa_form(self):
        if not self.is_element_present(self.SA_SELECT_ENGINE):
            logger.warning("SA fields missing. Backend has no SA config. Running minimal save.")
            self.minimal_sa_save()
            return False

        self.wait_until_present(self.SA_SELECT_ENGINE, timeout=15)
        return True

    def minimal_sa_save(self):
        self.toggle_sa(True)
        self.click_save()
        logger.info("Minimal SA save completed (toggle only).")

    def toggle_sa(self, sentiment_value=None):
        # JSON override
        if sentiment_value is None:
            sentiment_value = self.sentimentAnalysis

        if sentiment_value is None:
            logger.info("No SA toggle instruction provided — skipping.")
            return

        input_el, _ = self._get_sa_input_and_clickable()
        current = input_el.is_selected()

        if current == bool(sentiment_value):
            logger.info("SA already in desired state — no change.")
            return

        if sentiment_value:
            self.enable_sa()
        else:
            self.disable_sa()

    def select_engine(self):
        sample_dropdown = Select(self.driver.find_element(*self.SA_SELECT_ENGINE))
        sample_dropdown.select_by_value(self.engine)
        self.loader.load()
        print(f"Selected Engine: {self.engine}")
        logger.info(f"Selected Engine: {self.engine}")

    def choose_conversion_mode(self):
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


    def key_file_input(self):
        key_file_input = self.driver.find_element(*self.SA_KEY_FILE_INPUT)
        key_file_input.send_keys(self.keyFile)  # Use the corrected and safe path

        logger.info(f"File uploaded successfully: {self.keyFile}")

    def add_text_area_input(self):
        textarea_locator = (By.XPATH, f"{self.MODAL_ACTIVE}//*[@id='sentiment_text']")

        text_area = self.wait_until_clickable(textarea_locator, timeout=10)
        logger.info("Modal text area found, entering sentiment text...")

        self.driver.execute_script("arguments[0].value = '';", text_area)
        text_area.clear()
        text_area.send_keys(self.sentiment_text)

        logger.debug(f"Sentiment text entered: {self.sentiment_text}")

    def click_dynamic_edit(self, locators, load=True):
        """
        Try clicking whichever Edit button is visible among the provided locators.
        """
        for locator in locators:
            try:
                if self.is_element_present(locator):
                    el = self.wait_until_clickable(locator)
                    el.click()
                    if load:
                        self.loader.load()
                    logger.info(f"Clicked Edit button: {locator}")
                    return True
            except Exception:
                continue

        raise Exception("No usable Edit button found in any locator")

    def click_modal_submit(self):
        submit_locator = (By.XPATH, f"{self.MODAL_ACTIVE}//button[text()='Submit']")
        btn = self.wait_until_clickable(submit_locator)
        btn.click()
        self.loader.load()
        self.toast_text()

    def _handle_modal(self, button_locator):
        """Generic modal button handler."""
        try:
            self.loader.load()
            self._safe_click(button_locator, load=False)
            return self.toast_text()
        except Exception:
            Screenshot.take(self.driver, "modal_handling_failed")
            raise

    def _safe_click(self, locator, load=True):
        element = self.wait_until_clickable(locator)
        element.click()
        if load:
            self.loader.load()

    def config_sa(self):
        try:
            self.tab_sa()
            logger.info("sentiment tab clicked")

            self.click_edit()
            print("Edit clicked")
            self.loader.load()

            self.toggle_sa()
            self.select_engine()
            self.choose_conversion_mode()
            self.key_file_input()


            logger.info("Going to save")

            self.click_save()
            Screenshot.take(self.driver,"Config details saved successfully")
            logger.info(f"Sentiment Analysis configured successfully: {self.sentimentAnalysis}")
            self.click_test()
            self.add_text_area_input()
            self.click_submit()
            self.loader.load()
            self.click_submit()

        except Exception as e:
            logger.error("Error when configuring sentiment analysis mode", exc_info=True)

    def reconfig_sa(self):

        self.tab_sa()
        logger.info("sentiment tab clicked")

        # single edit
        self.click_edit()
        logger.info("Re-configuring sentiment analysis mode")

        self.edit_toggle_sa()
        self.get_edit_toggle_state()

        self.select_engine()
        self.choose_conversion_mode()

        self.key_file_edit()
        self.key_file_input()

        self.click_save()
        self.toast_text()
        Screenshot.take(self.driver, "Config details saved successfully")
        logger.info(f"Sentiment Analysis configured successfully: {self.sentimentAnalysis}")
        self.click_test()
        self.add_text_area_input()
        self.click_modal_submit()  # instead of click_submit()
        self.loader.load()
        self.click_modal_submit()  # second confirm
        logger.info("Reconfiguration completed")

    def is_conversion_mode_invalid(self):
        manual = self.driver.find_element(*self.SA_RADIO_CONVERSION_MODE_MANUAL)
        auto = self.driver.find_element(*self.SA_RADIO_CONVERSION_MODE_AUTO)

        return (
                "is-invalid" in manual.get_attribute("class") or
                "is-invalid" in auto.get_attribute("class")
        )

    def load_modal(self):
        try:
            logger.info("Attempting to open modal...")

            modal_locator = (By.XPATH,
                             "//div[@role='dialog' and contains(@class,'modal') and contains(@class,'show')]")
            self.wait_until_clickable(modal_locator)

            logger.info("Import Version modal is visible.")

        except TimeoutException as te:
            logger.error(" Timeout while waiting for modal elements: %s", te)
        except NoSuchElementException as ne:
            logger.error(" Could not locate modal element: %s", ne)
        except ElementClickInterceptedException as ee:
            logger.error("⚠Element not clickable at the moment: %s", ee)
        except Exception as e:
            logger.exception(" Unexpected error while handling modal: %s", e)
            raise

    def click_save(self):
        self.scroll_and_click(self.SA_SAVE_BTN)
        self.toast_text()

    def click_reset(self):
        self.wait_until_clickable(self.SA_RESET_BTN).click()

    def click_edit(self):
        EDIT_BUTTONS = [
            self.EDIT_LOC_MAIN,
            self.EDIT_LOC_TEST,
            self.EDIT_LOC_TEST_AGAIN,
        ]

        self.click_dynamic_edit(EDIT_BUTTONS)
        logger.info("Correct Edit button clicked based on current UI state")

    def click_edit_test(self):
        self.wait_until_clickable(self.SA_TEST_EDIT_BTN).click()

    def click_test(self):
        self.scroll_and_click(self.SA_TEST_BTN)

    def click_test_again(self):
        self.wait_until_clickable(self.SA_TEST_AGAIN_BTN).click()

    def click_submit(self):
        submit_button = self.wait_until_clickable(self.SA_SUBMIT, timeout=10)
        submit_button.click()
        self.toast_text()

    def key_file_edit(self):
        try:
            self.wait_until_clickable(self.SA_EDIT_KEY_FILE).click()
        except Exception as e:
            logger.error("Error when opening key file: %s", e)

    def tab_sa(self):
        self.scroll_and_click(self.TAB_SENTIMENT_ANALYSIS)
        logger.info("SA tab clicked through scroll helper")
        self.loader.load()

    def toast_text(self):
        txt = self.capture_toast()
        self.last_toast = txt
        logger.info(f"Toast: {txt}")
        return txt

    def get_sa_error(self, field):
        locator = self.SA_ERROR_LOCATORS.get(field)
        if not locator:
            raise ValueError(f"No SA error locator for field: {field}")
        return self.wait_until_visible(locator).text.strip()

    def get_edit_toggle_state(self):
        el = self.wait_until_present(self.SA_EDIT_TOGGLE_INPUT)
        selected = el.is_selected()
        disabled = el.get_attribute("disabled") is not None

        logger.info(f"Toggle -> selected={selected}, disabled={disabled}")
        return selected, disabled

    def edit_toggle_sa(self, sentiment_value=None):

        # Hardcode to enable always for testing
        sentiment_value = True

        el = self.wait_until_present(self.SA_EDIT_TOGGLE_INPUT)

        current = el.is_selected()
        disabled = el.get_attribute("disabled") is not None

        logger.info(f"Toggle -> HARD ENABLE MODE: current={current} disabled={disabled}")

        if disabled:
            logger.info("Toggle disabled, cannot enable")
            return

        if current:
            logger.info("Toggle already ON")
            return

        # Click span after checkbox
        clickable = self.wait_until_clickable(self.EDIT_TOGGLE_SA)
        clickable.click()
        logger.info("Toggle turned ON by force")
        self.loader.load()

    def get_selected_mode(self):
        if self.driver.find_element(*self.SA_RADIO_CONVERSION_MODE_MANUAL).is_selected():
            return "manualmode"
        if self.driver.find_element(*self.SA_RADIO_CONVERSION_MODE_AUTO).is_selected():
            return "automode"
