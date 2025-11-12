import configparser
config = configparser.RawConfigParser()
config.read('.\\configuration\\config.ini')


class ReadConfig:
    @staticmethod
    def get_login_url(self):
        url=config.get('login info','baseurl')
        return url
    def get_username(self):
        username=config.get('login info','username')
        return username
    def get_password(self):
        password=config.get('login info','password')
        return password