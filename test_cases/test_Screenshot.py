import os
import pytest
from utils.screenshot import Screenshot

@pytest.mark.usefixtures("driver_function")
class TestScreenshot:

    def test_screenshot_creation(self, driver_function):
        """Verify that screenshot file is created successfully."""
        path = Screenshot.take(driver_function, "test_shot")

        assert path is not None, "Screenshot.take() returned None"
        assert os.path.exists(path), f"Screenshot not found at: {path}"

        # Optional: cleanup to keep reports clean
        os.remove(path)
