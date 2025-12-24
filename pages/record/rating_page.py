import random
import time

from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.common.loader import Loader
from pages.common.submit_search_filter import SubmitFilterSearch
from utils.logger import get_logger
from utils.screenshot import Screenshot

logger = get_logger(__name__)


class RatingPage(BasePage):
    _CALCULATE_BTN = (By.XPATH, "//button[normalize-space()='Calculate Score']")
    _RESET_BTN = (By.XPATH, "//button[normalize-space()='Reset']")
    _SUBMIT_BTN = (By.XPATH, "//button[normalize-space()='Submit']")
    _NAV_TABS = (By.CSS_SELECTOR, "ul.nav-tabs li span.nav-link")
    _QUESTIONS = (By.CSS_SELECTOR, "li.rate_sect_item")
    _OPTIONS = ".rate_acts_btn"
    _RATING_SUBMIT_SUCCESS="Rating saved successfully"
    _RATING_UPDATE_SUCCESS="Rating updated successfully"

    def __init__(self, driver):
        super().__init__(driver)
        self.action = SubmitFilterSearch(driver)
        self.loader = Loader(driver)
        self.last_toast = None
        logger.info("RatingPage initialized")

    # -------------------------------
    # NAV TABS
    # -------------------------------
    def get_all_tabs(self):
        logger.info("Fetching all rating nav tabs")
        tabs = self.find_elements(self._NAV_TABS)
        logger.info(f"Found {len(tabs)} rating tabs")
        return tabs

    def switch_to_tab(self, tab_name):
        logger.info(f"Attempting to switch to rating tab: {tab_name}")

        try:
            for tab in self.get_all_tabs():
                if tab.text.strip() == tab_name:
                    tab.click()
                    self.loader.load()
                    logger.info(f"Successfully switched to tab: {tab_name}")
                    return True

            logger.warning(f"Rating tab not found: {tab_name}")
            Screenshot.take(self.driver, f"rating_tab_not_found_{tab_name}")
            return False

        except Exception as e:
            logger.error(f"Failed while switching tab: {tab_name} | Error: {e}")
            Screenshot.take(self.driver, f"switch_tab_error_{tab_name}")
            raise

    # -------------------------------
    # QUESTIONS & ANSWERS
    # -------------------------------
    def get_questions(self):
        logger.info("Fetching all rating questions")
        questions = self.find_elements(self._QUESTIONS)
        logger.info(f"Total questions found: {len(questions)}")
        return questions

    def answer_all_questions(self, strategy="first"):
        logger.info(f"Answering all questions using strategy: {strategy}")

        questions = self.get_questions()

        if not questions:
            logger.warning("No rating questions found")
            Screenshot.take(self.driver, "no_rating_questions")
            return

        for index, q in enumerate(questions, start=1):
            try:
                question_text = q.text.strip()
                logger.info(f"Processing Question {index}: {question_text}")

                options = q.find_elements(By.CSS_SELECTOR, self._OPTIONS)

                if not options:
                    logger.warning(f"No options found for question {index}")
                    Screenshot.take(self.driver, f"no_options_q{index}")
                    continue

                if strategy == "first":
                    options[0].click()
                    logger.info(f"Selected first option for question {index}")

                elif strategy == "random":
                    selected = random.choice(options)
                    selected.click()
                    logger.info(
                        f"Random option selected for question {index}: {selected.text}"
                    )

            except Exception as e:
                logger.error(f"Failed to answer question {index} | Error: {e}")
                Screenshot.take(self.driver, f"answer_question_failed_q{index}")
                raise

    # -------------------------------
    # BUTTON STATES
    # -------------------------------
    def is_button_enabled(self, locator):
        try:
            enabled = self.wait_until_visible(locator).is_enabled()
            logger.info(f"Button {locator} enabled status: {enabled}")
            return enabled

        except Exception as e:
            logger.error(f"Failed to check button enabled state | Error: {e}")
            Screenshot.take(self.driver, "button_state_check_failed")
            raise

    def calculate_score(self):
        logger.info("Clicking Calculate Score button")

        try:
            btn = self.wait_until_visible(self._CALCULATE_BTN)
            btn.click()
            self.loader.load()
            logger.info("Calculate Score clicked successfully")

        except Exception as e:
            logger.error(f"Failed to click Calculate Score | Error: {e}")
            Screenshot.take(self.driver, "calculate_score_failed")
            raise

    def submit_rating(self):
        logger.info("Submitting rating")

        # Clear old toast
        self.last_toast = None

        submit_btn = self.wait_until_visible(self._SUBMIT_BTN)

        if not submit_btn.is_enabled():
            Screenshot.take(self.driver, "submit_button_disabled")
            raise AssertionError("Submit button is disabled")

        submit_btn.click()
        self.loader.load()

        toast = self.toast_text()

        if toast not in (
                self._RATING_SUBMIT_SUCCESS,
                self._RATING_UPDATE_SUCCESS
        ):
            Screenshot.take(self.driver, "unexpected_toast")
            raise AssertionError(f"Unexpected toast message: {toast}")

        logger.info(f"Rating action successful: {toast}")

    def toast_text(self):
        try:
            txt = self.capture_toast()
        except Exception:
            time.sleep(0.3)
            try:
                txt = self.capture_toast()
            except:
                txt = ""

        self.last_toast = txt
        logger.info(f"[toast_text] Toast captured: {txt}")
        return txt
