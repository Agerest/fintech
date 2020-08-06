import threading

import controller
from icq import icq_main
from telegram import telegram_main

if __name__ == '__main__':
    telegram_polling_thread = threading.Thread(target=telegram_main.init, args=())
    telegram_polling_thread.start()
    icq_polling_thread = threading.Thread(target=icq_main.init, args=())
    icq_polling_thread.start()
    flask_thread = threading.Thread(target=controller.init, args=())
    flask_thread.start()
    print('bot is started')
