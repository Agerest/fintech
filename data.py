import configparser

config_path = 'settings.ini'
config = configparser.ConfigParser()
config.read(config_path)

BOT_TOKEN = config.get('Telegram', 'BOT_TOKEN')
CUBA_HOST = config.get('Cuba', 'HOST')

CREATE_DEBIT_URL = config.get('Cuba', 'CREATE_DEBIT_URL')
CREATE_CREDIT_URL = config.get('Cuba', 'CREATE_CREDIT_URL')
CREATE_DEBIT_FULL_URL = config.get('Cuba', 'CREATE_DEBIT_FULL_URL')
CREATE_CREDIT_FULL_URL = config.get('Cuba', 'CREATE_CREDIT_FULL_URL')
SEND_MESSAGE_URL = config.get('Cuba', 'SEND_MESSAGE_URL')
GET_APPLICATION_LIST_URL = config.get('Cuba', 'GET_APPLICATION_LIST_URL')
GET_APPLICATION_URL = config.get('Cuba', 'GET_APPLICATION_URL')

FLASK_PORT = config.get('Flask', 'PORT')

ICQ_TOKEN = config.get('ICQ', 'TOKEN')
