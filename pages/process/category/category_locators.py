from selenium.webdriver.common.by import By

class CategoryLocators:

    @staticmethod
    def for_category(name: str):
        return {
               "EDIT_BTN": (
                By.XPATH,
                f"//span[@title='{name}']/ancestor::div[@class='plver_box_headerin']//button[@title='Edit']"
            ),
            "DELETE_BTN": (
                By.XPATH,
                f"//span[@title='{name}']/ancestor::div[@class='plver_box_headerin']//button[@title='Delete']"
            ),
            "TAB_HEADER": (
                By.XPATH,
                f"//span[@title='{name}']/ancestor::div[@class='plver_box_headerin']"
            ),
            "EDIT_NAME_INPUT": (
                By.XPATH,
                f"//input[@value='{name}']/ancestor::div[@class='title_editable']//input[@id='floatingInput']"
            ),
            "EDIT_WEIGHT_INPUT": (
                By.XPATH,
                f"//input[@value='{name}']/ancestor::div[@class='title_editable']//input[@placeholder='Enter Weightage']"
            ),
            "SAVE_BTN": (
                By.XPATH,
                f"//input[@value='{name}']/ancestor::div[@class='plver_box_headerin']//button[@title='Save']"
            ),
            "CLOSE_BTN": (
                By.XPATH,
                f"//input[@value='{name}']/ancestor::div[@class='plver_box_headerin']//button[@title='Close']"
            )
        }
