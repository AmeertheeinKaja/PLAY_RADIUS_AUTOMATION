import os
import time
from utils.logger import get_logger

logger = get_logger(__name__)

class Screenshot:
    BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "screenshots")

    @staticmethod
    def take(driver, name_prefix="screenshot"):
        try:
            os.makedirs(Screenshot.BASE_DIR, exist_ok=True)
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            file_name = f"{name_prefix}_{timestamp}.png"
            path = os.path.join(Screenshot.BASE_DIR, file_name)
            driver.save_screenshot(path)
            logger.info(f"Screenshot saved: {path}")
            return path
        except Exception as e:
            logger.error(f"Failed to capture screenshot: {e}")
            return None
