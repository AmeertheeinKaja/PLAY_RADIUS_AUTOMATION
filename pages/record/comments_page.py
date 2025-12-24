import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from utils.logger import get_logger
from pages.base_page import BasePage
from utils.screenshot import Screenshot

logger = get_logger(__name__)


class CommentsPage(BasePage):

    ADD_TEXT_AREA = (By.XPATH, "//textarea[@formcontrolname='agentNote']")
    COMMENT_SUBMIT_BTN = (
        By.XPATH,
        "//textarea[@formcontrolname='agentNote']/ancestor::form//button[@type='submit']"
    )
    CLEAR_BTN = (
        By.XPATH,
        "//textarea[@formcontrolname='agentNote']/ancestor::form//button[contains(text(),'Clear')]"
    )

    MODAL_OK_BTN = (By.XPATH, "//button[contains(text(), 'Ok')]")
    MODAL_CANCEL_BTN = (By.XPATH, "//button[contains(text(), 'Cancel')]")

    COMMENT_ROW = "//div[contains(@class,'anc_box')]"

    def __init__(self, driver):
        super().__init__(driver)
        self.last_toast = None

    # ----------------------------------------------------------
    # COMMENT ENTRY
    # ----------------------------------------------------------
    def type_comment(self, message):
        try:
            box = self.wait_until_visible(self.ADD_TEXT_AREA)
            box.clear()
            box.send_keys(message)
            logger.info(f"[type_comment] Entered comment text: {message}")
        except Exception as e:
            logger.error(f"[type_comment] Failed entering text. Error: {e}")
            Screenshot.take("comment_typing_failed")

    def click_submit(self):
        try:
            self.wait_until_clickable(self.COMMENT_SUBMIT_BTN).click()
            logger.info("[click_submit] Submit clicked.")

            self.toast_text()
            Screenshot.take("comment_submitted")

        except Exception as e:
            logger.error(f"[click_submit] Failed. Error: {e}")
            Screenshot.take("comment_submit_failed")

    def click_clear(self):
        try:
            self.wait_until_clickable(self.CLEAR_BTN).click()
            logger.info("[click_clear] Clear clicked.")
        except Exception as e:
            logger.error(f"[click_clear] Failed to click clear. Error: {e}")
            Screenshot.take("clear_btn_failed")

    # ----------------------------------------------------------
    # TOAST CAPTURE
    # ----------------------------------------------------------
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

    # ----------------------------------------------------------
    # SHARED COMMENT LOCATOR METHOD
    # ----------------------------------------------------------
    def _first_comment_row_by_text(self, text):
        """
        Always match first comment that contains given text.
        """

        xpath = (
            "(//span[contains(@class,'col-9') and "
            "contains(normalize-space(), '{}')]/ancestor::div[contains(@class,'anc_box')])[1]"
        ).format(text[:60])

        try:
            row = self.wait_until_visible((By.XPATH, xpath))

            # scroll + hover
            self.driver.execute_script("arguments[0].scrollIntoView(true);", row)
            ActionChains(self.driver).move_to_element(row).pause(0.3).perform()

            logger.info(f"[row locator] Located comment row for: {text}")
            return row

        except Exception as e:
            logger.error(f"[row locator] Failed to locate row for '{text}' Error: {e}")
            Screenshot.take("row_not_found")
            return None

    # ----------------------------------------------------------
    # EDIT COMMENT
    # ----------------------------------------------------------
    def edit_comment(self, comment_text):

        try:
            row = self._first_comment_row_by_text(comment_text)
            if row is None:
                return False

            edit_xpath = (
                ".//following-sibling::div[contains(@class,'anc_box_action')]"
                "//button[@id='editBtn']"
            )

            edit_btn = row.find_element(By.XPATH, edit_xpath)
            edit_btn.click()

            logger.info(f"[edit_comment] Editing -> {comment_text}")

            return True

        except Exception as e:
            logger.error(f"[edit_comment] Failed to edit '{comment_text}'. Error: {e}")
            Screenshot.take("edit_failed")
            return False

    # ----------------------------------------------------------
    # DELETE COMMENT
    # ----------------------------------------------------------
    def delete_comment(self, comment_text):

        try:
            row = self._first_comment_row_by_text(comment_text)
            if row is None:
                return False

            delete_xpath = (
                ".//following-sibling::div[contains(@class,'anc_box_action')]"
                "//button[@id='deleteBtn']"
            )

            delete_btn = row.find_element(By.XPATH, delete_xpath)
            delete_btn.click()
            logger.info(f"[delete_comment] Delete clicked for '{comment_text}'")

            self._confirm_delete()

            return True

        except Exception as e:
            logger.error(f"[delete_comment] Failed deleting '{comment_text}'. Error: {e}")
            Screenshot.take("delete_failed")
            return False

    # ----------------------------------------------------------
    # MODAL CONFIRMATION
    # ----------------------------------------------------------
    def _confirm_delete(self):
        try:
            btn = self.wait_until_clickable(self.MODAL_OK_BTN)
            btn.click()
            logger.info("[confirm_delete] Ok clicked on delete modal")

            self.toast_text()
        except Exception as e:
            logger.error(f"[confirm_delete] Failed modal confirmation. Error: {e}")
            Screenshot.take("modal_failed")
