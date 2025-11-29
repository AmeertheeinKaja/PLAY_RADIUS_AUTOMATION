import configparser

config = configparser.RawConfigParser()
config.read('.\\configurations\\config.ini')


class ReadConfig:
    @staticmethod
    def get_login_url():
        return config.get('login info', 'baseurl')

    @staticmethod
    def get_username():
        return config.get('login info', 'username')

    @staticmethod
    def get_password():
        return config.get('login info', 'password')
