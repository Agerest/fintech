import configparser

config_path = 'settings.ini'
config = configparser.ConfigParser()
config.read(config_path)
BOT_TOKEN = config.get('Telegram', 'BOT_TOKEN')
HOST = config.get('Cuba', 'HOST')
CREATE_DEBIT_URL = config.get('Cuba', 'CREATE_DEBIT_URL')
CREATE_CREDIT_URL = config.get('Cuba', 'CREATE_CREDIT_URL')
SEND_MESSAGE_URL = config.get('Cuba', 'SEND_MESSAGE_URL')
