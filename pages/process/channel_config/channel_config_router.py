from _pytest.config import Config

from pages.process.channel_config.call.call_sa_config import CallSAConfig
from pages.process.channel_config.call.call_stt_config import CallSTTConfig
from pages.process.channel_config.call.call_storage_config import CallStorageConfig
from pages.process.channel_config.chat.chat_sa_config import ChatSAConfig
from pages.process.channel_config.chat.chat_storage_config import ChatStorageConfig
from pages.process.channel_config.email.email_sa_config import EmailSAConfig
from pages.process.channel_config.email.email_storage_config import EmailStorageConfig
from pages.process.channel_config.video.video_storage_config import VideoStorageConfig
from pages.process.channel_config.video.video_sa_config import VideoSAConfig
from pages.process.channel_config.video.video_stt_config import VideoSTTConfig
from utils.logger import get_logger
logger = get_logger(__name__)

class ChannelConfigRouter:
    def __init__(self, driver,config):
        self.driver = driver
        self.config = config
        self.call_storage = CallStorageConfig(driver)
        self.call_sa = CallSAConfig(driver)
        self.call_stt = CallSTTConfig(driver)
        # self.chat_storage = ChatStorageConfig(driver)
        # self.chat_sa = ChatSAConfig(driver)
        # self.email_storage = EmailStorageConfig(driver)
        # self.email_sa = EmailSAConfig(driver)
        # self.video_storage = VideoStorageConfig(driver)
        # self.video_sa = VideoSAConfig(driver)
        # self.video_stt = VideoSTTConfig(driver)

    def route_call_missing_key(self):


        # STT
        call_cfg = self.config["channel_config"]["call"]

        stt_cfg = call_cfg["stt"]

        stt = CallSTTConfig(
            self.driver,
            speech_to_text=stt_cfg.get("speech_to_text"),
            sample_rate=stt_cfg.get("sample_rate"),
            engine_name=stt_cfg.get("engine_name"),
            bucket_name=stt_cfg.get("bucket_name"),
            bucket_dir=stt_cfg.get("bucket_dir"),
            keyFile=stt_cfg.get("keyFile"),
            audioFile=stt_cfg.get("audioFile"),
            conversion_mode=stt_cfg.get("conversion_mode")
        )

        # stt.reconfigure_stt()
        # SA

        sa_cfg = call_cfg["sa"]

        sa_config = CallSAConfig(
            self.driver,
            sentiment_analysis=sa_cfg.get("sentiment_analysis"),
            engine_name=sa_cfg.get("engine_name"),
            keyFile=sa_cfg.get("keyFile"),
            sentiment_text=sa_cfg.get("sentiment_text"),
            conversion_mode=sa_cfg.get("conversion_mode")
        )
        logger.info(f"Sentiment Analysis Mode: {sa_cfg.get('sentiment_analysis')}")
        logger.info(f"Sentiment Text Mode: {sa_cfg.get('sentiment_text')}")
        logger.info(f"Conversion Mode: {sa_cfg.get('conversion_mode')}")
        logger.info(f"engine_name: {sa_cfg.get('engine_name')}")


        sa_config.reconfig_sa()

        logger.info("Call channel: STT + SA configured successfully due to missing key")

    def route_chat_missing_key(self):
        # chat_cfg = self.config["channel_config"]["chat"]
        #
        # # SA
        # sa_cfg = chat_cfg["sa"]
        # ChatSAConfig(self.driver, **sa_cfg).config_sentiment_analysis()

        logger.info("Chat channel: SA configured successfully due to missing key")

    def route_video_missing_key(self):
        video_cfg = self.config["channel_config"]["video"]

        # # STT
        # stt_cfg = video_cfg["stt"]
        # VideoSTTConfig(self.driver, **stt_cfg).configure_stt()
        #
        # # SA
        # sa_cfg = video_cfg["sa"]
        # VideoSAConfig(self.driver, **sa_cfg).config_sa()

        logger.info("Video channel: STT + SA configured successfully due to missing key")

    def route_email_missing_key(self):
        email_cfg = self.config["channel_config"]["email"]

        # SA
        # sa_cfg = email_cfg["sa"]
        # EmailSAConfig(self.driver, **sa_cfg).config_sentiment_analysis()

        logger.info("Email channel: SA configured successfully due to missing key")

    def route_call_storage_missing_key(self):
        # self.config should be the top-level config dict
        call_cfg = self.config["channel_config"]["call"]
        storage_json = call_cfg["storage"]  # <-- correct path

        storage_page = CallStorageConfig(self.driver)
        storage_page.edit_storage_config(storage_json)

        logger.info("Call channel: Storage configured successfully due to missing key")
