import pytest
from selenium.webdriver.common.by import By

from pages.login.login import LoginPage
from pages.common.loader import Loader
from pages.process.process_manager.create_process import CreateProcess
from pages.common.sidemenupage import SideMenuPage
from pages.process.channel_config.call.call_stt_config import CallSTTConfig
from pages.login.logout import Logout
from utils.screenshot import Screenshot
from utils.logger import get_logger
from utils.data_reader import load_test_data

logger = get_logger(__name__)


@pytest.mark.usefixtures("driver_function")
class TestCallConfigSTT:

    # =========================================================
    # MAIN POSITIVE FLOW
    # =========================================================

    def test_call_config_stt(self, driver_function):
        """
        Full STT configuration test (happy path)
        """
        driver = driver_function
        logout = None

        try:
            login = LoginPage(driver)
            loader = Loader(driver)
            side_menu = SideMenuPage(driver)
            create_process = CreateProcess(driver)
            stt_config = CallSTTConfig(
                driver

            )
            logout = Logout(driver)

            login.open()
            login.login()
            loader.load()

            side_menu.process()
            loader.load()

            create_process.create_process()
            loader.load()

            stt_config.open_tab()
            stt_config.click_edit()

            stt_config.set_speech_to_text(True)
            stt_config.set_sample_rate(16000)
            stt_config.set_engine("google")
            stt_config.set_conversion_mode("manualMode")
            stt_config.set_bucket("play-asr")
            stt_config.set_bucket_path("QARADIUS")

            # Upload key file
            stt_config.upload_key_file("D:\\visnet\\google_api_key.json")

            # Save first
            stt_config.click_save()

            # Test flow
            stt_config.click_test()

            # Upload audio file
            stt_config.upload_audio_file("D:\\visnet\\audio1.mp3")

            # The modal should appear only AFTER uploading audio file
            stt_config._handle_modal(stt_config.MODAL_BTN_SUBMIT)

            assert stt_config.last_toast in [
                stt_config.MSG_TEST_SUCCESS,
                stt_config.MSG_CONVERT_SUCCESS,
                stt_config.MSG_UPDATE_SUCCESS
            ]



        except Exception as e:
            Screenshot.take(driver, "test_call_config_stt_failure")
            logger.error("STT configuration failed", exc_info=True)
            raise

        finally:
            if logout:
                try:
                    logout.logout()
                except:
                    pass

    def test_sample_rate_required(self, driver_function):
        driver = driver_function
        logout = None

        try:
            full_cfg = load_test_data("process/create_process.json")
            stt_cfg = full_cfg["channel_config"]["call"]["stt"]
            login = LoginPage(driver)
            loader = Loader(driver)
            side_menu = SideMenuPage(driver)
            create_process = CreateProcess(driver)
            stt_config = CallSTTConfig(
                driver,
                speech_to_text=stt_cfg.get("speech_to_text"),

                engine=stt_cfg.get("engine_name"),
                bucket_name=stt_cfg.get("bucket_name"),
                bucket_dir=stt_cfg.get("bucket_dir"),
                key_file=stt_cfg.get("keyFile"),
                audio_file=stt_cfg.get("audioFile"),
                mode=stt_cfg.get("conversion_mode")
            )
            logout = Logout(driver)

            login.open()
            login.login()
            loader.load()

            side_menu.process()
            loader.load()
            create_process.create_process()
            loader.load()

            stt_config.open_tab()
            stt_config.click_edit()
            stt_config.set_speech_to_text()

            stt_config.set_engine()
            stt_config.set_bucket("")

            stt_config.set_bucket_path()

            # File uploads
            stt_config.upload_key_file()
            stt_config.click_save()

            error_msg = stt_config.get_error_for("sample_rate")
            assert error_msg == "This field is required"

        except Exception:
            Screenshot.take(driver, "sample_rate_required_failure")
            raise

        finally:
            if logout:
                try:
                    logout.logout()
                except:
                    pass

    def test_engine_name_required(self, driver_function):
        driver = driver_function
        logout = None

        try:
            full_cfg = load_test_data("process/create_process.json")
            stt_cfg = full_cfg["channel_config"]["call"]["stt"]
            login = LoginPage(driver)
            loader = Loader(driver)
            side_menu = SideMenuPage(driver)
            create_process = CreateProcess(driver)
            stt_config = CallSTTConfig(
                driver,
                speech_to_text=stt_cfg.get("speech_to_text"),
                sample_rate=stt_cfg.get("sample_rate"),

                bucket_name=stt_cfg.get("bucket_name"),
                bucket_dir=stt_cfg.get("bucket_dir"),
                key_file=stt_cfg.get("keyFile"),
                audio_file=stt_cfg.get("audioFile"),
                mode=stt_cfg.get("conversion_mode")
            )
            logout = Logout(driver)

            login.open()
            login.login()
            loader.load()

            side_menu.process()
            loader.load()
            create_process.create_process()
            loader.load()

            stt_config.open_tab()
            stt_config.click_edit()
            stt_config.set_speech_to_text()
            stt_config.set_sample_rate()


            stt_config.click_save()

            error_msg = stt_config.get_error_for("engine")
            assert error_msg == "This field is required"

        except Exception:
            Screenshot.take(driver, "engine_required_failure")
            raise

        finally:
            if logout:
                try:
                    logout.logout()
                except:
                    pass

    def test_bucket_name_required(self, driver_function):
        driver = driver_function
        logout = None

        try:
            full_cfg = load_test_data("process/create_process.json")
            stt_cfg = full_cfg["channel_config"]["call"]["stt"]
            login = LoginPage(driver)
            loader = Loader(driver)
            side_menu = SideMenuPage(driver)
            create_process = CreateProcess(driver)
            stt_config = CallSTTConfig(
                driver,
                speech_to_text=stt_cfg.get("speech_to_text"),
                sample_rate=stt_cfg.get("sample_rate"),
                engine=stt_cfg.get("engine_name"),

                bucket_dir=stt_cfg.get("bucket_dir"),
                key_file=stt_cfg.get("keyFile"),
                audio_file=stt_cfg.get("audioFile"),
                mode=stt_cfg.get("conversion_mode")
            )
            logout = Logout(driver)

            login.open()
            login.login()
            loader.load()

            side_menu.process()
            loader.load()
            create_process.create_process()
            loader.load()

            stt_config.open_tab()
            stt_config.click_edit()
            stt_config.set_speech_to_text()
            stt_config.set_sample_rate()
            stt_config.set_engine()


            stt_config.set_bucket_path()

            # File uploads
            stt_config.upload_key_file()
            stt_config.click_save()

            error_msg = stt_config.get_error_for("bucket_name")
            assert error_msg == "This field is required"

        except Exception:
            Screenshot.take(driver, "bucket_name_required_failure")
            raise

        finally:
            if logout:
                try:
                    logout.logout()
                except:
                    pass

    def test_bucket_directory_required(self, driver_function):
        driver = driver_function
        logout = Logout(driver)

        try:
            full_cfg = load_test_data("process/create_process.json")
            stt_cfg = full_cfg["channel_config"]["call"]["stt"]
            login = LoginPage(driver)
            loader = Loader(driver)
            side_menu = SideMenuPage(driver)
            create_process = CreateProcess(driver)

            stt_config = CallSTTConfig(
                driver,
                speech_to_text=stt_cfg.get("speech_to_text"),
                sample_rate=stt_cfg.get("sample_rate"),
                engine=stt_cfg.get("engine_name"),
                bucket_name=stt_cfg.get("bucket_name"),

                key_file=stt_cfg.get("keyFile"),
                audio_file=stt_cfg.get("audioFile"),
                mode=stt_cfg.get("conversion_mode")
            ) # empty bucket directory

            login.open()
            login.login()
            loader.load()

            side_menu.process()
            loader.load()
            create_process.create_process()
            loader.load()

            stt_config.open_tab()
            stt_config.click_edit()
            stt_config.set_speech_to_text()
            stt_config.set_sample_rate()
            stt_config.set_engine()

            stt_config.set_bucket()

            stt_config.upload_key_file()

            stt_config.click_save()

            error_msg = stt_config.get_error_for("bucket_dir")
            assert error_msg == "This field is required"

        except Exception:
            Screenshot.take(driver, "bucket_dir_required_failure")
            raise

        finally:
            try:
                logout.logout()
            except:
                pass


    def test_key_file_required(self, driver_function):
        driver = driver_function
        logout = Logout(driver)

        try:
            full_cfg = load_test_data("process/create_process.json")
            stt_cfg = full_cfg["channel_config"]["call"]["stt"]
            login = LoginPage(driver)
            loader = Loader(driver)
            side_menu = SideMenuPage(driver)
            create_process = CreateProcess(driver)

            stt_config = CallSTTConfig(
                driver,
                speech_to_text=stt_cfg.get("speech_to_text"),
                sample_rate=stt_cfg.get("sample_rate"),
                engine=stt_cfg.get("engine_name"),
                bucket_name=stt_cfg.get("bucket_name"),
                bucket_dir=stt_cfg.get("bucket_dir"),

                audio_file=stt_cfg.get("audioFile"),
                mode=stt_cfg.get("conversion_mode")
            ) # empty file

            login.open()
            login.login()
            loader.load()

            side_menu.process()
            loader.load()
            create_process.create_process()
            loader.load()

            stt_config.open_tab()
            stt_config.click_edit()
            stt_config.set_speech_to_text()
            stt_config.set_sample_rate()
            stt_config.set_engine()
            stt_config.set_bucket()
            stt_config.set_bucket_path()

            stt_config.click_save()


            error_msg = stt_config.get_error_for("key_file")
            assert error_msg == "This field is required"

        except Exception:
            Screenshot.take(driver, "key_file_required_failure")
            raise

        finally:
            try:
                logout.logout()
            except:
                pass

    def test_audio_file_required(self, driver_function):
        driver = driver_function
        logout = Logout(driver)

        try:
            full_cfg = load_test_data("process/create_process.json")
            stt_cfg = full_cfg["channel_config"]["call"]["stt"]
            login = LoginPage(driver)
            loader = Loader(driver)
            side_menu = SideMenuPage(driver)
            create_process = CreateProcess(driver)

            # Force the audio_file to be empty
            stt_config = CallSTTConfig(
                driver,
                speech_to_text=stt_cfg.get("speech_to_text"),
                sample_rate=stt_cfg.get("sample_rate"),
                engine=stt_cfg.get("engine_name"),
                bucket_name=stt_cfg.get("bucket_name"),
                bucket_dir=stt_cfg.get("bucket_dir"),
                key_file=stt_cfg.get("keyFile"),

                mode=stt_cfg.get("conversion_mode")
            )

            # Login flow
            login.open()
            login.login()
            loader.load()

            side_menu.process()
            loader.load()
            create_process.create_process()
            loader.load()

            # Start configuring STT
            stt_config.open_tab()
            stt_config.click_edit()

            stt_config.set_speech_to_text()
            stt_config.set_sample_rate()
            stt_config.set_engine()
            stt_config.set_conversion_mode()
            stt_config.set_bucket()
            stt_config.set_bucket_path()

            # Upload ONLY key file, SKIP audio file intentionally
            stt_config.upload_key_file()
            stt_config.click_save()

            # Click Test, which should trigger the validation for missing audioFile
            stt_config.click_test()
            stt_config._handle_modal(stt_config.MODAL_BTN_SUBMIT)

            # Expecting validation message for missing audio file
            error_msg = stt_config.get_error_for("audio_file")
            assert error_msg == "This field is required"

        except Exception:
            Screenshot.take(driver, "audio_file_required_failure")
            raise

        finally:
            try:
                logout.logout()
            except:
                pass

    def test_toggle_speech_to_text(self, driver_function):
        driver = driver_function
        logout = Logout(driver)

        try:
            full_cfg = load_test_data("process/create_process.json")
            stt_cfg = full_cfg["channel_config"]["call"]["stt"]
            login = LoginPage(driver)
            loader = Loader(driver)
            side_menu = SideMenuPage(driver)
            create_process = CreateProcess(driver)
            stt_config = CallSTTConfig(
                driver,
                speech_to_text=stt_cfg.get("speech_to_text"),
                sample_rate=stt_cfg.get("sample_rate"),
                engine=stt_cfg.get("engine_name"),
                bucket_name=stt_cfg.get("bucket_name"),
                bucket_dir=stt_cfg.get("bucket_dir"),
                key_file=stt_cfg.get("keyFile"),
                audio_file=stt_cfg.get("audioFile"),
                mode=stt_cfg.get("conversion_mode")
            )

            login.open()
            login.login()
            loader.load()

            side_menu.process()
            loader.load()
            create_process.create_process()
            loader.load()

            stt_config.open_tab()
            stt_config.click_edit()

            # Correct locators
            toggle_input = driver.find_element(By.NAME, "isEnableSTT")
            toggle_slider = driver.find_element(By.XPATH, "//input[@name='isEnableSTT']/following-sibling::span")

            # Toggle OFF → ON
            toggle_slider.click()
            assert toggle_input.is_selected() is True

            # Toggle ON → OFF
            toggle_slider.click()
            assert toggle_input.is_selected() is False

        finally:
            try:
                logout.logout()
            except:
                pass

    def test_conversion_mode_switching(self, driver_function):
        driver = driver_function
        logout = Logout(driver)

        try:
            full_cfg = load_test_data("process/create_process.json")
            stt_cfg = full_cfg["channel_config"]["call"]["stt"]


            login = LoginPage(driver)
            loader = Loader(driver)
            side_menu = SideMenuPage(driver)
            create_process = CreateProcess(driver)

            stt_config = CallSTTConfig(
                driver,
                speech_to_text=stt_cfg.get("speech_to_text"),
                sample_rate=stt_cfg.get("sample_rate"),
                engine=stt_cfg.get("engine_name"),
                bucket_name=stt_cfg.get("bucket_name"),
                bucket_dir=stt_cfg.get("bucket_dir"),
                key_file=stt_cfg.get("keyFile"),
                audio_file=stt_cfg.get("audioFile"),
                mode=stt_cfg.get("conversion_mode")
            )

            login.open()
            login.login()
            loader.load()

            side_menu.process()
            loader.load()
            create_process.create_process()
            loader.load()

            stt_config.open_tab()
            stt_config.click_edit()
            stt_config.set_speech_to_text()
            stt_config.set_sample_rate()
            stt_config.set_engine()

            # Set Manual Mode
            stt_config.set_conversion_mode("manualMode")
            manual_radio = driver.find_element(*stt_config.STT_RADIO_CONVERSION_MODE_MANUAL)
            assert manual_radio.is_selected()

            # Set Auto Mode
            stt_config.set_conversion_mode("autoMode")
            auto_radio = driver.find_element(*stt_config.STT_RADIO_CONVERSION_MODE_AUTO)
            assert auto_radio.is_selected()

        except Exception:
            Screenshot.take(driver, "conversion_mode_switching_failure")
            raise

        finally:
            try:
                logout.logout()
            except:
                pass

    def test_stt_with_json_data(self, driver_function):
        driver = driver_function
        logout = Logout(driver)

        try:
            # Load the JSON data
            full_cfg = load_test_data("process/create_process.json")
            stt_cfg = full_cfg["channel_config"]["call"]["stt"]
            # Page objects
            login = LoginPage(driver)
            loader = Loader(driver)
            side_menu = SideMenuPage(driver)
            create_process = CreateProcess(driver)

            # Build STT config using JSON
            stt_config = CallSTTConfig(
                driver,
                speech_to_text=stt_cfg.get("speech_to_text"),
                sample_rate=stt_cfg.get("sample_rate"),
                engine=stt_cfg.get("engine_name"),
                bucket_name=stt_cfg.get("bucket_name"),
                bucket_dir=stt_cfg.get("bucket_dir"),
                key_file=stt_cfg.get("keyFile"),
                audio_file=stt_cfg.get("audioFile"),
                mode=stt_cfg.get("conversion_mode")
            )

            # Login
            login.open()
            login.login()
            loader.load()

            # Navigate and create process
            side_menu.process()
            loader.load()
            create_process.create_process()
            loader.load()

            # Apply STT configuration
            stt_config.configure_stt()

            # Validation
            assert stt_config.last_toast in [
                stt_config.MSG_TEST_SUCCESS,
                stt_config.MSG_CONVERT_SUCCESS,
                stt_config.MSG_UPDATE_SUCCESS
            ], "STT JSON configuration did not complete successfully"

        except Exception:
            Screenshot.take(driver, "test_stt_with_json_data_failure")
            raise

        finally:
            try:
                logout.logout()
            except:
                pass